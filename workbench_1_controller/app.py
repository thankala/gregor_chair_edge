from typing import Any

from flask import Flask, request, jsonify

from gpio.gpio import set_pin_state, get_pin_state, cleanup, LEDPin, LEDState, init_pins

app = Flask(__name__)


@app.route('/pin', methods=['POST'])
def set_led() -> Any:
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({'error': 'Invalid data format, must be a dictionary'}), 400

    for pin_name, state_name in data.items():
        try:
            pin = LEDPin[pin_name.upper()]
            state = LEDState[state_name.upper()]
        except KeyError:
            return jsonify({'error': f'Invalid pin or state name: {pin_name}, {state_name}'}), 400

        set_pin_state(pin, state)

    states = {pin.name: get_pin_state(pin).name for pin in LEDPin}
    return jsonify(states), 200


@app.route('/pins', methods=['GET'])
def get_leds_state():
    states = {pin.name: get_pin_state(pin).name for pin in LEDPin}
    return jsonify(states), 200


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        init_pins()
        app.run(host='0.0.0.0', port=5000)
    finally:
        cleanup()
