ALDL Echo
=========

A simple python program to echo data read from the ALDL port of an old Suburban.

The Suburban this was written for is a 1994 1/2 ton model with the L05 engine
(5.7L V8 TBI, VIN=K) and 4L60E transmission. As far as I can tell, it uses data
streams A217 and A218.

A Quick Background
------------------

**Disclaimer: My area of expertise is computer science, not cars. All
information that follows is the result of copious Googling. I cannot be held
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
have found is in the "ALDLstuff.rar" archive, from [this forum post](http://www.mp3car.com/engine-management-obd-ii-engine-diagnostics-etc/104591-gm-aldl-protocols-description-from-gm-guy.html).
Each "Axxx.DS" file documents one data stream format. The other files in the
archive describe general details on the serial protocol (e.g. voltages) and
which data stream goes with what car. It seems my Suburban uses streams A217 and
A218.

As it so happens, an FT232RL chip can be made to successfully communicate
with the ECM by wiring its RX and TX lines together to pin M on the ALDL
connector and tying its ground to pin A. Boards like the FTDI Friend from
Adafruit or FTDI Basic from SparkFun have these signals conveniently broken out,
making it relatively easy to fashion an inexpensive sort of USB ALDL cable.
Prebuilt USB cables are also readily available for purchase online, but tend to
be fairly expensive (maybe $60).

There are already Windows programs out there that can make use of such a setup
to gather and log real-time data from the engine, but most, if not all, are
closed source and not available for other OS's. Hence this program: an effort to
produce open-source code that can parse the ALDL data stream.

------------------------------------------------------------------------

Copyright © 2014 Dominick C. Pastore
