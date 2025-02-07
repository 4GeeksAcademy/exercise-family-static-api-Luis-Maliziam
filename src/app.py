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
# create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    if members == [] :
       return "No existen miembros", 400
    return jsonify(members), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member_result = jackson_family.get_member(member_id)
    if member_result is None :
        return jsonify({"msg":"Miembro no encontrado"}), 404
    return jsonify(member_result), 200

@app.route('/member', methods=['POST'])
def handle_post():
        request_body = request.json
        if len(request_body) < 3:
            return jsonify({"msg": "missing information"}), 400
        elif len(request_body) > 3:
            return jsonify({"msg": "a lot of information"}), 400
        else: 
            member_add_result = jackson_family.add_member(request_body)
            return jsonify(request_body), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def handle_delete_member(member_id):
    delete_member = jackson_family.delete_member(member_id) 
    if delete_member == None:
        return jsonify({"msg":"El miembro que desea eliminar no existe"}), 400
    return jsonify({"msg":"El miembro ha sido eliminado"}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
