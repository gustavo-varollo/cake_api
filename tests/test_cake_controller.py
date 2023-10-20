"""
Cakes API Test Module

This module contains unit tests for the Cakes API, covering its functionality and endpoints. The
tests are designed to verify the correct behavior of the APIs core features, including listing
cakes, adding new cakes, deleting existing cakes by UUID, and updating cakes with partial or full
replacements.

The tests use Pytest and include fixtures for creating a test Flask app with a specific
configuration and a test client for making HTTP requests. Pytest mocker is used for mocking
dependencies to isolate the code under test.

Tested Endpoints:
- GET /cakes: List all cakes.
- POST /cakes: Add a new cake.
- DELETE /cakes/<cake_id>: Delete an existing cake by UUID.
- PUT /cakes/<cake_id>: Update an existing cake with partial or full changes.
"""

import uuid
import pytest

from cakes_app import create_app
from config.config import TestingConfig


class TestCakesAPIController:
    """
    Test class for the Cake API services.
    """
    @classmethod
    def setup_class(cls):
        cls.app = create_app(TestingConfig)
        cls.app.testing = True
        cls.client = cls.app.test_client()

    def test_list_cakes(self, mocker):
        """
        Test listing cakes via the /cakes endpoint.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the PyMongo database object
        mongo_mock = mocker.patch("cakes_app.controllers.cake_controller.mongo")
        # Mock the database response
        mongo_mock.db.cakes.find.return_value = [
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

        response = self.client.get("/cakes")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2

    def test_add_cake(self, mocker):
        """
        Test adding a new cake via the /cakes endpoint.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the PyMongo database object
        mongo_mock = mocker.patch("cakes_app.controllers.cake_controller.mongo")
        # Mock the database insertion
        mongo_mock.db.cakes.insert_one.return_value.acknowledged = True

        data = {
            "name": "Test Cake",
            "comment": "Test comment",
            "imageUrl": "test-image.jpg",
            "yumFactor": 3,
        }

        response = self.client.post("/cakes", json=data)
        assert response.status_code == 200

    def test_add_cake_missing_fields(self):
        """
        Test adding a new cake with missing required fields.
        """
        data = {
            "comment": "Test comment",
            "imageUrl": "test-image.jpg",
            "yumFactor": 3,
        }

        response = self.client.post("/cakes", json=data)
        assert response.status_code == 400
        assert response.get_json() == {"message": "Missing required fields in the data"}

    def test_add_cake_unexpected_fields(self):
        """
        Test adding a new cake with unexpected fields.
        """
        data = {
            "name": "Test Cake",
            "comment": "Test comment",
            "imageUrl": "test-image.jpg",
            "yumFactor": 3,
            "extraField": "This should not be here",
        }

        response = self.client.post("/cakes", json=data)
        assert response.status_code == 400
        assert response.get_json() == {"message": "Unexpected fields: extraField"}

    def test_delete_cake(self, mocker):
        """
        Test deleting a cake via the /cakes/<cake_id> endpoint.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the PyMongo database object
        mongo_mock = mocker.patch("cakes_app.controllers.cake_controller.mongo")

        # Add a cake to the database with a known ID
        known_id = str(uuid.uuid4())
        mongo_mock.db.cakes.find_one.return_value = {
            "_id": known_id,
            "name": "Cake 1",
            "comment": "Comment 1",
            "imageUrl": "image1.jpg",
            "yumFactor": 4,
        }

        # Mock the database deletion for a cake with the known ID
        mongo_mock.db.cakes.delete_one.return_value.deleted_count = 1

        response = self.client.delete(f"/cakes/{known_id}")
        assert response.status_code == 200
        assert response.get_json() == {"message": "Cake deleted successfully"}

    def test_delete_cake_not_found(self, mocker):
        """
        Test deleting a non-existent cake via the /cakes/<cake_id> endpoint.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the PyMongo database object
        mongo_mock = mocker.patch("cakes_app.controllers.cake_controller.mongo")
        # Mock the database deletion for a non-existent cake
        mongo_mock.db.cakes.delete_one.return_value.deleted_count = None

        response = self.client.delete("/cakes/123")
        assert response.status_code == 404

    def test_update_cake(self, mocker):
        """
        Test updating a cake via the /cakes/<cake_id> endpoint with a full replacement.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the PyMongo database object
        mongo_mock = mocker.patch("cakes_app.controllers.cake_controller.mongo")

        # Mock the database response to include at least one cake
        known_id = str(uuid.uuid4())
        existing_cake = {
            "_id": known_id,
            "name": "Cake 1",
            "comment": "Comment 1",
            "imageUrl": "image1.jpg",
            "yumFactor": 4,
        }
        mongo_mock.db.cakes.find_one.return_value = existing_cake

        data = {"name": "Updated Cake"}

        response = self.client.put(f"/cakes/{known_id}", json=data)
        assert response.status_code == 200
        assert response.get_json() == {"message": "Cake updated successfully"}

    def test_update_cake_partial(self, mocker):
        """
        Test updating a cake via the /cakes/<cake_id> endpoint with partial data.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the PyMongo database object
        mongo_mock = mocker.patch("cakes_app.controllers.cake_controller.mongo")

        # Mock the database response to include at least one cake
        known_id = str(uuid.uuid4())
        existing_cake = {
            "_id": known_id,
            "name": "Cake 1",
            "comment": "Comment 1",
            "imageUrl": "image1.jpg",
            "yumFactor": 4,
        }
        mongo_mock.db.cakes.find_one.return_value = existing_cake

        data = {"name": "New Cake Name"}

        response = self.client.put(f"/cakes/{known_id}", json=data)
        assert response.status_code == 200
        assert response.get_json() == {"message": "Cake updated successfully"}

    def test_update_cake_not_found(self, mocker):
        """
        Test updating a non-existent cake via the /cakes/<cake_id> endpoint.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the PyMongo database object
        mongo_mock = mocker.patch("cakes_app.controllers.cake_controller.mongo")
        # Mock the database response for a non-existent cake
        mongo_mock.db.cakes.find_one.return_value = None

        data = {"name": "Updated Cake"}

        response = self.client.put("/cakes/123", json=data)
        assert response.status_code == 404


if __name__ == "__main__":
    pytest.main()
