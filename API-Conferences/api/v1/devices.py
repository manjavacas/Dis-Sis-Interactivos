# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, abort, make_response, request


class Device:

    def __init__(self, MAC, model, firmware, battery_level, deep_sleep):
        self.MAC = MAC
        self.model = model
        self.firmware = firmware
        self.battery_level = battery_level
        self.deep_sleep = deep_sleep


####################################################################
# Example:
device_list = [Device('D8-D3-85-EA-1B-EE', 'Augmented Clicker', 'ver 1.0', 95, True),
               Device('05-A3-A5-BB-44-32', 'Augmented Clicker', 'ver. 1.1', 23, False)]

####################################################################

devices_api = Blueprint('devices_api', __name__)

# Devuelve el listado de devices
@devices_api.route('/v1/devices/', methods=['GET'])
def getDevices():
    return jsonify({'devices': device_list})

# Devuelve los datos de un device
@devices_api.route('/v1/devices/<string:device_MAC>/', methods=['GET'])
def getOneDevice(device_MAC):
    for device in device_list:
        if device.MAC == device_MAC:
            return jsonify({'device': device})
    abort(404)

# Crea un nuevo device
@devices_api.route('/v1/devices/', methods=['POST'])
def createDevice():
    if not request.json or not 'MAC' in request.json:
        abort(404)
    MAC = request.json.get('MAC')
    model = request.json.get('model')
    firmware = request.json.get('firmware')
    battery_level = request.json.get('battery_level')
    deep_sleep = request.json.get('deep_sleep')

    device = Device(MAC, model, firmware, battery_level, deep_sleep)
    device_list.append(device)
    return jsonify({'device': device}), 201

# Actualiza los datos de un device
@devices_api.route('/v1/devices/<string:device_id>/', methods=['PUT'])
def updateDevice(device_id):
    device = [
        device for device in device_list if device.MAC == device_id]
    device[0]['model'] = request.json.get('model', device[0]['model'])
    device[0]['firmware'] = request.json.get('firmware', device[0]['firmware'])
    device[0]['battery_level'] = request.json.get(
        'battery_level', device[0]['battery_level'])
    device[0]['deep_sleep'] = request.json.get(
        'deep_sleep', device[0]['deep_sleep'])

    return jsonify({'device': device[0]})

# Borrar un device
@devices_api.route('/v1/devices/<string:device_id>/', methods=['DELETE'])
def deleteDevice(device_id):
    device = [device for device in device_list if device.MAC == device_id]
    device_list.remove(device[0])
    return jsonify({}), 204  # No content

# Manejo errores 404
@devices_api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
