import os

from controller import RobotController

robot_port = os.getenv('ROBOT_PORT', '/dev/ttyUSB0')

print(f"Robot port is set to {robot_port}")

# Example of starting a Flask server (if you are using Flask)
from flask import Flask

app = Flask(__name__)

controller = RobotController(port=robot_port)


@app.route('/')
def hello_world():
    return 'Hello, World!!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
