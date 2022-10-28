# Backend API

this document contains the format of the backend API messages.

## Data Structures

```json
User = {'id': String, 'name': String}

Presentation = {
  'id': String, 
  'host'          : User,
  'users'         : List(User),
  'current_slide' : Int
  }
```

## REST Routes

* `POST:/api/name`:
  ```json
  POST: {'username': String}
  RESP: {'status': 'success', 'user': User}
  FAIL: {'status': 'failed', 'message': 'already registered'}
  ```
* `GET:/api/name`:
  ```json
  RESP: {'status': 'success', 'user': User}
  FAIL: {'status': 'failed', 'message': 'unknown user'}
  ```
* `POST:/api/presentation/create`:
  ```
  POST: an html form with following fields:
    * 'slides' in files-field

  RESP: {'status': 'success', 'presentation': Presentation}
  FAIL: {'status': 'failed', 'message': 'malformed'}
        {'status': 'failed', 'message': 'unknown user'}
  ```
* `GET:/api/presentation/<presentation_id>`
  ```json
  RESP: {'status': 'success', 'presentation': Presentation}
  FAIL: {'status': 'failed', 'message': 'unknown user'}
  FAIL: {'status': 'failed', 'message': 'presentation does not exist'}
  ```
* `POST:/api/presentation/<presentation_id>/current_slide`
  ```json
  POST: {'new_slide': Int}
  FAIL: ..
  ```
* `GET:/api/presentation/<presentation_id>/current_slide`
  ```json
  RESP: {'status': 'success', 'current_slide': Int}
  FAIL: {'status': 'failed', 'message': 'not in a presentation'}
  FAIL: {'status': 'failed', 'message': 'wrong presentation'}
  ```

## SocketIO Events
### Client side

`set_slide` event:
```json
{"new_slide": Int}
```

`set_users` event:
```json
{"new_users": List(User)}
```
