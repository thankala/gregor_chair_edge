from typing import Any

from flask import Flask, request, jsonify

from gpio.gpio import set_pin_state, get_pin_state, cleanup, LEDPin, LEDState, init_pins

# from jsonschema import validate, ValidationError

app = Flask(__name__)


# set_led_schema = {
#     "type": "object",
#     "properties": {
#         "pin": {"type": "string", "enum": ["FREE", "ASSEMBLING", "PENDING"]},
#         "state": {"type": "string", "enum": ["HIGH", "LOW"]}
#     },
#     "required": ["pin", "state"]
# }


@app.route('/pin', methods=['POST'])
def set_led() -> Any:
    data = request.get_json()
    # try:
    #     validate(data, set_led_schema)
    # except ValidationError as e:
    #     return jsonify({'error': e.message}), 400
    pin_name = data.get('pin')
    state_name = data.get('state')

    try:
        pin = LEDPin[pin_name.upper()]
        state = LEDState[state_name.upper()]
    except KeyError:
        return jsonify({'error': 'Invalid pin or state name'}), 400

    set_pin_state(pin, state)
    return jsonify({pin.name: get_pin_state(pin).name}), 200


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
