The code is somewhat tricky to read, as it is hacked
together from the Pinguino original (Pinguino uses simple ‘sketches’
to generate a large number of files which are then compiled to produce
the machine-code running on the microcontroller), but the core routine
is simple enough:
```c
receivedbyte = BULK_read(buffer); /* returns index of end */

unsigned char channel;
unsigned long duty;
inputPTR = buffer;

if (!strncmp(inputPTR, "s", 1)) {

  channel = ascii_to_decimal(inputPTR[1]);

  duty = 100* ascii_to_decimal(inputPTR[2]) + 
   10*ascii_to_decimal(inputPTR[3]) + 
   ascii_to_decimal(inputPTR[4]);

  if (duty>256) duty = 256;
  newDuties[channel] = duty;
  BULK_printf("Set channel %u to %u", channel, duty);
}
else if (!strncmp(inputPTR, "g", 1)) {

  BULK_printf("Channel %u is %u", channel, newDuties[channel]);
}
```

This is in C, which is harder than python, at any rate to read as a
non-coder.  I’ve also cut all the error detection and a few other
things: see `pic/user.c` if you want to see the whole thing.

This code, which runs in a loop which otherwise sits around waiting
for data, looks to see if the input (obtained by calling `BULK_read`)
starts with ‘s’, and if so, Sets the given channel to the value given
(after converting it from ascii to decimal, i.e. from a string like
`"4"` to the number `4`), makes sure it’s no bigger than 256, and then
writes the new value to an array, `newDuties`.  This array is checked
by the interrupt routine which happens very quickly, thousands of
times a second, and which, in simplified form, looks like this:
```c
++count;
unsigned char latch = LATD;
if (count == 0) {
  latch = 0;
  for (unsigned char i=0; i<8; i++) {
    duties[i] = newDuties[i];
  }
}
for (unsigned char i=0; i<8; i++) {
  if (duties[i] == count) latch |= (0x1 << i);
}
LATD = latch;
```

Firstly we update a variable ‘count’.  This variable is defined
elsewhere as being only 8 bits long, i.e. the maximum value it can
store is \(2^8 -1 = 255\).  If we try to add one to it when it stores
255, it will ‘roll over’ to 0 again, which is handy.  So we have 255
steps.

Then we set a temporary variable to the value of `LATD`, which is the
value of the 8-bit output port controlling the channels, or, in simple
terms, the value of the channels.  So if LATD is ‘11110000’, channels
0-3 will be off, and 4-7 will be on (note: numbers are right-to-left
when written down!).  We store this in a variable, since writing to
LATD *changes the actual outputs*, which is pretty nifty.  

Then, only if count is ‘0’, we set the temporary ‘latch’ variable to 0
(i.e. all channels off), and set the ‘duties’ array to be the same as
the ‘newduties’ we modified earlier.  We don’t modify ‘duties’
directly to avoid flickering, which would happen if we updated
‘duties’ halfway through a cycle.

Then we go through each channel in turn, and if the value of `count` is the same
as the value of `duties[i]` (that is: the `ith` value in the array `duties`)
turn the `ith` channel on. (This is what the weird thing with the `<<` does: it
sets the `ith` bit of our ‘latch’ variable.) Note that we start by turning
outputs *off*, and turn them *on* when we get to the value transmitted. So to
turn a channel *off* you send 256, which is 1 more than 255 and so will *never*
cause it to be turned on. This is the reason for the weird resolution&#x2014;255
steps - 1 to turn it fully off = 256 steps. The HAL turns this round for you, so
`set_brightness(256)` is full on and `set_brightness(0)` is off, as you would
expect. This is another reason to use a HAL.

Then, finally, we set the real output to be whatever we have assembled
in our temporary `latch` variable.











