import os

from flask import Flask, jsonify, request
from controller import RobotController

robot_name = os.getenv('ROBOT_NAME', 'robot1')
robot_serial_number = os.getenv('ROBOT_SERIAL_NUMBER', '123456')
port = os.getenv('PORT', 8000)

app = Flask(__name__)

controller = RobotController(serial_number=robot_serial_number, name=robot_name)


@app.route('/primitive/move', methods=['POST'])
def move():
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')
    z = data.get('z')
    r = data.get('r')
    try:
        return jsonify(controller.move(x, y, z, r)), 200
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


@app.route('/primitive/get_pose', methods=['GET'])
def get_pose():
    try:
        return jsonify(controller.get_pose()), 200
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


@app.route('/home', methods=['POST'])
def home():
    try:
        controller.home()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route("/primitive/move/<name>", methods=["POST"])
def move_to(name: str):
    try:
        return jsonify(controller.move_to(name)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route("/primitive/pick", methods=["POST"])
def pick():
    try:
        controller.pick()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route("/primitive/place", methods=["POST"])
def place():
    try:
        controller.place()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route("/composite/pick_and_place", methods=["POST"])
def pick_and_place():
    try:
        controller.pick_and_place()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route("/composite/pick_and_insert", methods=["POST"])
def pick_and_insert():
    try:
        controller.pick_and_insert()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/composite/pick_and_flip_and_press', methods=['POST'])
def pick_and_flip_and_press():
    try:
        controller.pick_and_flip_and_press()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/composite/screw_pick_and_fasten', methods=['POST'])
def screw_pick_and_fasten():
    try:
        controller.screw_pick_and_fasten()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
