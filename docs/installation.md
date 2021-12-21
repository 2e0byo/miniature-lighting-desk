## The server

is deployed on `pypi`. To install it you need a recent python (>=3.9) installed,
and then you can run in a terminal:

```bash
python3 -m pip install miniature-lighting-desk
```

or, if you prefer to pipx:

```bash
pipx install miniature-lighting-desk
```

When the server is installed, it needs to be started. You run it in a terminal
with:

```bash
miniature-lighting-desk-server
```

It will find an available port and set up network and local access.

## The local frontend

is installed with the server.  You run it with:

```bash
miniature-lighting-desk
```

It will start the server if it is not already running.

## The web frontend

need not be installed. It is developed separately from this server, and is
available online at https://github.io/2e0byo/lighting-desk. You will need to
entry the ip (or hostname, if your network resolves hostnames) of the computer
running the server, and the port the server is running on. This information is
printed in the terminal when the server is started. Note that the desk runs
*locally*: no information leaves your local network.
