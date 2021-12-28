# Hardware #




## Mains Dimming ##

It would be possible to add a trailing-edge mosfet dimmer to functions
like a standard dimmer switch.  Contact me if you want to do this.




## Multiple Voltages ##

It would be possible to add another voltage regulator inside to drive
some channels, so that they could be controlled in, say, two groups.
But if you need to do this a lot (and can’t use the trick above), it
would be better to build another controller, which would probably be
about as much work.




## Parallel outputs? ##

What if you want more current? You *can* theoretically run two outputs
in parallel, as they switch at the same time, but you should be
careful to make sure they really *do* have the same value all the
time.  This would be quite easy if we were scripting, we could do
something like:

```python
def set_parallel_output(brightness):
    output_one.set_brightness(brightness)
    output_two.set_brightness(brightness)

set_parallel_output(128)
```

where `output_one` and `output_two` are already defined, like
`red_lamp` etc in the scripting section.  Alternatively you could have
one slider control multiple outputs.  Have a go at implementing this
if you want it, but ask me if you need help.

Paralleling more than two outputs is probably a bad idea.  What are
you tring to drive which needs so much current?  It would be possible
(and easier) just to modify the hardware to use a beefier MOSFET.
They are very cheap.




## A nicer case! ##

Yes, the case is really not of the best.  It was made in the freezing
cold in a great hurry.  Since you now have a 3D printer, perhaps you
would like to make a better one?



