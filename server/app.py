#!/usr/bin/env python3

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'instance/app.db')}")

from flask import Flask, make_response, jsonify, request, abort
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Activity, Camper, Signup

from werkzeug.exceptions import (
    HTTPException,
    BadRequest,
    UnprocessableEntity,
    InternalServerError,
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

# app.errorhandler(HTTPException)
# def handle_bad_request(error):
#     response = jsonify({"error": "404 Camper not found"})
#     response.status_code = 404
#     return response



@app.route('/')
def home():
    return '<h1>Home is where the heart is!<h1>'


class Campers(Resource):

    def get(self):
        camper = [camper.to_dict() for camper in Camper.query.all()]
        return make_response(jsonify(camper), 200)
    
    def post(self):
        data = request.get_json()
        if not data or "name" not in data or "age" not in data:
            return {"error": "400: Name and Age are required"}, 400
        try:
            camper = Camper(**data)
            db.session.add(camper)
            db.session.commit()
            return make_response(camper.to_dict(), 201)
        except:
            return {"error": "400: Validation error"}, 400


api.add_resource(Campers, '/campers')


class CamperById(Resource):
    def get(self, id):
        camper = Camper.query.get(id)
        if not camper:
            return {"error": "404: Camper not found"}, 404
        return make_response(camper.to_dict(), 200)
api.add_resource(CamperById,'/campers/<int:id>')



class Activities(Resource):
    def get(self):
        activity = [activity.to_dict() for activity in Activity.query.all()]
        return make_response(jsonify(activity), 202)

api.add_resource(Activities, '/activities')

class ActivityByID(Resource):
    def delete(self, id):
        try:
            activity = db.session.get(Activity, id)
            db.session.delete(activity)
            db.session.commit()
            return make_response("", 204)
        except:
            return {"error": "404: Camper not found"}, 404
api.add_resource(ActivityByID,'/activities/<int:id>')


class Signups(Resource):
    def get(self):
        signup = [signup.to_dict() for signup in Signup.query.all()]
        return make_response(jsonify(signup), 200)
    
    def post(self):
        data = request.get_json()
        try:
            signup = Signup(**data)
            db.session.add(signup)
            db.session.commit()
            return make_response(signup.to_dict(), 201)
        except:
            return {"error": "400: Validation error"}, 400
api.add_resource(Signups, '/signups')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
