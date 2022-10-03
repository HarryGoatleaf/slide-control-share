from slide_control_share import create_app, init_socketio

if __name__ == '__main__':
    app, socketio = init_socketio(create_app())
    socketio.run(app, debug=True)
