import os
from enum import Enum
from getpass import getpass
from typing import Literal, Optional

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
    import serial
    from serial.tools.miniterm import Miniterm

    serial_instance = serial.serial_for_url(port or "/dev/ttyUSB0", 460_800)
    if not hasattr(serial_instance, "cancel_read"):
        serial_instance.timeout = 1
    miniterm = Miniterm(serial_instance)
    miniterm.set_tx_encoding("utf8")
    miniterm.set_rx_encoding("utf8")

    # miniterm.main(default_port=port or "/dev/ttyUSB0", default_baudrate=460800)
    miniterm.start()
    try:
        miniterm.join()
    except KeyboardInterrupt:
        pass
    print("--- Leaving repl ---")
    miniterm.join()
    miniterm.close()


@app.command(help="Get or set pwm frequency.")
def frequency(
    controller: _Controller = _Controller["16chan"].value,
    port: str = "",
    frequency_hz: Optional[int] = None,
):
    kwargs = {"port": port} if port else {}
    controller = controllers[controller.value]
    if not hasattr(controller, "frequency"):
        raise ValueError("Dropping to repl not possible on this controller.")
    rich.print(controller(**kwargs).frequency(frequency_hz))


if __name__ == "__main__":
    app()
