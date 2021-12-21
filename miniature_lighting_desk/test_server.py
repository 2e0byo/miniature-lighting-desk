from tkinter import Tk, Canvas
from unittest.mock import MagicMock
from PIL import Image, ImageTk
from multiprocessing import Queue
from queue import Empty


from .server import Server

COLORS = ("red", "orange", "yellow", "green", "blue", "indigo", "violet", "brown")


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
        self.images = [None] * channels
        canvas.pack()
        self.canvas = canvas
        for i in range(channels):
            self.set_brightness(i, 100)

    def set_brightness(self, channel: int, val: int):
        super().set_brightness(channel, val)
        self.queue.put((channel, val))

    def _set_brightness(self, channel: int, val: int):
        self.create_rectangle(
            1 + 50 * channel, 1, (1 + 50 * channel) + 40, 60, val, channel
        )

    def create_rectangle(self, x1, y1, x2, y2, brightness, channel):
        fill = COLORS[channel]
        brightness = max(1, brightness)
        self._logger.debug(f"Creating rectangle of brightness {brightness}")
        fill = self.root.winfo_rgb(fill) + (brightness,)
        image = Image.new("RGBA", (x2 - x1, y2 - y1), fill)
        first = not self.images[channel]
        first = True
        self.images[channel] = ImageTk.PhotoImage(image)
        if first:
            self.canvas.create_image(x1, y1, image=self.images[channel], anchor="nw")
            self.canvas.create_rectangle(x1, y1, x2, y2)

    def get_changes(self):
        try:
            self._set_brightness(*self.queue.get(0))
        except Empty:
            pass

        self.root.after(10, self.get_changes)

    def __enter__(self):
        super().__enter__()
        self.root.after(100, self.get_changes)
        self.root.mainloop()


if __name__ == "__main__":
    server = MockGuiServer()
    with server:
        input()
