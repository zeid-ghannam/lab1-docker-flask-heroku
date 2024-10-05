from flask import Blueprint, jsonify, request, url_for
from app.services import PersonService

bp = Blueprint('main', __name__)

@bp.route('/persons/<int:person_id>', methods=['GET'])
def get_person(person_id):
    person = PersonService.get_person(person_id)
    if person:
        return jsonify(person)
    return jsonify({'error': 'Person not found'}), 404

@bp.route('/persons', methods=['GET'])
def get_all_persons():
    persons = PersonService.get_all_persons()
    return jsonify(persons)

@bp.route('/persons', methods=['POST'])
def create_person():
    data = request.json
    person = PersonService.create_person(data['name'], data['age'])
    response = jsonify(person)
    response.status_code = 201
    # response.headers['Location'] = url_for('main.get_person', person_id=person.id)
    return response

@bp.route('/persons/<int:person_id>', methods=['PATCH'])
def update_person(person_id):
    data = request.json
    person = PersonService.update_person(person_id, data['name'], data['age'])
    if person:
        return jsonify(person)
    return jsonify({'error': 'Person not found'}), 404

@bp.route('/persons/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    if PersonService.delete_person(person_id):
        return '', 204
    return jsonify({'error': 'Person not found'}), 404
