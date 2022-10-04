# Backend API

this document contains the format of the backend API messages.

## SocketIO Events

### Server side

Client sends 'set_slide' event:
```json
{"new_slide": 1}
```
Server replies with either:
* `200` success
* `400` bad request: i.e. "new_slide" is not a valid slide number
* `403` forbidden: user does not have sufficient permissions, or is not named yet
* `404` not found: presentation id does not exist

Client sends 'add_me_to_room': (no data)

Server replies with:
* `200` success
* `404` not found: presentation id does not exist

### Client side

'set_slide' event:
```json
{"new_slide": 1}
```

'set_user' event: