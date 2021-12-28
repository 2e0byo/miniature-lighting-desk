A circuit diagram is provided, since it’s a good idea to have such
things:

![schematic](../schematic.svg)

Note that the voltage regulator is not shown: this is a module, bought from
Amazon or Ebay ages ago, and is switch-mode (so it shouldn’t get too hot). I
have no idea of its specifications, but the worst case scenario&#x2014;300mA on
each channel, or \(8\times300 = 2.4A\) is probably pushing it.

The core of the hardware is a PIC18f4550 microcontroller, a small one-chip
computer running at 12MHz (compare that to your laptop, running probably at
several GHz). It has integrated USB hardware, and is running the
[Pinguino](https://pinguino.cc/) bootloader, which allows updating the firmware
over usb.

The circuit is simplicity itself.  The outputs from the PIC are either
at 0v or at 5v.  They are connected to 2n7000 mosfets, which are in
this usage like switches, which turn on if 5v is applied to the gate
and off if 0v is applied.  They don’t like handling more than a few
hundred mA, though, so bigger mosfet switches might be needed if you
wanted to switch more.
