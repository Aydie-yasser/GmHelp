pause_request_schema = {
    'type': 'object',
    'properties': {
        'PlyID': {"minimum": 1},
        'Tkn': {'type': 'string',"minLength": 0},
        'DevID': {'type': 'string',"minLength": 0},
        'source': {'type': 'string',"minLength": 0},
        'ProjectKey': {'type': 'string',"minLength": 2},
        'ProjectSecret': {'type': 'string',"minLength": 2},
        'StartDate' : {'type': 'string'},
        'EndDate' : {'type': 'string'}
    },
    'required': ['PlyID','Tkn','DevID','ProjectKey','ProjectSecret','StartDate']
}
