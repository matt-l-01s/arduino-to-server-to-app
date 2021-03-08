import json

entrance_button =
exit_button =

buttonpress_json = {}
buttonpress_json['type'] = 'FeatureCollection'
buttonpress_json['metadata'] = {'count':6}
buttonpress_json['features'] = []

buttonpress_json['features'].append({
    'type': 'Feature',
    'properties': {
        'Number of Visitors': str(entrance_button - exit_button),
        'Name': 'UCSI'
    },
    'geometry': {
        'type': 'Point',
        'coordinates': [101.733216,3.079548]
    },
    'id': 'ucsi1'
}
)

with open('buttonpress.json', 'w') as jsonFile:
    json.dump(buttonpress_json, jsonFile)