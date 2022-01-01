There, that was easy!   Let’s take another look at demo.py.  Here is
the beginning again:

```python
from math import pi, sin
from time import sleep

import async_hal as hal  # hal = Hardware Abstraction Layer

lighting_controller = hal.Controller()
red_lamp = hal.Channel(lighting_controller, 7)
white_lamp = hal.Channel(lighting_controller, 0)

# set brightness in background
red_lamp.set_brightness(0)
```

Anything after a `#` is a ‘comment’, i.e. it’s for you, not the
computer, which just ignores it.  The first two lines ‘import’ things
from ‘libraries’&#x2014;i.e. ‘other code’.  The ‘math’ library is built
into Python, and provides mathematical functions and constants
(obviously).  The time library, amazingly enough, provides things to
do with time, and is likewise built in.

`async_hal` is a library I wrote, distributed with the demo.  It’s
called *async* hal as I first wrote a *synchronous* hal, but then
abandoned it as the async one is much better.  (It sends the usb
requests in the background.) A hal is a Hardware Abstraction Layer,
i.e. something which does the hard work of talking to the hardware.

This hal provides a *class*, which is a way of assigning
representations to objects&#x2014;in this case the physical object in front
of you.  From your point of view it’s just a function which returns an
‘object’, which we call `lighting_controller`.

Once we have an object representing the controller, we make an object
for each of the channels:

```python
red_lamp = hal.Channel(lighting_controller, 7)
```

The `Channel` class in the hall represents a channel *on a
controller*.  So you have to tell it *which* controller.  We only have
one: the one we just made a representation of!  We also need to know
which channel on the ‘hardware’ correlates with this channel on the
‘software’: here’s it’s number 7.

This is conceptually quite complicated, but very easy in practice.
For instance, let’s make a Channel object for the third channel.
Remember we start counting at 0:

```python
third_channel = hal.Channel(lighting_controller, 2)
```

We could have called it something else.  Perhaps we have a street lamp
attached to channel 3:

```python
street_lamp = hal.Channel(lighting_controller, 3)
```

The *name* we give it is just a variable.  It can contain pretty much
anything, if we stick to the alphabet and the underscore (`_`).

Each channel object has few methods.  Here they are:

```python
white_lamp.set_brightness(128)
white_lamp.set_percent_brightness(0.1)
white_lamp.get_brightness()
white_lamp.get_percent_brightness()
white_lamp.fade_on(1)
# wait a second before typing
white_lamp.fade_off(100)
white_lamp.cancel_fade()
```

Additionally, when we initialise a Channel object it queries the
controller for the current setting on that channel, so the
software never gets out of sync with the hardware.  (This is used in
the gui to make the sliders all appear at the right place.)

## Going further

Read the rest of `demo.py`.  Can you see how it works?



