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

import sys
from time import sleep
import serial

# From here on, "s" is always the serial object for the ALDL link.

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

        checksum_in = s.read()[0]

        if checksum != checksum_in:
            print("Warning: Checksum fail. Msg: {:02x} {:02x} {:02x}".format(
                msg_id, msg_len + 0x56, msg_mode), end="", file=sys.stderr)
            for b in msg_body:
                print(" {:02x}".format(b), end="", file=sys.stderr)
            print(" {:02x}".format(checksum_in), file=sys.stderr)
        else:
            return (msg_id, msg_mode, msg_body)

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
    msg.append(~checksum & 0xff)

    s.write(msg)

# This function should be called with an open serial object. It starts with
# the actual communication and echoing.
def parse_stream(s):
    #s.write(b'\xf4\x57\x01\x00\xb4')
    message_send(s, 0xf4, 0x01, b'\x00')
    #message_send(s, 0xf5, 0x01, b'\x00')
    #message_send(s, 0xf5, 0x01, b'\x01')

    try:
        while True:
            #sleep(0.2)
            #message_send(s, 0xf4, 0x01, b'\x00')
            #print(message_recv(s))

            #sleep(0.2)
            #message_send(s, 0xf5, 0x01, b'\x00')
            #print(message_recv(s))

            #sleep(0.2)
            #message_send(s, 0xf5, 0x01, b'\x01')

            print(message_recv(s))
    except KeyboardInterrupt:
        print("Stopping...", file=sys.stderr)

def main(serial_port):
    try:
        s = serial.Serial(serial_port, 8192)
    except SerialException as e:
        print("Error: {}".format(e.strerror))
        sys.exit(1)
    else:
        parse_stream(s)
        s.close()

if __name__ == "__main__":
    if "--help" in sys.argv:
        print("Usage: {} {{<serial_port> | --help}}".format(sys.argv[0]),
                file=sys.stderr)
        sys.exit(0)

    try:
        main(sys.argv[1])
    except IndexError:
        print("Usage: {} {{<serial_port> | --help}}".format(sys.argv[0]),
                file=sys.stderr)
        sys.exit(2)
