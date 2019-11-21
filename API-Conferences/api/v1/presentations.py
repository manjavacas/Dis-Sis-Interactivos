# -*- coding: utf-8 -*-

from api.v1.attendees import attendees_list

from flask import Blueprint, jsonify, abort, make_response, request


class Presentation:

    def __init__(self, iden, title, date, hour, lecturer, authors, topics, place):
        self.iden = iden
        self.title = title
        self.date = date
        self.hour = hour
        self.lecturer = lecturer
        self.authors = authors
        self.topics = topics
        self.place = place


####################################################################
# Example:
presentations_list = [Presentation(1, 'New trends in HCI', '12-5-19', '15:30', attendees_list[1], attendees_list[0:2], ['hci'], 'General garden'),
                      Presentation(2, 'Software: just a lie?', '12-5-19', '15:30',
                                   attendees_list[0], attendees_list[0:2], ['software engineering'], 'Room 206'),
                      Presentation(3, 'Neural networks: just a trend?', '12-5-19', '18:15', attendees_list[0], attendees_list[0], ['artificial intelligence'], 'Classroom 43-B')]

####################################################################

presentations_api = Blueprint('presentations_api', __name__)

# Devuelve el listado de presentaciones
@presentations_api.route('/v1/presentations/', methods=['GET'])
def getPresentations():
    return jsonify({'presentations': presentations_list})

# Devuelve los datos de una presentacion
@presentations_api.route('/v1/presentations/<int:presentation_id>/', methods=['GET'])
def getOnePresentation(presentation_id):
    for presentation in presentations_list:
        if presentation.iden == presentation_id:
            return jsonify({'presentation': presentation})
    abort(404)

# Crea una nueva presentacion
@presentations_api.route('/v1/presentations/', methods=['POST'])
def createPresentation():
    if not request.json or not 'iden' in request.json:
        abort(404)

    iden = request.json.get('iden')
    title = request.json.get('title')
    date = request.json.get('date')
    hour = request.json.get('hour')
    lecturer = request.json.get('lecturer')
    authors = request.json.get('authors')
    topics = request.json.get('topics')
    place = request.json.get('place')

    presentation = Presentation(
        iden, title, date, hour, lecturer, authors, topics, place)
    presentations_list.append(presentation)
    return jsonify({'presentation': presentation}), 201

# Actualiza los datos de una presentacion
@presentations_api.route('/v1/presentations/<int:presentation_id>/', methods=['PUT'])
def updatePresentation(presentation_id):
    presentation = [
        presentation for presentation in presentations_list if presentation.iden == presentation_id]
    presentation[0]['title'] = request.json.get(
        'title', presentation[0]['title'])
    presentation[0]['date'] = request.json.get('date', presentation[0]['date'])
    presentation[0]['hour'] = request.json.get('hour', presentation[0]['hour'])
    presentation[0]['lecturer'] = request.json.get(
        'lecturer', presentation[0]['lecturer'])
    presentation[0]['authors'] = request.json.get(
        'authors', presentation[0]['authors'])
    presentation[0]['topics'] = request.json.get(
        'topics', presentation[0]['topics'])
    presentation[0]['place'] = request.json.get(
        'place', presentation[0]['place'])

    return jsonify({'presentation': presentation[0]})

# Borrar una presentacion
@presentations_api.route('/v1/presentations/<int:presentation_id>/', methods=['DELETE'])
def deletePresentation(presentation_id):
    presentation = [
        presentation for presentation in presentations_list if presentation.iden == presentation_id]
    presentations_list.remove(presentation[0])
    return jsonify({}), 204  # No content

# Devuelve las presentaciones de un dia a una determinada hora y fecha
@presentations_api.route('/v1/presentations/<string:presentation_date>/at/<string:presentation_hour>/', methods=['GET'])
def getPresentationByTime(presentation_date, presentation_hour):
    presentations_at = []
    for presentation in presentations_list:
        if presentation.date == presentation_date and presentation.hour == presentation_hour:
            presentations_at.append(presentation)
    if len(presentations_at) > 0:
        return jsonify({'presentations at {0}'.format(presentation_hour): presentations_at})
    else:
        return make_response(jsonify({'warning': 'No presentations at {0}, {1}'.format(presentation_hour, presentation_date)}))

# Obtener presentaciones en un determinado lugar y fecha
@presentations_api.route('/v1/presentations/<string:presentation_date>/in/<string:presentation_place>/', methods=['GET'])
def getPresentationsByPlace(presentation_date, presentation_place):
    presentations_in = []
    for presentation in presentations_list:
        if presentation.date == presentation_date and presentation.place == presentation_place:
            presentations_in.append(presentation)
    if len(presentations_in) > 0:
        return jsonify({'presentations in {0}'.format(presentation_place): presentations_in})
    else:
        return make_response(jsonify({'warning': 'No presentations in {0}, {1}'.format(presentation_place, presentation_date)}))

# Manejo errores 404
@presentations_api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
