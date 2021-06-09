import json
import os
import threading
from flask import Flask, jsonify, request
import logging

file_handler = logging.FileHandler(os.path.join("/tmp/tests", 'mock.log'), 'w')

app = Flask(__name__)

DATA = {}
user_id_seq = 1


@app.route('/user/<id>', methods=['GET'])
def get_user_surname(id):
    try:
        if name := DATA.get(id_user := int(id)):
            return jsonify(
                {
                    "id": id_user,
                    "name": name
                }), 200
        else:
            return jsonify({"error": f'User {id} not fount'}), 404
    except Exception as e:
        return jsonify({"error": e}), 400


@app.route('/user', methods=['POST'])
def create_user():
    global user_id_seq
    try:
        req = request.data.decode().replace("'", '"')
        name = json.loads(req).get('name')
        DATA[user_id_seq] = name
        data = {
            "id": user_id_seq,
            "name": name
        }
        user_id_seq += 1
        return jsonify(data), 201
    except Exception as e:
        return jsonify({"error": e}), 400


@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    try:
        if DATA.get(id_user := int(id)):
            req = request.data.decode().replace("'", '"')
            name = json.loads(req).get('name')
            DATA[id_user] = name
            data = {
                "id": id_user,
                "name": DATA[id_user]
            }
            return jsonify(data), 200
        else:
            return jsonify({"error": f"User {id} not found."}), 404
    except Exception as e:
        return jsonify({"error": e}), 400


@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        if DATA.get(id_user := int(id)):
            data = {
                "id": id_user,
                "name": DATA.pop(id_user)
            }
            return jsonify(data), 200
        else:
            return jsonify({"error": f"User {id} not found."}), 404
    except Exception as e:
        return jsonify({"error": e}), 400


def run_mock(host: str, port: int):
    server = threading.Thread(target=app.run, kwargs={
        'host': host,
        'port': port
    })
    server.start()
    # file_handler = logging.FileHandler(os.path.join("/tmp/tests", 'mock.log'), 'w')
    logging.getLogger('werkzeug').setLevel(logging.DEBUG)
    logging.getLogger('werkzeug').addHandler(file_handler)
    file_handler.close()
    return server


def shutdown_mock():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_mock()
    file_handler.close()
    return jsonify({"info": "OK, exiting"}), 200
