from flask import Flask
import zmq
import json
context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

app = Flask(__name__)


@app.route('/action/<action>')
def do_action(action):
    print("Sending request")
    socket.send_json(action)
    jsonr = socket.recv_json()
    print("Received reply: ", jsonr)

    return f'Hello, World! {jsonr}'
