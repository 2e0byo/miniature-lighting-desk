"""
A very basic gui to let you drag some sliders around.

Can you tell I'm not at all a gui programmer?
"""
import asyncio
import csv
from logging import getLogger
from tkinter import Tk
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.ttk import Button, Label, Scale
from wampy.peers import Client
from wampy.roles.subscriber import subscribe


logger = getLogger(__name__)

root = Tk()
root.title("Minature Lighting Controller")

channels = []


class DeskClient(Client):
    @subscribe(topic="controller.statechange")
    def handler(self, vals, **kwargs):
        for channel, val in zip(channels, vals):
            asyncio.create_task(channel.set_soon(val))
        return True


client = DeskClient(
    url="ws://wamp.2e0byo.co.uk:3227/ws",
    realm="miniature-lighting-controller",
).__enter__()


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
        self.root = root
        self.skip = False
        self.slider.grid(column=channel, row=0, padx=10)
        self.label = Label(root, text=f"Channel {channel}")
        self.label.grid(column=channel, row=1, pady=10)
        self.slider.set(client.rpc.get_brightness(channel=channel))

    def _slider_changed(self, val):
        if self.skip:
            self.skip = False
            return
        val = int(float(val))
        self._set(val)

    def set(self, val):
        val = int(float(val))
        self._set(val)
        self.slider.set(val)

    def _set(self, val):
        client.rpc.set_brightness(channel=self.channel, val=val)

    def slider_set(self, val):
        print("Setting slider")
        self.skip = True
        self.slider.set(val)

    async def set_soon(self, val):
        if self.slider.get() != val:
            # self.slider.set(val)
            await asyncio.sleep(0.1)
            self.slider_set(val)

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
    channels.append(ChannelSlider(i, root))

load_button = Button(root, text="Load State", command=load_state)
load_button.grid(column=2, row=3)

save_button = Button(root, text="Save State", command=save_state)
save_button.grid(column=8 - 3, row=3)


async def mainloop():
    while True:
        root.update()
        await asyncio.sleep(0.01)


asyncio.run(mainloop())
