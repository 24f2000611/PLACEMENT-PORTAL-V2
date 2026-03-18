from flask_restful import Resource
from flask import request,jsonify , make_response
from Backend.user_datastore import user_datastore
from flask_security import utils,auth_token_required,roles_required
from Backend.models import *