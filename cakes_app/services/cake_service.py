"""
Cake Service Module

This module defines the CakeService class, which provides methods for managing cake-related
operations, including listing cakes, retrieving cakes by ID, adding new cakes, deleting cakes,
and updating existing cakes.
"""

import uuid
from bson import json_util


class CakeService:
    """
    Service class for managing cake-related operations.

    This class provides methods for listing cakes, retrieving cakes by ID, adding new cakes,
    deleting cakes, and updating existing cakes.

    Methods:
        get_all_cakes(cake_collection): Get a list of all cakes.
        get_cake_by_id(cake_collection, cake_id): Get a specific cake by its UUID.
        add_cake(cake_collection, data): Add a new cake with a UUID.
        delete_cake(cake_collection, cake_id): Delete a cake by ID.
        update_cake(cake_collection, cake_id, data): Update a cake by ID.
    """

    @staticmethod
    def get_all_cakes(cake_collection):
        """
        Get a list of all cakes.

        :param cake_collection: The MongoDB collection for cakes.
        :return: A list of cakes.
        """
        cakes = list(cake_collection.find({},
                                          {"_id": 1, "name": 1, "comment": 1, "imageUrl": 1,
                                           "yumFactor": 1}))
        # Convert ObjectId to string
        for cake in cakes:
            cake["_id"] = str(cake["_id"])
        return cakes

    @staticmethod
    def get_cake_by_id(cake_collection, cake_id):
        """
        Get a specific cake by its UUID.

        :param cake_collection: The MongoDB collection for cakes.
        :param cake_id: The UUID of the cake to retrieve.
        :return: A cake with its ID, or None if not found.
        """
        try:
            # Parse the UUID string
            cake = cake_collection.find_one({"_id": str(cake_id)})
            return json_util.dumps(cake) if cake else None
        except ValueError:
            return {"message": "Cake not found"}, 404

    @staticmethod
    def add_cake(cake_collection, data):
        """
        Add a new cake with a UUID.

        :param cake_collection: The MongoDB collection for cakes.
        :param data: The data of the
        cake to be added (excluding the _id field). :return: A JSON response indicating the
        success of the operation, a "bad request" message for missing or extra fields,
        or a "server error" message for database issues.
        """
        # Check if all required fields are present
        required_fields = ['name', 'comment', 'imageUrl', 'yumFactor']
        if not all(field in data for field in required_fields):
            return {"message": "Missing required fields in the data"}, 400

        # Check for unexpected fields
        allowed_fields = required_fields + ["_id"]  # Add any additional allowed fields here
        unexpected_fields = [field for field in data if field not in allowed_fields]
        if unexpected_fields:
            return {"message": f"Unexpected fields: {', '.join(unexpected_fields)}"}, 400

        # Include the UUID in the cake data
        data["_id"] = str(uuid.uuid4())

        # Insert the cake into the collection
        try:
            cake_collection.insert_one(data)
            return {"message": "Cake added successfully", "_id": data["_id"]}
        except Exception as e:
            return {"message": "Server error while adding the cake", "error": str(e)}, 500

    @staticmethod
    def delete_cake(cake_collection, cake_id):
        """
        Delete a cake by ID.

        :param cake_collection: The MongoDB collection for cakes.
        :param cake_id: The ID of the cake to delete.
        :return: A JSON response indicating the success of the operation or a "not found" message.
        """
        result = cake_collection.delete_one({"_id": cake_id})
        if result.deleted_count == 1:
            return {"message": "Cake deleted successfully"}
        return {"message": "Cake not found"}, 404

    @staticmethod
    def update_cake(cake_collection, cake_id, data):
        """
        Update a cake by ID.

        :param cake_collection: The MongoDB collection for cakes.
        :param cake_id: The UUID of the cake to update.
        :param data: The data for updating the cake. It can be a dictionary with fields to update.
        :return: A JSON response indicating the success of the operation or a "not found" message.
        """
        existing_cake = cake_collection.find_one({"_id": str(cake_id)})

        if existing_cake is not None:
            existing_cake.update(data)
            cake_collection.find_one_and_replace({"_id": str(cake_id)}, existing_cake)
            return {"message": "Cake updated successfully"}
        return {"message": "Cake not found"}, 404
