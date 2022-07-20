from flask import Blueprint
from flask_restful import Api
from landing_page.resources.lpage_resource import Home, CallBack, Email

# OAUTH_ENV= env_config("OAUTH_ENV")





lpage_bp = Blueprint("landing_page", __name__)

api = Api(lpage_bp)

api.add_resource(Home, '/')
api.add_resource(CallBack, '/callback')
api.add_resource(Email, '/email')


# api.add_resource(GetHandleFromJS, "/handle_reg")
# api.add_resource(Registration, "/register")