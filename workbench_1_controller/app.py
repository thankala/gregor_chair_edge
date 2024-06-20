from typing import Any

from flask import Flask, request, jsonify

from workbench_1_controller.gpio.gpio import LedPin, State
from workbench_1_controller.services.service import (
    workbench_rotate,
    gpio_cleanup,
    gpio_init_pins,
    gpio_set_pin_state,
    gpio_get_pin_state
)

app = Flask(__name__)


@app.route('/leds', methods=['POST'])
def set_led() -> Any:
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({'error': 'Invalid data format, must be a dictionary'}), 400

    for pin_name, state_name in data.items():
        try:
            pin = LedPin[pin_name.upper()]
            state = State[state_name.upper()]
        except KeyError:
            return jsonify({'error': f'Invalid pin or state name: {pin_name}, {state_name}'}), 400

        gpio_set_pin_state(pin, state)

    states = {pin.name: gpio_get_pin_state(pin).name for pin in LedPin}
    return jsonify(states), 200


@app.route('/leds', methods=['GET'])
def get_leds_state():
    states = {pin.name: gpio_get_pin_state(pin).name for pin in LedPin}
    return jsonify(states), 200


@app.route('/rotate', methods=['POST'])
def rotate():
    workbench_rotate()
    return jsonify("Rotated"), 200


if __name__ == '__main__':
    try:
        gpio_init_pins()
        app.run(host='0.0.0.0', port=5000)
    finally:
        gpio_cleanup()
