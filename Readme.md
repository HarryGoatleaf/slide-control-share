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
├── Readme.md
├── docker-compose.yml          # |
├── Dockerfile                  # | docker files are currently only suitable for debugging
├── requirements.txt
├── slide_control_share
│   ├── __init__.py             # configures app, registers extensions&blueprints
│   ├── db.py                   # database module
│   ├── hello.py                # |
│   ├── presentation.py         # | blueprints
│   ├── static                  # contains static files like stylesheets
│   │   └── example.css
│   └── templates
│       ├── create.html
│       ├── hello.html
│       └── presentation.html
├── instance                    # app runtime data
└── slide-control-share-diagram
```
