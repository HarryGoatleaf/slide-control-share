# Backend API

this document contains the format of the backend API messages.

## REST Routes

* `POST:/api/name`:
  ```json
  POST: {'username': '...'}
  RESP: {'status': 'success', 'user': {...}}
  ```
* `GET:/api/name`:
  ```json
  RESP: {'status': 'success', 'user': {...}}
  FAIL: {'status': 'failed', 'message': 'unknown user'}
  ```
* `POST:/api/presentation/create`:
  ```json
  POST: {'content': '...'}
  RESP: {'status': 'success', 'presentation_id': '...'}
  FAIL: {'status': 'failed', 'message': 'malformed'}
        {'status': 'failed', 'message': 'unknown user'}
  ```
* `GET:/api/presentation/<presentation_id>`
  ```json
  RESP: {'status': 'success', 'presentation': {...}}
  FAIL: {'status': 'failed', 'message': unknown user'}
  ```
* `POST:/api/presentation/<presentation_id>/current_slide`
  ```json
  POST: {}
  ```
* `GET:/api/presentation/<presentation_id>/current_slide`
  ```json
  RESP: {'status': 'success', 'current_slide': '...'}
  FAIL: {'status': 'failed', 'message': 'not in a presentation'}
  ```


## SocketIO Events
### Server side

Client sends `set_slide` event:
```json
{"new_slide": 1}
```
Server replies with either:
* `200` success
* `400` bad request: i.e. "new_slide" is not a valid slide number
* `403` forbidden: user does not have sufficient permissions, or is not named yet
* `404` not found: presentation id does not exist

Client sends `add_me_to_room`: (no data)

Server replies with:
* `200` success
* `404` not found: presentation id does not exist

### Client side

`set_slide` event:
```json
{"new_slide": 1}
```

`set_user` event:
