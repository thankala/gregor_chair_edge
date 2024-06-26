import os
from flask import Flask, jsonify, request
from controller import RobotController

robot_port = os.getenv('ROBOT_PORT', '/dev/ttyUSB_robot1')

print(f"Robot port is set to {robot_port}")

app = Flask(__name__)

controller = RobotController(port=robot_port)


@app.route('/primitive/move', methods=['POST'])
def move():
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')
    z = data.get('z')
    r = data.get('r')
    try:
        controller.move(x, y, z, r)
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/primitive/grip', methods=['POST'])
def grip():
    data = request.get_json()
    enable_control = data.get('enable_control', True)
    enable_grip = data.get('enable_grip', True)
    try:
        controller.grip(enable_control, enable_grip)
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/primitive/ungrip', methods=['POST'])
def ungrip():
    try:
        controller.ungrip()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/primitive/wait', methods=['POST'])
def wait():
    data = request.get_json()
    ms = data.get('ms')
    try:
        controller.wait(ms)
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/primitive/get_pose', methods=['GET'])
def get_pose():
    try:
        pose = controller.get_pose()
        return jsonify({'pose': pose}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/primitive/clear_alarms', methods=['GET'])
def clear_alarms():
    try:
        controller.clear_alarms()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/primitive/get_alarms_state', methods=['GET'])
def get_alarms():
    try:
        state = controller.get_alarms_state()
        return jsonify({'state': state}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
