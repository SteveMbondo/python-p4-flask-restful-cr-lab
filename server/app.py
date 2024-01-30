#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plant_dict = [plant.to_dict() for plant in Plant.query.all()]

        response = make_response(
            jsonify(plant_dict), 200
        )
        response.headers['Content-Type'] = 'application/json'

        return response
    
    def post(self):
    try:
        new_plant = Plant(
            name=request.form['name'],
            image=request.form['image'],
            price=request.form['price']
        )
        db.session.add(new_plant)
        db.session.commit()

        new_plant_dict = new_plant.to_dict()
        response = make_response(
            jsonify(new_plant_dict), 201
        )
        response.headers['Content-Type'] = 'application/json'

        return response
    except Exception as e:
        # Log or print the exception to identify the issue
        print(f"Error: {e}")
        db.session.rollback()  # Rollback changes in case of an error
        return make_response(jsonify({"error": "Failed to create plant record"}), 500)

    
api.add_resource(Plants, '/plants')


class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()

        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}), 404)

        response = make_response(
            jsonify(plant), 200
        )
        response.headers['Content-Type'] = 'application/json'

        return response
        
api.add_resource(PlantByID, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
