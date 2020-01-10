from flask import Flask

from api.v1.conferences import conferences_api, Conference
from api.v1.attendees import attendees_api, Attendee
from api.v1.presentations import presentations_api, Presentation
from api.v1.devices import devices_api, Device

from flask.json import JSONEncoder


class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Conference):
            return {
                'iden': obj.iden,
                'name': obj.name,
                'topics': obj.topics,
                'city': obj.city,
                'country': obj.country,
                'date': obj.date,
                'general_chair': obj.general_chair,
                'attendees': obj.attendees,
                'information': obj.information
            }
        if isinstance(obj, Attendee):
            return {
                'iden': obj.iden,
                'name': obj.name,
                'surname': obj.surname,
                'institution': obj.institution,
                'languages': obj.languages,
                'country': obj.country,
                'research_in': obj.research_in,
                'is_lecturer': obj.is_lecturer,
                'clicker_id': obj.clicker_id
            }
        if isinstance(obj, Presentation):
            return {
                'iden': obj.iden,
                'title': obj.title,
                'date': obj.date,
                'hour': obj.hour,
                'lecturer': obj.lecturer,
                'authors': obj.authors,
                'topics': obj.topics,
                'place': obj.place
            }
        if isinstance(obj, Device):
            return {
                'MAC': obj.MAC,
                'model': obj.model,
                'firmware': obj.firmware,
                'battery_level': obj.battery_level,
                'deep_sleep': obj.deep_sleep
            }
        return super(MyJSONEncoder, self).default(obj)


app = Flask(__name__, static_url_path="")
app.json_encoder = MyJSONEncoder

# Blueprint
app.register_blueprint(conferences_api)
app.register_blueprint(attendees_api)
app.register_blueprint(presentations_api)
app.register_blueprint(devices_api)


@app.route('/')
def root():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True)
