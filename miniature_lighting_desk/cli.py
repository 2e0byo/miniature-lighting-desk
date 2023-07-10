import os
from enum import Enum
from getpass import getpass
from typing import Literal

import typer

from . import server
from .async_hal import controllers
from .local_gui import main as gui

app = typer.Typer()

# Typer provides proper hinting like this
_Controller = Enum("_Controller", {k: k for k in controllers.keys()})


class Controller(str, Enum):
    pinguino = "PinguinoController"
    mock = "MockController"


@app.command(help="Run local gui.")
def local_gui(
    controller: _Controller = _Controller.pinguino,
):
    controller = controllers[controller.value]()
    gui(controller)


@app.command(help="Run backend for web gui.")
def backend(
    controller: _Controller = _Controller.pinguino,
    password: str = "",
):
    password = password or os.getenv("PASSWORD") or getpass("Enter Password: ")
    controller = controllers[controller.value]()
    server.main(password, controller)


if __name__ == "__main__":
    app()
