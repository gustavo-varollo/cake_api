"""
Cakes API Module

This module defines RESTful API endpoints for managing cakes. It provides functionality for
retrieving, adding, deleting, and updating cakes.
"""

from bson import json_util
from flask import request, Blueprint
from flask_restx import Resource, Api
from cakes_app import mongo
from cakes_app.models.cake import cake_model
from cakes_app.services.cake_service import CakeService

api = Api(
    Blueprint('cakes', __name__),
    version='1.0',
    title='Cakes API',
    description='API for managing cakes',
    doc='/cake_api/swagger/swagger.json',
)


@api.route('/cakes')
class Cakes(Resource):
    """
    Resource for managing cakes.

    This class defines endpoints for retrieving a list of all cakes and adding new cakes.

    Methods:
        get(self): Retrieve a list of all cakes.
        post(self): Add a new cake.

    Attributes:
        api (flask_restx.Api): The REST API used for defining endpoints.
    """

    @api.doc('Get all cakes')
    def get(self):
        """
        Get a list of all cakes.

        :return: A list of cakes.
        """
        return CakeService.get_all_cakes(mongo.db.cakes)

    @api.doc('Add a new cake')
    @api.expect(cake_model)
    def post(self):
        """
        Add a new cake.

        :return: A JSON response indicating the success of the operation.
        """
        data = request.get_json()
        result = CakeService.add_cake(mongo.db.cakes, data)
        return result


@api.route('/cakes/<string:cake_id>')
@api.doc(params={'cake_id': 'A cake ID'})
class Cake(Resource):
    """
    Resource for managing individual cakes.

    This class defines endpoints for retrieving, deleting, and updating an individual cake by its
    ID.

    Methods:
        get(self, cake_id): Retrieve a specific cake by ID.
        delete(self, cake_id): Delete a cake by ID.
        put(self, cake_id): Update a cake by ID.

    Attributes:
        api (flask_restx.Api): The REST API used for defining endpoints.
    """

    @api.doc('Get a cake by ID')
    def get(self, cake_id):
        """
        Get a specific cake by UUID.

        :param cake_id: The UUID of the cake to retrieve.
        :return: A cake with its ID, or a "not found" message.
        """
        cake = CakeService.get_cake_by_id(mongo.db.cakes, cake_id)
        if cake:
            return json_util.loads(cake)
        return {"message": "Cake not found"}, 404

    @api.doc('Delete a cake by ID')
    def delete(self, cake_id):
        """
        Delete a cake by ID.

        :param cake_id: The ID of the cake to delete.
        :return: A JSON response indicating the success of the operation or a "not found" message.
        """
        result = CakeService.delete_cake(mongo.db.cakes, cake_id)
        return result

    @api.doc('Update a cake by ID')
    @api.expect(cake_model)
    def put(self, cake_id):
        """
        Update a cake by ID.

        :param cake_id: The ID of the cake to update.
        :return: A JSON response indicating the success of the operation or a "not found" message.
        """
        data = request.get_json()
        result = CakeService.update_cake(mongo.db.cakes, cake_id, data)
        return result
