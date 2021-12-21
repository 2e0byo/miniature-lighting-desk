"""
A very basic gui to let you drag some sliders around.

Can you tell I'm not at all a gui programmer?
"""
import csv
from tkinter import Tk, mainloop
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.ttk import Button, Label, Scale
from sys import argv

import jsonrpclib

from .server import Server

master = Tk()
master.title("Minature Lighting Controller")

channels = []

if len(argv) > 1:
    url = f"http://localhost:{argv[1]}"
    server = jsonrpclib.Server(url)
    server.sync()

else:
    try:
        server = jsonrpclib.Server(f"http://localhost:{Server.DEFAULT_PORT}")
        server.sync()
    except Exception:
        s = Server()
        server = jsonrpclib.Server(f"http://localhost:{s.port}")


class ChannelSlider:
    """Channel Slider."""

    def __init__(self, channel, root):
        self.channel = channel
        self.slider = Scale(
            root,
            from_=256,
            to=0,
            command=self._slider_changed,
            length=300,
            orient="vertical",
        )
        self.slider.grid(column=channel, row=0, padx=10)
        self.label = Label(master, text=f"Channel {channel}")
        self.label.grid(column=channel, row=1, pady=10)
        self.slider.set(server.get_brightness(channel))

    def _slider_changed(self, val):
        server.set_brightness(self.channel, int(float(val)))

    def set(self, val):
        server.set_brightness(self.channel, int(float(val)))
        self.slider.set(int(float(val)))

    def get(self):
        return self.slider.get()


def slider_changed(event):
    """Set channel when slider changes."""
    print(event)


def load_state():
    """Load a previous state from a .csv."""
    states = []
    with askopenfile(filetypes=[("State CSV", "*.csv")], defaultextension=".csv") as f:
        reader = csv.reader(f)
        for row in reader:
            states = row  # we just take the last row

    if len(states) != 8:
        print("Input file is corrupt.")  # we should use a dialog box for this.

    try:
        for i, state in enumerate(states):
            channels[i].set(state)
    except Exception as e:
        print(f"Error: {e}")


def save_state():
    """Save a state to a single-line csv."""
    try:
        with asksaveasfile(
            filetypes=[("State CSV", "*.csv")], defaultextension=".csv"
        ) as f:
            writer = csv.writer(f)
            writer.writerow([channel.get() for channel in channels])
    except Exception as e:
        print(f"Error: {e}")


for i in range(8):
    channels.append(ChannelSlider(i, master))

load_button = Button(master, text="Load State", command=load_state)
load_button.grid(column=2, row=3)

save_button = Button(master, text="Save State", command=save_state)
save_button.grid(column=8 - 3, row=3)

mainloop()
