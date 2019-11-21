# -*- coding: utf-8 -*-

from api.v1.attendees import attendees_list

from flask import Blueprint, jsonify, abort, make_response, request


class Conference:

    def __init__(self, iden, name, topics, city, country, date, general_chair, attendees, information):
        self.iden = iden
        self.name = name
        self.topics = topics
        self.city = city
        self.country = country
        self.date = attendees
        self.general_chair = general_chair,
        self.attendees = attendees
        self.information = information


####################################################################
# Example:
conferences_list = [Conference(1, 'ICGSE', ['global software development'], 'Madrid', 'Spain', '12-5-19', 'Chad Smith', attendees_list[0:2], 'info'),
                    Conference(2, 'HCIC', ['m-Health', 'hci'], 'Berlin', 'Germany', '5-7-20', 'Michael Flea', attendees_list[0:1], 'info')]

####################################################################

conferences_api = Blueprint('conferences_api', __name__)

# Devuelve el listado de congresos
@conferences_api.route('/v1/conferences/', methods=['GET'])
def getConferences():
    return jsonify({'conferences': conferences_list})

# Devuelve los datos de un congreso
@conferences_api.route('/v1/conferences/<int:conference_id>/', methods=['GET'])
def getOneConference(conference_id):
    for conference in conferences_list:
        if conference.iden == conference_id:
            return jsonify({'conference': conference})
    abort(404)

# Devuelve conferencias relacionadas con una tematica concreta
@conferences_api.route('/v1/conferences/about/<string:topic>/', methods=['GET'])
def getByTopic(topic):
    results = []
    for conference in conferences_list:
        if topic in conference.topics:
            results.append(conference)
    if len(results) > 0:
        return jsonify({'conferences about {0}'.format(topic): results})
    else:
        return make_response(jsonify({'warning': 'No conferences about {0} found'.format(topic)}))


# Crea un nuevo congreso
@conferences_api.route('/v1/conference/', methods=['POST'])
def createConference():
    if not request.json or not 'iden' in request.json:
        abort(404)

    iden = request.json.get('iden')
    name = request.json.get('name')
    topics = request.json.get('topics')
    city = request.json.get('city')
    country = request.json.get('country')
    date = request.json.get('date')
    general_chair = request.json.get('general_chair')
    attendees = request.json.get('attendees')
    information = request.json.get('information')

    conference = Conference(iden, name, topics, city,
                            country, date, general_chair, attendees, information)
    conferences_list.append(conference)
    return jsonify({'conference': conference}), 201

# Actualiza los datos de un congreso
@conferences_api.route('/v1/conferences/<int:conference_id>/', methods=['PUT'])
def updateConference(conference_id):
    conference = [
        conference for conference in conferences_list if conference.iden == conference_id]
    conference[0]['name'] = request.json.get('name', conference[0]['name'])
    conference[0]['topics'] = request.json.get(
        'topics', conference[0]['topics'])
    conference[0]['city'] = request.json.get('city', conference[0]['city'])
    conference[0]['country'] = request.json.get(
        'country', conference[0]['country'])
    conference[0]['date'] = request.json.get('date', conference[0]['date'])
    conference[0]['general_chair'] = request.json.get(
        'general_chair', conference[0]['general_chair'])
    conference[0]['attendees'] = request.json.get(
        'attendees', conference[0]['attendees'])
    conference[0]['information'] = request.json.get(
        'information', conference[0]['information'])

    return jsonify({'conference': conference[0]})

# Borrar un congreso
@conferences_api.route('/v1/conferences/<int:conference_id>/', methods=['DELETE'])
def deleteConference(conference_id):
    conference = [
        conference for conference in conferences_list if conference.iden == conference_id]
    conferences_list.remove(conference[0])
    return jsonify({}), 204  # No content

# Manejo errores 404
@conferences_api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
