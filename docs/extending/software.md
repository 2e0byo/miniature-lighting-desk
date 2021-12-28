## Example: a ‘zero’ button ##

Take a look at `gui.py`.  First open it and then save it under a new
name, so we can go back and retrieve the original if need be.  Call
the new name `gui2.py`.

We are going to add a ‘zero’ button which zeros every channel.  For
this we need a function which zeros channels.  After the lines

```python
for i in range(8):
    channels.append(ChannelSlider(i, master))
```

add the following:

```python
def zero():
    """Zero everything."""
    for channel in channels:
        channel.set(0)
```

Now we need a button to call this function.  After:

```python
save_button = Button(master, text="Save State", command=save_state)
save_button.grid(column=8 - 3, row=3)
```

add:

```python
zero_button = Button(master, text="Zero", command=zero)
zero_button.grid(column=0, row=3)
```

save it and run.  Now you have a zero button.

1.  Excercise: a ‘max’ button

    Can you implemenet another button, to set every channel to the
    maximum?  Hint: look at the specifications above (or the source code
    for the HAL) to find out what the maximum *is*, numerically.

2.  Harder Excercise: a master slider

    What if you wanted a &rsquo;master&rsquo; slider, which let you set the brightness
    of *all* the channels?
    
    Assume that you want the slider to function as a multiplier (i.e. it
    doesn&rsquo;t actually move the other channels, but they get multiplier by
    it before the controller is set.)
    
    This will require editing the definition of `ChannelSlider`.  I
    personally would just edit the `set` method.  Perhaps something like:

    ```python
        def set(self, val):
            self.channel.set_brightness(int(float(val) * master_slider.get() / 100))
            self.slider.set(int(float(val)))
    ```

    and then define `master slider` as something like:

    ```python
        master_slider = Scale(master, from_=100, to=0, length=300, orient="horizontal")
    ```

    and place it below the other sliders.
    
    Get in touch if you try this and have problems: I&rsquo;ve only provided the
    outline here.
