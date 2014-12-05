ALDL Echo
=========

A simple Python program to echo data read from the ALDL port on old GM cars. 

This program was written specifically for my Suburban (a 1994 1/2 model with the
L05 engine (5.7L V8 TBI, VIN=K) and 4L60E transmission). Out of the box, only
cars very similar to it will be supported. That being said, as long as your car
uses the 8192 baud variant of ALDL, it should take little effort to add support
for it. See "Data Streams" for how to do that. If your car only uses the 160
baud variant of ALDL, unfortunately, this program cannot easily support your car
as is (though with more effort, and the will to dive into a bit of programming, 
it's still very possible. The documentation is here).

If none of the above makes sense to you, try reading the rest of this README,
which explains more about ALDL.

Even if all of the above makes sense to you, you should read the rest of this
README. It contains useful information.

Prerequisites and Limitations
-----------------------------

This program requires Python 3 and PySerial.

Note that this program requires at least one data stream definition file that
is appropriate for your car in order to work properly. Defintions are already
included for the Suburban I wrote this for (A217 and A218). If your car uses a
data stream other than A217 or A218, you'll need to create a definition file
for it. See "Data Streams" for more information.

Data Streams
------------

A Quick Background
------------------

**Disclaimer: My area of expertise is computer science, not cars. All
information in this README is the result of copious Googling. I cannot be held
responsible for any injury, damage, or loss of life or property that results
from the contents of this file, or mistakes it may contain.**

ECM's for older GM cars (pre OBD-II) mostly used the same ALDL connector shape,
but different cars made use of different pins within the connector.

       __________###__________
      | F | E | D | C | B | A |
       ---+---+---+---+---+--- 
    __|_G_|_H_|_J_|_K_|_L_|_M_|__

    (Facing the dashboard-mounted connector)

The serial data lines are pins E and M. Older cars used pin E at 160 baud. Newer
(early 90's until '96?) used pin M at 8192 baud. Pin A is always ground.

The 8192 baud pin M signal (the one my '94 Suburban has) is bidirectional. It's
much like the UART found on many microcontrollers, except both TX and RX are on
the same line. When inactive, the line is held at 5V. Either end may pull the
line to ground to send a start bit and begin transmitting. The common 8-N-1 
format is used. Note that some cars (not my Suburban) require a 10k resistor
between pin B and pin A for serial transmission to be enabled.

To make matters a bit more complicated, besides different physical pins and baud
rates, different cars use different versions of the data stream protocol. There
are some 200-something versions, depending on the make, model year, engine type,
etc. Furthermore, it seems some cars may have multiple streams for different
parts (perhaps one for the engine and one for the transmission, for example).
Documentation on which streams go with which car can be found online. The best I
have found is in the "ALDLstuff.rar" archive, from [this forum post][1].
Each "Axxx.DS" file documents one data stream format. The other files in the
archive describe general details on the serial protocol (e.g. voltages) and
which data stream goes with what car. It seems my Suburban uses streams A217 and
A218.

As it so happens, an FT232RL chip can be made to successfully communicate
with the ECM by wiring its RX and TX lines together to pin M on the ALDL
connector and tying its ground to pin A. Boards like the [FTDI Friend][2] from
Adafruit (be sure to solder the 5V jumper and cut the 3.3V one) or [FTDI Basic 5V][3] from SparkFun have these signals conveniently broken out,
making it relatively easy to fashion an inexpensive sort of USB ALDL cable.
Prebuilt USB cables are also readily available for purchase online, but tend to
be fairly expensive (maybe $60).

There are already [Windows programs][4] out there that can make use of such a setup
to gather and log real-time data from the engine, but most, if not all, are
closed source and not available for other OS's. Hence this program: an effort to
produce open-source code that can parse the ALDL data stream.

[1]: http://www.mp3car.com/engine-management-obd-ii-engine-diagnostics-etc/104591-gm-aldl-protocols-description-from-gm-guy.html) "ALDL Data Streams"
[2]: https://www.adafruit.com/products/284 "FTDI Friend"
[3]: https://www.sparkfun.com/products/9716 "FTDI Basic 5V"
[4]: http://aldlcable.com/diagnosticsoftware.asp "ALDL Software"

------------------------------------------------------------------------

Copyright © 2014 Dominick C. Pastore
