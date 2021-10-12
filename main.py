from google.cloud import datastore
from flask import Flask, request
import json
import constants

app = Flask(__name__)
client = datastore.Client()

@app.route('/')
def index():
    return 'Please navigate to /boats or /slips to use this API'

@app.route('/boats', methods=['GET', 'POST'])
def boats():
    if request.method == 'GET':
        query = client.query(kind=constants.boat)
        results = list(query.fetch())
        for boat in results:
            boat["id"] = boat.key.id
        return json.dumps(results)

    elif request.method == 'POST':
        content = request.get_json()
        new_boat = datastore.Entity(client.key(constants.boat))
        new_boat.update(content)
    else:
        return 'Invalid request method, please try again'
"""
@app.route('/boat/<id>', methods=['GET', 'PATCH', 'DELETE'])
def boat():
    if request.method == 'GET':
    elif request.method == 'PATCH':
    elif request.method == 'DELETE':
    else:
        return 'Invalid request method, please try again'

@app.route('/boat/<slipid>', methods=['POST', 'DELETE'])
def boat():
    if request.method == 'POST':
    elif request.method == 'DELETE':
    else:
        return 'Invalid request method, please try again'

@app.route('/slip', methods=['GET', 'POST'])
def slip():
    if request.method == 'GET':
    elif request.method == 'POST':
    else:
        return 'Invalid request method, please try again'

@app.route('/slip/<id>', methods=['GET', 'PATCH', 'DELETE'])
def boat():
    if request.method == 'GET':
    elif request.method == 'PATCH':
    elif request.method == 'DELETE':
    else:
        return 'Invalid request method, please try again'
"""

if __name__ == "__main__":
    app.run(debug=True)