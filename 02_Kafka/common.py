import json
TOPIC = 'traffic-sensors'
def classify(event):
    if not isinstance(event.get('speed_kmh'), (int, float)) or not isinstance(event.get('vehicles'), int):
        raise ValueError('speed_kmh and vehicles must be numeric')
    return event['speed_kmh'] < 25 and event['vehicles'] >= 30

def decode(data):
    obj = json.loads(data)
    if not isinstance(obj, dict):
        raise ValueError('event must be an object')
    return obj
