from flask import current_app as app, request
from flask_restful import Api, Resource
from app.recurrController import recurrController

class Router:
    """Basic Routes Handler"""

    def init_app_routes(self):
        api = Api(app)
        api.add_resource(App,"/PauseRecurr")

class App(Resource):
    """
    Application Requests Routes Handler
    """

    def post(self):
        route = request.url_rule.rule
        recurrcontroller  = recurrController()

        if route == "/PauseRecurr":
            return recurrcontroller.pause_recurr_game()
         
        return 'Hello from recurr module!'
