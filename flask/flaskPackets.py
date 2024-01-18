from flask import flask, request, jsonify, Blueprint, render_template

command_blueprint = Blueprint('command', __name__)

@auth_blueprint.route('/command/capture_packets', methods=['GET'])

def execute_packet_capture():
    return 0