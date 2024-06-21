import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Any
from flask import Flask, request, jsonify

from workbench_2_controller.gpio import LedPin, LedState
from workbench_2_controller.services import (
    gpio_cleanup,
    gpio_init_pins,
    gpio_set_pin_state,
    gpio_get_pin_state, set_fixture_state
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


@app.route('/state', methods=['POST'])
def set_state():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({'error': 'Invalid data format, must be a dictionary'}), 400
    try:
        result = set_fixture_state(data)
    except Exception as e:
        return jsonify(e.args), 400
    return jsonify(result), 200


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        gpio_init_pins()
        app.run(host='0.0.0.0', port=5000)
    finally:
        gpio_cleanup()
