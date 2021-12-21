from tkinter import Tk, Canvas
from unittest.mock import MagicMock
from PIL import Image, ImageTk
from multiprocessing import Queue
from queue import Empty


from .server import Server

COLORS = ("red", "orange", "yellow", "green", "blue", "indigo", "black", "gold")


class MockChannel:
    def __init__(self, *args):
        self.val = 0

    def get_brightness(self):
        return self.val

    def set_brightness(self, val):
        self.val = max(0, min(255, val))


class MockServer(Server):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, channel=MockChannel, controller=MagicMock)


class MockGuiServer(Server):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, channel=MockChannel, controller=MagicMock)
        self.queue = Queue()
        root = Tk()
        root.title("Mock Lighting Controller")
        self.root = root
        channels = kwargs.get("channels", 8)
        canvas = Canvas(root, width=channels * 50 + 2, height=62)
        self.images = [
            [self.create_image(brightness, fill) for brightness in range(256)]
            for fill in COLORS[:channels]
        ]
        self._current_images = [None] * channels
        canvas.pack()
        self.canvas = canvas
        for i in range(channels):
            self.set_brightness(i, 100)

    def set_brightness(self, channel: int, val: int):
        val = max(0, min(val, 255))
        super().set_brightness(channel, val)
        self.queue.put((channel, val))

    def _set_brightness(self, channel: int, val: int):
        self.set_image_brightness(
            1 + 50 * channel, 1, (1 + 50 * channel) + 40, 60, val, channel
        )

    def set_image_brightness(self, x1, y1, x2, y2, brightness, channel):
        self._logger.debug(f"Setting channel {channel} to brightness {brightness}")
        self._current_images[channel] = ImageTk.PhotoImage(
            self.images[channel][brightness]
        )
        self.canvas.create_image(
            x1, y1, image=self._current_images[channel], anchor="nw"
        )
        self.canvas.create_rectangle(x1, y1, x2, y2)

    def create_image(self, brightness, fill):
        fill = self.root.winfo_rgb(fill) + (brightness,)
        return Image.new("RGBA", (40, 60), fill)

    def get_changes(self):
        try:
            self._set_brightness(*self.queue.get(0))
        except Empty:
            pass

        self.root.after(1, self.get_changes)

    def __enter__(self):
        super().__enter__()
        self.root.after(100, self.get_changes)
        self.root.mainloop()


if __name__ == "__main__":
    server = MockGuiServer()
    with server:
        input()
