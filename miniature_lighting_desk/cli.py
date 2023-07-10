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
    port: str = "",
):
    kwargs = {"port": port} if port else {}
    controller = controllers[controller.value](**kwargs)
    gui(controller)


@app.command(help="Run backend for web gui.")
def backend(
    controller: _Controller = _Controller.pinguino,
    password: str = "",
    port: str = "",
):
    password = password or os.getenv("PASSWORD") or getpass("Enter Password: ")
    kwargs = {"port": port} if port else {}
    controller = controllers[controller.value](**kwargs)
    server.main(password, controller)


if __name__ == "__main__":
    app()
