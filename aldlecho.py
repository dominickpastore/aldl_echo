#!/usr/bin/env python3

#
# ALDL Echo
#
# Copyright © 2014 Dominick C. Pastore
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

#TODO
#Use getopt
#Make it read from a definition file

#TODO definition file
# Definition file could be a bunch of lines, each with the "DATA NAME" and
# "DESCRIPTION". If a word has descriptions for each bit, just leave the "DATA
# NAME" part of the next 8 lines blank. The program can recognize leading
# whitespace and know they're bit descriptions.
# The file can start with the message ID for this data stream and the mode and
# message_body to get the ECM in and out of data transmission mode
# Maybe have a way to include multiple transmit modes in one data stream? Or
# even multiple data streams in a file?
# The program will know which data stream to use based on a) the message ID and
# b) the message length (and maybe c) the mode)

import sys
import argparse
from time import sleep
from collections import OrderedDict
import serial

#### Global variables ##########################################################

# A list of tuples (id, mode, message) containing commands to put the ECM back
#in normal mode. There may be more than one if multiple data stream definitions
# are used.
normal_mode_cmds = []

# A list of tuples (id, mode, message) containing commands that will put the ECM
# in various transmit modes. There will be more than one if multiple data stream
# definitions are used. Also, some data streams may specify mutliple transmit
# modes alone.
transmit_mode_cmds = []

# A dictionary containing the transmit modes the ECM can be in. This dict will
# contain the bulk of the information from the data stream definitions.
# The keys will be tuples containing the id, mode, and message length. When an
# incoming message arrives, these fields will be used to look up the data format
# to parse it as.
# Each value will be a list of tuples. Each tuple corresponds to one byte of
# data. Here is roughly what this list should look like:
#  [ ("BYTENAME", 1, "English description of byte", None),
#    ("BYTENAME2", 1, "Description of byte with conversion", "n * 5 / 256"),
#    ("WORDNAME3", 2, "Description of 16-bit value", None),
#    ("BYTEFLAG4", 1, "Description of byte with flag bits",
#      ( ("Description of flag bit 0", "Value if 0", "Value if 1")
#        ("Description of flag bit 1, uses default yes/no values", None, None)
#        ("Description of flag bit 0", "Value if 0", "Value if 1")
#        ("Description of flag bit 0", "Value if 0", "Value if 1")
#        ("Description of flag bit 0", "Value if 0", "Value if 1")
#        ("Description of flag bit 0", "Value if 0", "Value if 1")
#        ("Description of flag bit 0", "Value if 0", "Value if 1")
#        ("Description of flag bit 0", "Value if 0", "Value if 1")
#        ("Description of flag bit 0", "Value if 0", "Value if 1") ) )
#    ... ]
transmit_mode_data = dict()

#### Data parsing and formatting ###############################################

def parse_data_stream_defn(f):
    global normal_mode_cmds
    global transmit_mode_cmds
    global transmit_mode_data

    # Some state variables
    msg_id = None
    have_normal_cmd = False
    msg_mode = None
    data_count = None
    byte_num = 0
    bit_num = 0

    # To store our data until we add it to the globals above
    normal_mode_cmd = None
    transmit_mode_cmd = []
    transmit_mode_data_key = []
    transmit_mode_data_val = []

    try:
        line_num = 0
        for line in f:
            line_num += 1
            # Ignore comments and empty lines
            line = line.strip()
            if line == '':
                continue

            # Tokenize strings out (not 100% trivial since quotes are optional)
            strings = []
            while line != '':
                if line[0] != '"':
                    # Take off a word and add it
                    split_line = line.split(maxsplit=1)
                    strings.append(split_line[0])
                    try:
                        line = split_line[1]
                    except IndexError:
                        line = ''
                else:
                    # Take off everything until the next quotes and add it
                    line = line[1:]
                    # Let's only match quotes followed by a space. Be a little
                    # flexible with what we accept.
                    string, sep, line = line.partition('" ')
                    strings.append(string)

            # Parse data out from here until end of for loop
            if msg_id == None:
                # Verify it's an 8192 baud format
                if int(strings[0]) != 8192:
                    #TODO raise exception
                    print("Parse error (bad baud) line " + str(line_num), file=sys.stderr)
                msg_id = int(strings[1])
                have_id = True

            elif not have_normal_cmd:
                normal_mode_cmd = (msg_id, int(strings[0]),
                    bytes([int(x) for x in strings[1:]]))
                have_normal_cmd = True
                
            elif msg_mode == None:
                msg_mode = int(strings[0])
                transmit_mode_cmd.append((msg_id, msg_mode,
                    bytes([int(x) for x in strings[1:]])))

            elif data_count == None:
                data_count = int(strings[0])
                transmit_mode_data_key.append((msg_id, msg_mode, data_count))
                transmit_mode_data_val.append(List())

            else:
                pass
                #TODO parse a data byte/bit line and increment byte/bit_num
                #and set bit_num to zero as appropriate
                
                #TODO set have_transmit_cmd to False and have_data_count to
                #None after finished reading a transmit block. Not 100% sure
                #how because when the last byte is encountered, there may still
                #be bits after it.
                
    except ValueError as e:
        #TODO raise exception
        print("Parse error (ValueError) line " + str(line_num), file=sys.stderr)
    except IndexError as e:
        #TODO raise exception
        print("Parse error (IndexError) line " + str(line_num), file=sys.stderr)
    finally:
        f.close()

def parse_data(msg_body):
    pass

def print_formatted(msg):
    print("ID:    {:#04x}".format(msg[0]))
    print("Mode:  {:#04x}".format(msg[1]))
    print("Body:")
    for i in range(len(msg[2])):
        print("   {0:3d}:  {1:#04x}  {2:04b} {3:04b}  {1:3d}".format(i,
            msg[2][i], msg[2][i] >> 4, msg[2][i] >> 0x0f))

#### Serial interface ##########################################################

# s is the serial object
def message_recv(s):
    """Wait for a valid message, then return its contents

    Wait for either an 0xf4 or an 0xf5. When it comes, read the rest of the
    message and verify its checksum. If all checks out, then return the message
    as an (id, mode, message) tuple. Otherwise, try again.
    """
    while True:
        msg_id = None
        msg_len = None
        msg_mode = None
        msg_body = None
        
        while msg_id != 0xf4 and msg_id != 0xf5:
            msg_id = s.read()[0]

        checksum = msg_id
        
        msg_len = s.read()[0]
        checksum += msg_len
        msg_len -= 0x56
        
        msg_mode = s.read()[0]
        checksum += msg_mode

        msg_body = s.read(msg_len)
        for b in msg_body:
            checksum += b

        checksum = (-checksum) & 0xff
        checksum_in = s.read()[0]

        if checksum != checksum_in:
            print("Warning: Checksum fail. Msg: {:02x} {:02x} {:02x}".format(
                msg_id, msg_len + 0x56, msg_mode), end="", file=sys.stderr)
            for b in msg_body:
                print(" {:02x}".format(b), end="", file=sys.stderr)
            print(" {:02x}".format(checksum_in), file=sys.stderr)
        else:
            return (msg_id, msg_mode, msg_body)

# s is the serial object
def message_send(s, msg_id, msg_mode, msg_body):
    """Send a message to the ECM.

    Message length and checksum are calculated automatically. See the data
    stream definition for what the parameters mean.

    Arguments:
    s: An open serial object
    msg_id: An integer representing the message ID
    msg_mode: An integer representing the message mode
    msg_body: A bytes or bytearray object containing the message body
    """
    msg = bytearray()
    msg.append(msg_id)
    checksum = msg_id

    msg_len = 0x56 + len(msg_body)
    msg.append(0x56 + len(msg_body))
    checksum = (checksum + msg_len)

    msg.append(msg_mode)
    checksum = (checksum + msg_mode)

    msg += msg_body
    for b in msg_body:
        checksum = (checksum + b)

    # Checksum is 1's compliment of sum of all bytes in the message
    msg.append((-checksum) & 0xff)

    s.write(msg)
    #DEBUG
    #print("@@@ 1", repr(msg), file=sys.stderr)

# This function should be called with an open serial object. It starts with
# the actual communication and echoing.
# s is the serial object
def manage_stream(s):
    # It seems this works (on 8192 baud ALDL's) by sending one command
    # requesting a data transmit mode, which the ECM responds to with one
    # message of data. It's not entirely clear what mode the ECM is left in
    # after this happens, but two things seem apparent:
    #   1) The ECM will not send any more data until another request is sent to
    #      it.
    #   2) It's probably a good idea to send a "switch to normal mode" command
    #      before terminating the serial link. The Windows ALDL program that
    #      I analyzed did this, and the normal mode command must exist for some
    #      reason, after all. Hopefully this doesn't mean there is a potential
    #      safety risk if the program crashes before this is sent!

    #message_send(s, 0xf4, 0x01, b'\x00')
    #message_send(s, 0xf5, 0x01, b'\x00')
    #message_send(s, 0xf5, 0x01, b'\x01')

    try:
        while True:
            #sleep(1)
            message_send(s, 0xf4, 0x01, b'\x00')
            new_msg = message_recv(s)
            print("\n### New Message ###")
            print_formatted(new_msg)

            #sleep(1)
            #message_send(s, 0xf5, 0x01, b'\x00')
            #new_msg = message_recv(s)
            #print("\n### New Message ###")
            #print_formatted(new_msg)

            #sleep(1)
            #message_send(s, 0xf5, 0x01, b'\x01')
            #new_msg = message_recv(s)
            #print("\n### New Message ###")
            #print_formatted(new_msg)
    except KeyboardInterrupt:
        print("Stopping...", file=sys.stderr)

    # Restore normal mode
    message_send(s, 0xf4, 0x00, b'')
    #message_send(s, 0xf5, 0x00, b'')

#### Program startup and init ##################################################

def main(args):
    for f in args.data_stream:
        parse_data_stream_defn(f)

    try:
        s = serial.Serial(args.port, 8192)
    except serial.SerialException as e:
        print("Error: {}".format(e.strerror))
        sys.exit(1)
    else:
        manage_stream(s)
        s.close()

if __name__ == "__main__":
    ap = argparse.ArgumentParser(
            description="Echo data parsed from the ALDL port",
            epilog="See the README for full documentation.")
    ap.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
    ap.add_argument("port",
            help="The serial port to use (e.g. COM1, /dev/ttyACM0)")
    ap.add_argument("data_stream", nargs='+', type=argparse.FileType('r'),
            help="One or more data stream definition files")


    args = ap.parse_args()

    main(args)
