# Slide Control Share

.. is a webapp that lets users interactively present PDF slides in a webapp.

## Design Goals

* no login required
* ...

## Deploying

WIP

## Debuging

We recommend using docker/docker-compose and VSCode with the "Dev Containers" extension.

* open project folder with VSCode
* select "open folder in container" (configuration is in `.devcontainer`)
* run the server with `flask --app slide_control_share --debug run`
* point your browser to http://127.0.0.1:5000

## Code Structure

```
/slide-control-share
├── Readme.md # this file :)
├── docker-compose.yml
├── Dockerfile # docker files are currently only suitable for debugging
├── requirements.txt # python package dependencies
├── slide_control_share
│   ├── __init__.py # configures app, registers extensions&blueprints
│   ├── db.py # database
│   ├── hello.py
│   ├── presentation.py
│   ├── static
│   │   └── example.css
│   └── templates
│       ├── create.html
│       ├── hello.html
│       └── presentation.html
├── instance
└── slide-control-share-diagram
```