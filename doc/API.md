# Backend API

this document contains the format of the backend API messages.

## REST Routes

* `POST:/api/name`:
  ```json
  POST: {'username': '...'}
  RESP: {'status': 'success', 'user': {...}}
  FAIL: {'status': 'failed', 'message': 'already registered'}
  ```
* `GET:/api/name`:
  ```json
  RESP: {'status': 'success', 'user': {...}}
  FAIL: {'status': 'failed', 'message': 'unknown user'}
  ```
* `POST:/api/presentation/create`:
  ```json
  POST: {'content': '...'}
  RESP: {'status': 'success', 'presentation': {...}}
  FAIL: {'status': 'failed', 'message': 'malformed'}
        {'status': 'failed', 'message': 'unknown user'}
  ```
* `GET:/api/presentation/<presentation_id>`
  ```json
  RESP: {'status': 'success', 'presentation': {...}}
  FAIL: {'status': 'failed', 'message': 'unknown user'}
  FAIL: {'status': 'failed', 'message': 'presentation does not exist'}
  ```
* `POST:/api/presentation/<presentation_id>/current_slide`
  ```json
  POST: {}
  ```
* `GET:/api/presentation/<presentation_id>/current_slide`
  ```json
  RESP: {'status': 'success', 'current_slide': '...'}
  FAIL: {'status': 'failed', 'message': 'not in a presentation'}
  FAIL: {'status': 'failed', 'message': 'wrong presentation'}
  ```


## SocketIO Events
### Client side

`set_slide` event:
```json
{"new_slide": 1}
```

`set_users` event:
```json
{"new_users": {...}}
```
