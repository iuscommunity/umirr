import math

def get_distance(coordinate1, coordinate2):
    a = {}
    b = {}
    a['latitude'], a['longitude'] = coordinate1
    b['latitude'], b['longitude'] = coordinate2
    a['phi'] = math.radians(90.0 - float(a['latitude']))
    b['phi'] = math.radians(90.0 - float(b['latitude']))
    a['theta'] = math.radians(float(a['longitude']))
    b['theta'] = math.radians(float(b['longitude']))
    arc = math.acos(math.sin(a['phi']) *
                    math.sin(b['phi']) *
                    math.cos(a['theta'] - b['theta']) +
                    math.cos(a['phi']) *
                    math.cos(b['phi']))
    return arc * 3960
