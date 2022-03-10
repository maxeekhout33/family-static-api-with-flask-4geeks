"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

miembros = [
    {
            "id": "1",
            "first_name": "Max",
            "age": 33,
            "lucky_numbers": [7,13,22]
        },
        {
            "id": "2",
            "first_name": "Jane",
            "age": 35,
            "lucky_numbers": [7,13,22]
        },
        {
            "id": "3",
            "first_name": "Jimmy",
            "age": 5,
            "lucky_numbers": [1]
        }
]
# create the jackson family object
jackson_family = FamilyStructure("Jackson", miembros)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    # response_body = {
    #     # "hello": "world",
    #     "family": members
    # }
    response_body = members


    return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def create_member():
    new_member = request.json
    miembros.append(new_member)
    return jsonify(miembros)
    # if isinstance(new_member, FamilyStructure):
    #     return jsonify(members), 200
    # else:
    #     return jsonify("No se pudo agregar el miembro"), 400 

@app.route('/member/<int:id>')
def member_detail(id):
    one_member = jackson_family.get_member(id)
    # return jsonify(one_member)
    if one_member is None:
        return jsonify({
            "msg": "not found"
        }), 404
    return jsonify(one_member), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete(id):
    delete_one_member = jackson_family.delete_member(id)
    if delete_one_member is None:
        return jsonify({
            "msg": "not found"
        }), 404
    return jsonify({
            "done": True
        }), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
