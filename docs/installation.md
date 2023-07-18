## The backend

is deployed on `pypi`. To install it you need a recent python (>=3.9) installed,
and then you can run in a terminal:

```
python3 -m pip install miniature-lighting-desk
```

or, if you prefer to use pipx (note that it will not be possible to use the
scripting interface if you install with pipx):

```
pipx install miniature-lighting-desk
```

When the server is installed, it needs to be started. You run it in a terminal
with:

```
lighting_desk server
```


## The local frontend

is installed with the server.  You run it with:

```
lighting_desk local-gui
```

## Server development

Clone this repository, and then run

```
poetry install
poetry shell
```

## Frontend development

Clone [2e0byo/lighting-desk](https://github.com/2e0byo/lighting-desk) and then run

```
cd lighting-desk
yarn install
yarn serve
```

## Contributing

Open a Pull Request.

