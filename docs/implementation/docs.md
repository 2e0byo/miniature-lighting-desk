It’s bad practice to ship code without documentation aimed at other
coders.  Thus this section is technical.

## Overview HAL

The controller interacted with using a `Controller()` object provided by
the hal.  Only the asyncio hal is developed.  The expectation is that
code will not be primarily asyncio-based, so the Controller() object
starts its own asyncio thread and manages it.  Communication is by
Bulk transfers, and is not awaitable (since AFAIK pyusb isn’t
awaitable yet).  In any case it’s so fast we don’t need to worry.  In
point of fact we merely await delays in various fade steps.

On initialisation the Controller object starts an asyncio thread,
grabs the usb device (specifically: the first it finds, so if we need
to control multiple devices we’ll have to edit it to accept a bus/dev
manually) and then waits.  It provides a `submit_async` method which
must be used to run awaitables, returning a futures.

The `Channel()` object represents a distinct channel on the
controller.  It takes a `Controller` object as an argument.  On
initialisation it queries the hardware for the current channel value.
It then keeps track of this locally, except when an asynchronous fade
is cancelled, when it queries again to discover what has actually
happend.  It provides methods to get and set brightness, either as a
raw number or a percentage (float between 0.0 and 1.0), and
asynchronous `fade_on` and `fade_off` methods, as well as
`cancel_fade` to cancel a running fade.  Note that precision in timing
is not promised with these methods, and userspace fading should be
done where precision matters.  Note also that the `Channel()` class is
wholly synchronous: it merely submits tasks to the `Controller()`
which in turn submits them to its `asyncio` thread.  If multiple
controllers are desired, the code should probably be extended to
enable sharing this asyncio event loop.




## Overview GUI

I am not a gui programmer.  This is a very simple gui in tkinter.  It
uses ttk (Themed Tkinter) for slightly better-looking graphics.

A `ChannelSlider` class both creates the `tkinter.ttk.Scale` object
which draws the slider and the `async_hal.Channel` object which
controls it.  Then we have a getter and setter.  The getter
just returns the slider value; the setter sets both the `Channel` by
calling `set_brightness` and the slider.  We cast to `float` and then
`int` since ttk returns float strings but tk int strings (at least in
my testing), and to show how it’s done.

State is handled with single line csvs consisting of nothing more than
than the channel values as ints.




## Further details

See the code, it’s very simple.


