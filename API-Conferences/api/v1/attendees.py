# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, abort, make_response, request


class Attendee:

    def __init__(self, iden, name, surname, institution, languages, country, research_in, is_lecturer, clicker_id):
        self.iden = iden
        self.name = name
        self.surname = surname
        self.institution = institution
        self.languages = languages
        self.country = country
        self.research_in = research_in
        self.is_lecturer = is_lecturer
        self.clicker_id = clicker_id


####################################################################
# Example:
attendees_list = [Attendee(1, 'John', 'Frusciante', 'Google', ['english', 'spanish'], 'United States', ['artificial intelligence'], True, 'D8-D3-85-EA-1B-EE'),
                  Attendee(2, 'Tomo', 'Fujita', 'CERN', ['english', 'korean'], 'China', [
                           'hci', 'artificial intelligence'], False, 'D8-D3-85-EA-1B-EE'),
                  Attendee(3, 'Anthony', 'Kiedis', 'MIT', ['english'], 'Lithuania', ['software engineering', 'human-computer interaction'], False, 'D8-D3-85-EA-1B-EE')]

####################################################################

attendees_api = Blueprint('attendees_api', __name__)

# Devuelve el listado de asistentes
@attendees_api.route('/v1/attendees/', methods=['GET'])
def getAttendees():
    return jsonify({'attendees': attendees_list})

# Devuelve los datos de un asistente
@attendees_api.route('/v1/attendees/<int:attendee_id>/', methods=['GET'])
def getOneAttendee(attendee_id):
    for attendee in attendees_list:
        if attendee.iden == attendee_id:
            return jsonify({'attendee': attendee})
    abort(404)

# Crea un nuevo asistente
@attendees_api.route('/v1/attendee/', methods=['POST'])
def createAttendee():
    if not request.json or not 'iden' in request.json:
        abort(404)

    iden = request.json.get('iden')
    name = request.json.get('name')
    surname = request.json.get('surname')
    institution = request.json.get('institution')
    languages = request.json.get('languages')
    country = request.json.get('country')
    research_in = request.json.get('research_in')
    is_lecturer = request.json.get('is_lecturer')
    clicker_id = request.json.get('clicker_id')

    attendee = Attendee(iden, name, surname, institution,
                        languages, country, research_in, is_lecturer, clicker_id)
    attendees_list.append(attendee)
    return jsonify({'attendee': attendee}), 201

# Actualiza los datos de un asistente
@attendees_api.route('/v1/attendees/<int:attendee_id>/', methods=['PUT'])
def updateAttendee(attendee_id):
    attendee = [
        attendee for attendee in attendees_list if attendee.iden == attendee_id]
    attendee[0]['name'] = request.json.get('name', attendee[0]['name'])
    attendee[0]['surname'] = request.json.get(
        'surname', attendee[0]['surname'])
    attendee[0]['institution'] = request.json.get(
        'institution', attendee[0]['institution'])
    attendee[0]['languages'] = request.json.get(
        'languages', attendee[0]['languages'])
    attendee[0]['country'] = request.json.get(
        'country', attendee[0]['country'])
    attendee[0]['research_in'] = request.json.get(
        'research_in', attendee[0]['research_in'])
    attendee[0]['is_lecturer'] = request.json.get(
        'is_lecturer', attendee[0]['is_lecturer'])
    attendee[0]['clicker_id'] = request.json.get(
        'clicker_id', attendee[0]['clicker_id'])

    return jsonify({'attendees': attendee[0]})

# Borrar un asistente
@attendees_api.route('/v1/attendees/<int:attendee_id>/', methods=['DELETE'])
def deleteAttendee(attendee_id):
    attendee = [
        attendee for attendee in attendees_list if attendee.iden == attendee_id]
    attendees_list.remove(attendee[0])
    return jsonify({}), 204  # No content

# Buscar asistentes con intereses similares
@attendees_api.route('/v1/attendee/<int:attendee_id>/similars', methods=['GET'])
def getSimilars(attendee_id):
    similars = []
    user_topics = []

    for attendee in attendees_list:
        if attendee.iden == attendee_id:
            user_topics = attendee.research_in
    for attendee in attendees_list:
        if (attendee.iden != attendee_id) and (len(set(attendee.research_in) & set(user_topics)) > 0):
            similars.append(attendee)
    return jsonify({'similar_researchers to attendee {0}'.format(attendee_id): similars}), 201

# Manejo errores 404
@attendees_api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
