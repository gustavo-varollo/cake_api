"""
Cakes Service Test Module

This module contains unit tests for the Cakes API services, covering functionality such as
retrieving cakes, adding new cakes, deleting cakes, and updating cakes. Pytest is used for
testing these services.
"""

import json
import uuid
from unittest import mock

import pytest
from cakes_app.services.cake_service import CakeService


class TestCakesAPIServices:
    """
    Test class for the Cake API services.
    """
    def test_get_all_cakes(self, mocker):
        """
        Test retrieving a list of all cakes.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the cake collection
        cake_collection = mocker.MagicMock()
        # Mock the list of cakes
        expected_cakes = [
            {
                "_id": "cake_id_1",
                "name": "Cake 1",
                "comment": "Comment 1",
                "imageUrl": "image1.jpg",
                "yumFactor": 4,
            },
            {
                "_id": "cake_id_2",
                "name": "Cake 2",
                "comment": "Comment 2",
                "imageUrl": "image2.jpg",
                "yumFactor": 5,
            },
        ]
        cake_collection.find.return_value = expected_cakes

        cakes = CakeService.get_all_cakes(cake_collection)

        assert cakes == expected_cakes

    def test_get_cake_by_id(self, mocker):
        """
        Test retrieving a cake by ID.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the cake collection
        cake_collection = mocker.MagicMock()
        # Mock the expected cake
        expected_cake = {
            "_id": "cake_id_1",
            "name": "Cake 1",
            "comment": "Comment 1",
            "imageUrl": "image1.jpg",
            "yumFactor": 4,
        }
        # Mock the find_one method
        cake_collection.find_one.return_value = expected_cake
        cake_id = str(uuid.uuid4())

        cake = json.loads(CakeService.get_cake_by_id(cake_collection, cake_id))

        assert cake == expected_cake

    def test_get_cake_by_id_not_found(self, mocker):
        """
        Test retrieving a non-existent cake by ID.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the cake collection
        cake_collection = mocker.MagicMock()
        # Mock the find_one method returning None
        cake_collection.find_one.return_value = None
        cake_id = str(uuid.uuid4())

        cake = CakeService.get_cake_by_id(cake_collection, cake_id)

        assert cake is None

    def test_add_cake(self, mocker):
        """
        Test adding a new cake.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the cake collection
        cake_collection = mocker.MagicMock()
        # Mock data for a new cake
        new_cake = {
            "name": "New Cake",
            "comment": "New Comment",
            "imageUrl": "new-image.jpg",
            "yumFactor": 5,
        }
        # Mock the insert_one method
        cake_collection.insert_one.return_value.acknowledged = True

        result = CakeService.add_cake(cake_collection, new_cake)

        assert result == {"message": "Cake added successfully", "_id": mock.ANY}

    def test_add_cake_missing_fields(self, mocker):
        """
        Test adding a new cake with missing required fields.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the cake collection
        cake_collection = mocker.MagicMock()
        # Mock data for a new cake with missing fields
        new_cake = {
            "comment": "New Comment",
            "imageUrl": "new-image.jpg",
            # YumFactor field is missing
        }

        result = CakeService.add_cake(cake_collection, new_cake)

        assert result == ({"message": "Missing required fields in the data"}, 400)

    def test_add_cake_unexpected_fields(self, mocker):
        """
        Test adding a new cake with unexpected fields.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the cake collection
        cake_collection = mocker.MagicMock()
        # Mock data for a new cake with an unexpected field
        new_cake = {
            "name": "New Cake",
            "comment": "New Comment",
            "imageUrl": "new-image.jpg",
            "yumFactor": 5,
            "extraField": "This should not be here",
        }

        result = CakeService.add_cake(cake_collection, new_cake)

        assert result == ({"message": "Unexpected fields: extraField"}, 400)

    def test_delete_cake(self, mocker):
        """
        Test deleting a cake by ID.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the cake collection
        cake_collection = mocker.MagicMock()
        # Mock the result of delete_one method
        cake_collection.delete_one.return_value.deleted_count = 1
        cake_id = str(uuid.uuid4())

        result = CakeService.delete_cake(cake_collection, cake_id)

        assert result == {"message": "Cake deleted successfully"}

    def test_delete_cake_not_found(self, mocker):
        """
        Test deleting a non-existent cake by ID.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the cake collection
        cake_collection = mocker.MagicMock()
        # Mock the result of delete_one method
        cake_collection.delete_one.return_value.deleted_count = 0
        cake_id = str(uuid.uuid4())

        result = CakeService.delete_cake(cake_collection, cake_id)

        assert result == ({"message": "Cake not found"}, 404)

    def test_update_cake(self, mocker):
        """
        Test updating a cake by ID.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the cake collection
        cake_collection = mocker.MagicMock()
        cake_id = str(uuid.uuid4())
        data = {"name": "Updated Cake"}
        # Mock the existing cake
        existing_cake = {
            "_id": cake_id,
            "name": "Cake 1",
            "comment": "Comment 1",
            "imageUrl": "image1.jpg",
            "yumFactor": 4,
        }
        # Mock the find_one method
        cake_collection.find_one.return_value = existing_cake
        # Mock the find_one_and_replace method
        cake_collection.find_one_and_replace.return_value = existing_cake

        result = CakeService.update_cake(cake_collection, cake_id, data)

        assert result == {"message": "Cake updated successfully"}

    def test_update_cake_not_found(self, mocker):
        """
        Test updating a non-existent cake by ID.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the cake collection
        cake_collection = mocker.MagicMock()
        # Mock the result of find_one method
        cake_collection.find_one.return_value = None
        cake_id = str(uuid.uuid4())
        data = {"name": "Updated Cake"}

        result = CakeService.update_cake(cake_collection, cake_id, data)

        assert result == ({"message": "Cake not found"}, 404)


if __name__ == "__main__":
    pytest.main()
