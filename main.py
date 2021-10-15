from google.cloud import datastore
from flask import Flask, request
import json
import constants

app = Flask(__name__)
client = datastore.Client()

url = "http://localhost:8080/"
boatID_error = {'Error': "No boat with this boat_id exists"}
slipID_error = {'Error': "No slip with this slip_id exists"}
boat_attr_error = {'Error': "The request object is missing at least one of the required attributes"}
slip_attr_error = {'Error': "The request object is missing the required number"}

# Clears datastore every reset
del_query = client.query(kind=constants.boats)
del_results = list(del_query.fetch())
for entity in del_results:
    client.delete(entity.key)


@app.route('/')
def index():
    return 'Please navigate to /boats or /slips to use this API'


@app.route('/boats', methods=['GET', 'POST'])
def boats():
    if request.method == 'GET':
        query = client.query(kind=constants.boats)
        results = list(query.fetch())
        for boat in results:
            boat["id"] = boat.key.id
        return json.dumps(results)

    elif request.method == 'POST':
        content = request.get_json()
        if 'name' not in content:
            return boat_attr_error, 400
        elif 'type' not in content:
            return boat_attr_error, 400
        elif 'length' not in content:
            return boat_attr_error, 400
        else:
            new_boat = datastore.Entity(client.key(constants.boats))
            new_boat.update({"name": content["name"], "type": content["type"], "length": content["length"]})
            client.put(new_boat)
            new_boat["id"] = new_boat.key.id
            new_boat["self"] = url + "boats/" + str(new_boat.key.id)
            return new_boat, 201
    else:
        return 'Invalid request method, please try again'


@app.route('/boats/<boat_id>', methods=['GET', 'PATCH', 'DELETE'])
def boat(boat_id):
    if request.method == 'GET':
        boat_key = client.key(constants.boats, int(boat_id))
        boat = client.get(key=boat_key)
        if boat is None:
            return boatID_error, 404
        else:
            boat["id"] = boat.key.id
            boat["self"] = url + "boats/" + str(boat.key.id)
            return json.dumps(boat)

    elif request.method == 'PATCH':
        content = request.get_json()
        if 'name' not in content:
            return boat_attr_error, 400
        elif 'type' not in content:
            return boat_attr_error, 400
        elif 'length' not in content:
            return boat_attr_error, 400
        else:
            boat_key = client.key(constants.boats, int(boat_id))
            boat = client.get(key=boat_key)
            if boat is None:
                return boatID_error, 404
            boat.update({"name": content["name"], "type": content["type"], "length": content["length"]})
            client.put(boat)
            boat["id"] = boat.key.id
            boat["self"] = url + "boats/" + str(boat.key.id)
            return json.dumps(boat)

    elif request.method == 'DELETE':
        boat_key = client.key(constants.boats, int(boat_id))
        boat = client.get(key=boat_key)
        if boat is None:
            return boatID_error, 404
        client.delete(boat_key)
        return '', 204

    else:
        return 'Invalid request method, please try again'


@app.route('/slips', methods=['GET', 'POST'])
def slips():
    if request.method == 'GET':
        query = client.query(kind=constants.slips)
        results = list(query.fetch())
        for slip in results:
            slip["id"] = slip.key.id
        return json.dumps(results)

    elif request.method == 'POST':
        content = request.get_json()
        if 'number' not in content:
            return slip_attr_error, 400
        else:
            new_slip = datastore.Entity(client.key(constants.slips))
            new_slip.update({"number": content["number"], "current_boat": None})
            client.put(new_slip)
            new_slip["id"] = new_slip.key.id
            new_slip["self"] = url + "slips/" + str(new_slip.key.id)
            return new_slip, 201
    else:
        return 'Invalid request method, please try again'


@app.route('/slips/<slip_id>', methods=['GET', 'DELETE'])
def slip(slip_id):
    if request.method == 'GET':
        slip_key = client.key(constants.slips, int(slip_id))
        slip = client.get(key=slip_key)
        if slip is None:
            return slipID_error, 404
        else:
            slip["id"] = slip.key.id
            slip["self"] = url + "slips/" + str(slip.key.id)
            return json.dumps(slip)

    elif request.method == 'DELETE':
        slip_key = client.key(constants.boats, int(slip_id))
        slip = client.get(key=slip_key)
        if slip is None:
            return boatID_error, 404
        client.delete(slip_key)
        return '', 204

    else:
        return 'Invalid request method, please try again'


"""
@app.route('/slips/<slip_id>/<boat_id>', methods=['PUT', 'DELETE'])
def slip_map(slip_id,boat_id):
    if request.method == 'PUT':

    elif request.method == 'DELETE':

    else:
        return 'Invalid request method, please try again'
"""

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
