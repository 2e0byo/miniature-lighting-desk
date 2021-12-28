This is a lighting controller, exactly like lighting controllers in a
theatre.  It has eight channels, numbered 0-7 (since I am a lazy
programmer, and computers start counting at 0).  These can be set
between off (0) and full on (256---no, that’s not a typo, see
[4](#orgc780223) to find out why).  At 0 the corresponding pair of
output terminals has no voltage accross it.  At 256 it has the voltage
displayed on the little display accross it.  This voltage can be
adjusted by turning the knob, but it applies to all channels (so you
can only really control lamps or outputs which want the same voltage
accross them, although see [3.2.1](#org0329802) below.)

You can drive standard filament lamps&#x2014;the kind you’ve used
before&#x2014;directly.  You can also drive some LEDs directly, and others
with an appropriate current limiting resistor (see [3.1.1](#org26e2c7d) below).  You
could also theoretically drive any other resistive sink, or indeed an
inductive sink like a motor, as protection diodes are fitted.

The controller (the hardware) is controlled over USB, by a computer
running software.  It ships with two demo programs: a graphical
program consisting of eight sliders which can be used to control the
channels, exactly like a ‘real’ theatre controller, together with the
ability to load and save states, for use as presets, and a
demonstration of scripting the controller, which is discussed in the
section [5](#orge444fa1).

The controller is powered by an external SMPSU, which sometimes gets a
little warm in operation, but which is capable of running for extended
periods wtihout overheating.  The SMPSU can supply up to 30v, but is
set to supply 15v at the moment, which is probably all you want to
handle.  Each channel can provide around 300mA, which should be enough
for all realistic uses.
