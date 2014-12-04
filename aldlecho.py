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
import serial

def parse_stream(s):
    pass

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
