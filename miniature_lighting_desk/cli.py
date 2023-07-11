import os
from enum import Enum
from getpass import getpass
from typing import Literal

import rich
import typer

from . import server
from .async_hal import WifiControllerABC, controllers
from .local_gui import main as gui

app = typer.Typer()

# Typer provides proper hinting like this
_Controller = Enum("_Controller", {k: k for k in controllers.keys()})


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


@app.command(help="Connect controller to wifi.")
def wifi(
    controller: _Controller = _Controller["16chan"].value,
    port: str = "",
    ssid: str = "",
    password: str = "",
):
    controller = controllers[controller.value]
    if not issubclass(controller, WifiControllerABC):
        raise ValueError(
            f"Connecting to wifi only makes sense with a wifi-enabled controller."
        )
    if not ssid:
        ssid = input("SSID: ").strip()
    if not password:
        password = getpass("Password: ").strip()
    kwargs = {"port": port} if port else {}
    rich.print(controller(**kwargs).wifi(ssid, password))


@app.command(help="Get controller wifi status.")
def wifi_status(
    controller: _Controller = _Controller["16chan"].value,
    port: str = "",
):
    controller = controllers[controller.value]
    if not issubclass(controller, WifiControllerABC):
        raise ValueError(
            "Connecting to wifi only makes sense with a wifi-enabled controller."
        )
    kwargs = {"port": port} if port else {}
    rich.print(controller(**kwargs).wifi_status())


@app.command(help="Drop to repl.")
def repl(
    controller: _Controller = _Controller["16chan"].value,
    port: str = "",
):
    kwargs = {"port": port} if port else {}
    controller = controllers[controller.value]
    if not hasattr(controller, "repl"):
        raise ValueError("Dropping to repl not possible on this controller.")
    rich.print(controller(**kwargs).repl())


if __name__ == "__main__":
    app()
