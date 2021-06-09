import json
import random

from flask import Flask, jsonify, request

app = Flask(__name__)

DATA = {}


@app.route('/vk_id/<username>', methods=['GET'])
def get_user_vk(username):
    if vk_id := DATA.get(username):
        return jsonify({'vk_id': vk_id}), 200
    else:
        return jsonify({}), 404


@app.route('/user', methods=['POST'])
def create_user_vk():
    try:
        req = request.data.decode().replace("'", '"')
        name = json.loads(req).get('username')
        DATA[name] = random.randint(1000, 2000)
        return jsonify({'username': name, 'vk_id': DATA[name]}), 201
    except Exception as e:
        return jsonify({"error": e}), 400


@app.route('/user/<username>', methods=['DELETE'])
def delete_user(username):
    try:
        return jsonify({'username': username, 'vk_id': DATA[username]}), 200
    except:
        return jsonify({'error': f'{username} not found'}), 404


if __name__ == '__main__':
    app.run('0.0.0.0', 8060)
