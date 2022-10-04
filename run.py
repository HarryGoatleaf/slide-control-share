from slide_control_share import create_app, socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)