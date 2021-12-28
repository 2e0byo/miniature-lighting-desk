The easiest way to start off is to open and edit the demo I have
provided.  So open `demo.py` in IDLE (Python’s inbuilt editor) and
let’s have a look.  It begins like this:

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

Copy this much into a new file called `quick_start.py` and save it 
*in the same place you found demo.py*&#x2014;probably just on the usb
stick.  Then change the last line to read:

```python
red_lamp.set_brightness(128)
```

and press ‘run’.  There.  You wrote your first controlling script.

The window which popped up when you pressed ‘run’ should still be
open.  Type into it:

```python
red_lamp.set_percent_brightness(0.75)
```

and observe what happens.  Then press Ctrl-P: the line you just typed
should appear.  Change the 0.75 to 0.25.  Press enter, and observe
what happens.  Press Ctrl-P, then press it again: do you see how it
lets you go ‘back’ through your input?  Replacing the ‘p’ with an ‘n’
lets you go ‘forward’.  In this way you can do less typing.

Try:

```python
white_lamp.fade_on()
```

Notice how the white lamps takes around a second to fade on, but the
code returns immediately: it’s fading in the background
(‘asynchronously’).  This may or may not be what you want, depending
on what you’re trying to do.
