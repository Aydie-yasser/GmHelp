def error(message: str, code: int = 100):

    return {
        'Result': 'False',
        'error': {
            'code': code,
            'message': message
        },
        'message': message
    }
