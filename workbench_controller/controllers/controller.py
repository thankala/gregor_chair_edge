from flask import Flask, jsonify, request

from domain.workbench import Workbench
from services.service import rotate_workbench, get_fixture_state, set_fixture_state


def create_app(workbench: Workbench) -> Flask:
    app = Flask(__name__)

    @app.route('/workbench/rotate', methods=['POST'])
    def rotate():
        try:
            return jsonify({"rotation": rotate_workbench(workbench)})
        except Exception as e:
            return jsonify({'errors': e.args}), 400

    @app.route('/workbench/states', methods=['GET'])
    def get_states():
        try:
            return jsonify(get_fixture_state(workbench)), 200
        except Exception as e:
            return jsonify({'errors': e.args}), 400

    @app.route('/workbench/state/<fixture_name>', methods=['GET'])
    def get_state(fixture_name: str):
        try:
            return jsonify(get_fixture_state(workbench, fixture_name)), 200
        except Exception as e:
            return jsonify({'errors': e.args}), 400

    @app.route('/workbench/state/<fixture_name>', methods=['POST'])
    def set_state(fixture_name: str):
        try:
            request_data = request.get_json()
            state_name = request_data.get('state')
            return jsonify(set_fixture_state(workbench, fixture_name, state_name)), 200
        except Exception as e:
            return jsonify({'errors': e.args}), 400

    return app
