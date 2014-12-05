ALDL Echo
=========

A simple Python program to echo data parsed from the ALDL port on old GM cars.

**Note that the documentation in this README is a bit ahead of the program right
now, since it is still in development.**

I made this program to be a simple reference implementation for using the ALDL
protocol. Almost all existing programs that use the ALDL port are Windows only
and closed source. I wanted to make a simple, open source program that parses
and echoes data from the port. That way, when I (or anyone else) embark on a
more substantial project that uses ALDL, there will be an existing, working
implementation to look over.

This program was written specifically for my Suburban (a 1994 1/2 ton model with
the L05 engine (5.7L V8 TBI, VIN=K) and 4L60E transmission). Out of the box,
only cars very similar to it will be supported. That being said, as long as your
car uses the 8192 baud variant of ALDL, it should take little effort to add
support for it. See "Data Streams" for how to do that. If your car only uses the
160 baud variant of ALDL, unfortunately, this program cannot easily support your
car as is (though with more effort, and the will to dive into a bit of
programming, it's still very possible. The documentation is here).

If none of the above makes sense to you, try reading the rest of this README,
which explains more about ALDL.

Even if all of the above makes sense to you, you should read the rest of this
README. It contains useful information.

**Disclaimer: My area of expertise is computer science, not cars. All
information in this README is the result of copious Googling. I cannot be held
responsible for any injury, damage, or loss of life or property that results
from the your use of this file or mistakes it may contain.**

Usage
-----

    aldlecho.py [-h | --help] [-v | --version] <serial_port> <data_stream_definition> ...

 *  `-h`/`--help` -- Show a short usage message
 *  `-v`/`--version` -- Show the version information for the program
 *  `<serial_port>` -- The name of the serial port to use. On Windows, something
    like `COM1`. On Linux, something like `/dev/ttyS0` or `/dev/ttyACM0`
 *  `<data_stream_definition> ...` -- One or more data stream definition files.
    See "Data Streams."

Prerequisites and Limitations
-----------------------------

This program requires Python 3 and PySerial.

Note that this program requires at least one data stream definition file that
is appropriate for your car in order to work properly. Definitions are already
included for the Suburban I wrote this for (A217 and A218). If your car uses a
data stream other than A217 or A218, you'll need to create a definition file
for it. See "Data Streams" for more information.

As this program is written right now, it only supports the 8192 baud data
streams. And, unfortunately, adding support for the 160 baud streams is a bit
harder than just changing a constant in the source code. The 8192 baud streams
are packet-based with all packets following the same basic format with a header
and checksum. The 160 baud streams, meanwhile, just send the same block of data,
no header or checksum, over and over (as far as I can tell). That being said, it
may not be too hard to modify the program to do away with headers and checksums
for those data streams. The code to parse the actual data itself would still be
useful, after all.

If anyone creates more data stream definition files or adds 160 baud support,
feel free to send me a pull request :)

Data Streams
------------

An ALDL data stream is sort of like a dialect of ALDL. It describes what modes
an ECM can be in, the exact command to change modes, and what particular pieces
of data that ECM will send when in each mode. Which data stream to use depends on your car's make, year, engine, etc. Because of this, the program requires you
to specify a data stream definition file on the command line.

Chances are, you are going to have to make this data stream definition file
yourself. Luckily, the "AlDlstuff.rar" archive that should have come with this
program (obtained from [this forum post][1]) documents in detail pretty much
every ALDL data stream in existence.

Inside the archive, there are many "Axxx.DS" files and a couple more other
files. Every file in the archive is a plain text document, no matter what its
extension is. Each "Axxx.DS" file documents one data stream. To find the correct
one, check the "INDEX.DOC" file (still a plain text file, not a Word document!)
for an entry that matches your engine. Here is a sample from the file:

      DATA STREAM A136
           ENGINE USAGE:
                  3.1L TBI   (LG6)   (VIN=D)   91 U VAN
                  3.1L TBI   (LG6)   (VIN=D)   92 U VAN
                  3.1L TBI   (LG6)   (VIN=D)   93 U VAN
                  3.1L TBI   (LG6)   (VIN=D)   94 U VAN
                  3.1L TBI   (LG6)   (VIN=D)   95 U VAN

This entry says that stream A136 is for an engine control module (a.k.a. ECM;
there are also transmission control modules (TCM) and others). It lists all the
engines it applies to. In this case, all are 3.1L throttle-body injection (TBI)
engines with [RPO][2] "LG6", VIN's engine digit (8th digit in VIN) is "D," model
years '91-'95, and all are in vans. The "U" may mean USA-assembled, or be a VIN
digit, or something else. Most entries follow that same rough format, though the
file isn't exactly well-organized.

Hopefully that is enough to find the correct data stream. If more than one
stream lists the proper engine, check to see if one might be for a different
part, such as the transmission.

Some of the other files in the archive also contain tables to look up data
stream numbers for various parts. They may prove to be helpful if you are having
trouble finding the correct entry in the main index file.

A couple files in the archive describe other aspects of the ALDL signal, such as
the voltage levels and timing info for the serial data. These may be useful if
you plan to build your own hardware to interface with the port.

Once you find the file documenting the proper data stream for your car, you are
ready to create a well-formed definition file for the program to use.

### Data Stream Definition File Format ###

The format for this file is relatively straightforward. If it helps, the two
data stream definition files that came with this program are commented and can
be used as a reference.

TODO

A Quick Background
------------------

Assembly Line Diagnostic Link (ALDL), sometimes called OBD-I, was GM's precursor
to OBD-II, which is the on-board diagnostics system used in modern cars. ALDL
was used roughly from 1988 through 1995, when the OBD-II standard replaced it.

There were a few different connectors used with ALDL. For the most part,
American cars used the 12-pin connector below, though different cars made use of
different pins. If present, however, the same pin generally had the same
function, no matter which car it was in. Some cars did use other connectors,
especially around '95, when GM started putting the OBD-II connector in some
cars, before actually adopting the OBD-II standard completely.

    The 12-pin American ALDL Connector
    
       __________###__________
      | F | E | D | C | B | A |
       ---+---+---+---+---+--- 
    __|_G_|_H_|_J_|_K_|_L_|_M_|__

    (Facing the dashboard-mounted end)

The serial data lines are pins E and M. Older cars used pin E at 160 baud. Newer
(early 90's until '95?) used pin M at 8192 baud. Some cars also had non-engine
systems utilizing other pins for serial data (for example, the ABS system
sometimes used pin H). Pin A is always ground.

The 8192 baud pin M signal (the one my '94 Suburban has) is bidirectional. It's
much like the UART found on many microcontrollers, except both TX and RX are on
the same line. When inactive, the line is held at 5V. Either end may pull the
line to ground to send a start bit and begin transmitting. The common 8-N-1 
format is used. Note that some cars (not my Suburban) require a 10k resistor
between pin B and pin A for serial transmission to be enabled.

To make matters a bit more complicated, besides different physical pins and baud
rates, different cars use different versions of the data stream protocol. There
are about 300 versions, depending on the make, model year, engine type, etc.
Furthermore, it seems some cars may have multiple streams for different parts
(perhaps one for the engine and one for the transmission, for example).
Documentation on which streams go with which car can be found online. The best I
have found is in the "AlDlstuff.rar" archive, from [this forum post][1].
Each "Axxx.DS" file documents one data stream format. The other files in the
archive describe general details on the serial protocol (e.g. voltages) and
which data stream goes with what car.

As it so happens, an FT232RL chip can be made to successfully communicate
with the ECM (at least the ones using the 8192 baud pin M signal) by wiring its
RX and TX lines together to pin M on the ALDL connector and tying its ground to
pin A. Boards like the [FTDI Friend][3] from Adafruit (be sure to solder the 5V
jumper and cut the 3.3V one) or [FTDI Basic 5V][4] from SparkFun have these
signals conveniently broken out, making it relatively easy to fashion an
inexpensive sort of USB ALDL cable. Prebuilt USB cables are also readily
available for purchase online, but tend to be fairly expensive (maybe $60).

There are already [Windows programs][5] out there that can make use of such a
setup to gather and log real-time data from the engine, but most, if not all,
are closed source and not available for other OS's. Hence this program: an
effort to produce open-source code that can parse the ALDL data stream.

[1]: http://www.mp3car.com/engine-management-obd-ii-engine-diagnostics-etc/104591-gm-aldl-protocols-description-from-gm-guy.html) "ALDL Data Streams"
[2]: http://en.wikipedia.org/wiki/Regular_Production_Option "Regular Production Option"
[3]: https://www.adafruit.com/products/284 "FTDI Friend"
[4]: https://www.sparkfun.com/products/9716 "FTDI Basic 5V"
[5]: http://aldlcable.com/diagnosticsoftware.asp "ALDL Software"

------------------------------------------------------------------------

Copyright © 2014 Dominick C. Pastore
