# Slide Control Share

.. is a webapp that lets users interactively present PDF slides in a webapp.

## Design Goals

* no login required
* 💨 fast
* ✨ pretty

## Deploying

WIP

## Debuging

We recommend using docker/docker-compose and VSCode with the "Dev Containers" extension.

* open `frontend` or `backend` folder with VSCode
* select "open folder in container" (configuration is in `.devcontainer`)
* for **backend**:
  * start the server with `python3 run.py`
  * point your browser to http://127.0.0.1:5000
* for **frontend**:
  * start dev server with `npm run dev`
  * point your browser to http://127.0.0.1:5173

## Code Structure
```
├── backend
│   ├── run.py                      # server launcher script
│   ├── backend
│   │   ├── __init__.py             # flask 'app' init stuff
│   │   ├── db.py                   # database 'schema'
│   │   ├── events.py               # socketio events
│   │   ├── presentation.py         # presentation api
│   │   └── user.py                 # user api
│   ├── instance                    # folder for temporary data
│   ├── Dockerfile
│   └── requirements.txt
├── doc
│   ├── API.md
│   ├── intervace-sketch.svg
│   └── slide-control-share-diagram
├── frontend
│   ├── index.html                  # (boilerplate) page that just contains root
│   │                               # element of app
│   ├── public
│   │   └── favicon.ico
│   ├── src
│   │   ├── main.js                 # configures vuejs app and mounts it to to
│   │   │                           # root app in index.html
│   │   ├── components              # ┐
│   │   ├── assets                  # ┴ until now unused
│   │   ├── App.vue
│   │   ├── store.js                # application global state singleton
│   │   ├── backend.js              # singleton for backend http connection
│   │   ├── router.js               # router info (url routes)
│   │   └── views
│   │       ├── Index.vue           # landing page
│   │       ├── Hello.vue           # requests name from user
│   │       ├── Create.vue          # create new presentation
│   │       └── Presentation.vue    # presentation view
│   ├── Dockerfile
│   ├── package.json                # ┐
│   ├── package-lock.json           # ├ project config
│   └── vite.config.js              # ┘
├── docker-compose.yml              # docker-compose for whole project
└── Readme.md                       # this file :)
```
