from . import server
from .local_gui import main as gui
import click
import os
from getpass import getpass


@click.group()
@click.version_option()
def cli():
    pass


@cli.command()
def local_gui():
    gui()


@cli.command()
@click.option("--mock", is_flag=True, help="Use mocked hardware.")
@click.option(
    "--password", help="Password.  If not supplied will be read from env or prompted."
)
def backend(mock, password):
    password = password or os.getenv("PASSWORD") or getpass("Enter Password: ")
    server.main(mock, password)


if __name__ == "__main__":
    cli()
