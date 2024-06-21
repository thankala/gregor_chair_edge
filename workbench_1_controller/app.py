from typing import Any
import os, sys
from flask import Flask, request, jsonify

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from workbench_1_controller.services import (
    workbench_rotate,
    gpio_cleanup,
    gpio_init_pins,
    gpio_set_pin_state,
    gpio_get_pin_state
)

app = Flask(__name__)


@app.route('/primitives/leds', methods=['POST'])
def set_led() -> Any:
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({'error': 'Invalid data format, must be a dictionary'}), 400
    try:
        result = gpio_set_pin_state(data)
    except Exception as e:
        return jsonify(e.args), 400
    return jsonify(result), 200


@app.route('/primitives/leds', methods=['GET'])
def get_leds_state():
    try:
        result = gpio_get_pin_state()
    except Exception as e:
        return jsonify(e.args), 400
    return jsonify(result), 200


@app.route('/primitives/rotate', methods=['POST'])
def rotate():
    workbench_rotate()
    return jsonify("Rotated"), 200


if __name__ == '__main__':
    try:
        gpio_init_pins()
        app.run(host='0.0.0.0', port=5000)
    finally:
        gpio_cleanup()
