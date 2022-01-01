Connect to Computer.  Plug in power supply.  Set correct voltage.
Attach lamps etc. to each channel.  Load software.

If you have any trouble connecting to the controller (after installing
the software), turn it off and on again whilst still plugged in to the
computer.

## Connnections

Connections are by screw-terminal (chocolate block). Try not to sort the outputs
(for instance by stripping too much insulation off the end of the wires).

## LEDs

LEDs can be driven, but need more care than filament lamps.  In
general LEDs should be driven in constant *current* mode, not constant
*voltage*.  This is because, although they have a constant *threshold*
voltage (the voltage, or rather narrow range of voltages, at which
they start glowing), they represent a very low-resistance load above
this voltage (effectively a short circuit).  Thus as the voltage
climbs they absorb a *lot* of power and catch fire.  This is inverse
to the behaviour of a filament lamp, which is effectively a short
circuit when connected, but rapidly gains in resistance as it heats
up, and so consumes less and less power until it reaches a stable
state.

If driven with a constant *current* of the right amount, LEDs will
operate at the correct voltage.  Thus, when a given current is put
through them, they have a given, fixed voltage accross them.  We can
take advantage of this to drive them with a series resistor.
According to Ohm’s Law, \(V=IR\), so \(I=V/R\).  V is fixed, but we can
change R. For an LED with a working voltage of 2.5v at 10mA (or
0.01A), with the controller set to 6V, the voltage accross the
resistor will be \(6-2.5=3.5\), and the resistor needs to be \(R=V/I =
3.5/0.01 = 350 \Omega\).  They don’t make 350 ohm resistors, so pick the
next largest: 390.  This value is rather high, but I made these
numbers up.

What about the christmas lights?  They have no resistor at all!
Another set I bought *did* use a series resistor, but in this case the
manufacturer has paralleled all the LEDs, and matched them so well
that they share current equally.  (It’s quite easy when you make them
in the hundreds of thousands).  Thus they represent one big LED.  This
big LED sinks a lot more current than a single LED&#x2014;most only sink a
few mA and can be blown up by a few tens of mA.  These all sink about
30mA.  Moreover, they have a working voltage of 3v.  If we go slightly
above the working voltage with a standard LED we supply a *lot* more
current than it can take.  But if we do so with these, we have more
room for error.  Also, we actually *do* have a series resistor&#x2014;the
controller’s internal resistance!  I estimate this to be in the order
of several ohms, perhaps even 10 ohms.  It is largely caused by the
switiching MOSFETs on-resistance (see [Hardware](../implementation/hardware.md)).


### TL;DR

If this sounds like a lot maths: most leds can be driven with a 150&Omega;
resistor from 5v without any problems.  Note that they only conduct
one way.  If you want to drive from a higher voltage, scale the
resistor appropriately.  The supplied red LED is a ‘high brightness’
kind (i.e. it turns on early) and is in series with a 1k (1,000&Omega;)
resistor, which makes it safe at least up to 15v, but it still turns
on appreciably at 3!  I wanted it to be hard for you to blow it up.

Christmas lights can generally be driven as in the original.  If there
is no series resistor, you don’t need one either.  If there is a
series resistor, you can simply cut it out and use it, setting the
controller to the same voltage.



## Differing Voltages

What do you do if you want to control two lamps of different voltage
ratings at the same time?  You *might* think that you could use e.g. a
6v and a 12v lamp at the same time, by never taking the 6v channel
above 50%.  And so you can&#x2014;with a caveat: the controller uses PWM
(Pulse Width Modulation) to adjust the effective output voltages,
i.e. it switches on and off very fast.  So the lamps need to be able
to survive a pulse at the maximum brightness.  Filament lamps are fine
about this, and LEDs often are.  Note that in this case the resolution
of the lower lamp is reduced&#x2014;i.e. if you have a 6V light never
driven above 50%, there are only 128 steps, not 256.



## Limitations

The hardware has a latency: it cannot switch instantaneously.  This is
likely not a problem, but could be if you try very high-frame rate
filming.  It is possible the switching frequency could create aliasing
effects with the shutter speed, although I highly doubt it.  In this
case contact about changing it.


