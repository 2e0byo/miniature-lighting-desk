"""
A very basic gui to let you drag some sliders around.

Can you tell I'm not at all a gui programmer?
"""
import csv
from tkinter import Tk
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.ttk import Button, Label, Scale

from . import async_hal as hal


class ChannelSlider:
    """Channel Slider."""

    def __init__(self, controller: hal.ControllerABC, channel, root):
        self.channel = hal.Channel(controller, channel)
        self.slider = Scale(
            root,
            from_=controller.max_brightness,
            to=0,
            command=self._slider_changed,
            length=300,
            orient="vertical",
        )
        self.slider.grid(column=channel, row=0, padx=10)
        self.label = Label(root, text=f"Channel {channel}")
        self.label.grid(column=channel, row=1, pady=10)
        self.slider.set(self.channel.get_brightness())

    def _slider_changed(self, val):
        self.channel.set_brightness(int(float(val)))

    def set(self, val):
        self.channel.set_brightness(int(float(val)))
        self.slider.set(int(float(val)))

    def get(self):
        return self.slider.get()


class App:
    def __init__(self, channels: int, controller: hal.ControllerABC):
        self.root = Tk()
        self.root.title("Miniature Lighting Controller")

        self.lighting_controller = controller
        self.channels = []

        for i in range(channels):
            self.channels.append(ChannelSlider(self.lighting_controller, i, self.root))

        load_button = Button(self.root, text="Load State", command=self.load_state)
        load_button.grid(column=2, row=3)

        save_button = Button(self.root, text="Save State", command=self.save_state)
        save_button.grid(column=8 - 3, row=3)

    def __call__(self):
        self.root.mainloop()

    def load_state(self):
        """Load a previous state from a .csv."""
        states = []
        with askopenfile(
            filetypes=[("State CSV", "*.csv")],
            defaultextension=".csv",
        ) as f:
            reader = csv.reader(f)
            for row in reader:
                states = row  # we just take the last row

        if len(states) != 8:
            print("Input file is corrupt.")  # we should use a dialog box for this.

        try:
            for i, state in enumerate(states):
                self.channels[i].set(state)
        except Exception as e:
            print(f"Error loading state: {e}")

    def save_state(self):
        """Save a state to a single-line csv."""
        try:
            with asksaveasfile(
                filetypes=[("State CSV", "*.csv")], defaultextension=".csv"
            ) as f:
                writer = csv.writer(f)
                writer.writerow([channel.get() for channel in self.channels])
        except Exception as e:
            print(f"Error: {e}")


def main(controller: hal.ControllerABC):
    app = App(channels=controller.no_channels, controller=controller)
    app()
