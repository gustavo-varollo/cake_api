# Cake API

The Cake API is a RESTful web service that allows to manage and interact with cake data. This API provides endpoints for listing cakes, adding new cakes, updating existing cakes, and deleting cakes.

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
  - [Docker Installation](#docker-installation)
  - [Local Installation](#local-installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
  - [Add a New Cake](#add-a-new-cake)
  - [Update a Cake](#update-a-cake)
  - [Delete a Cake](#delete-a-cake)
- [Swagger Documentation](#swagger-documentation)

## Features

- List all cakes in the database.
- Add a new cake to the database.
- Update an existing cake (with full or partial data).
- Delete a cake by its unique identifier.

## Getting Started

### Prerequisites

Before starting, make sure to have the following installed:

- Python
- Flask
- Flask-PyMongo
- MongoDB
- Docker

### Docker Installation

1. Make sure to have Docker and Docker Compose installed on the local machine.

2. Clone this repository to the local machine:

   ```bash
   git clone https://github.com/gustavo-varollo/cake_api.git
   ```
   
3. Build and run the Docker containers::

   ```bash
   docker-compose up --build
   ```

### Local Installation

1. Clone this repository to the local machine:

   ```bash
   git clone https://github.com/gustavo-varollo/cake-api.git
   ```
2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```
3. Start the Flask development server:

   ```bash
   python app.py
   ```
* For local MongoDB link the URI in instance/config.py for the MONGO_URI

## Usage

Interact with the API using HTTP requests. The primary endpoints are:

* **GET /cakes** - List all cakes.
* **POST /cakes** - Add a new cake.
* **PUT /cakes/{cake_id}** - Update an existing cake.
* **DELETE /cakes/{cake_id}** - Delete a cake.

## API Endpoints

* **List All Cakes**
* **URL: /cakes**
* **Method: GET**
* **Description:** Returns a list of all cakes.
* **Response**: A JSON array of cakes.

### Add a New Cake

* **URL:** /cakes
* **Method:** POST
* **Description:** Adds a new cake to the database.
* **Request Body:** JSON object with cake details.
* **Response:** A success message.

### Update a Cake

* **URL: /cakes/{cake_id}**
* **Method: PUT**
* **Description:** Updates an existing cake by its unique identifier (cake_id).
* **Request Body:** JSON object with cake details (full or partial).
* **Response:** A success message.

### Delete a Cake

* **URL: /cakes/{cake_id}**
* **Method: DELETE**
* **Description:** Deletes a cake by its unique identifier (cake_id).
* **Response:** A success message or a "not found" message (404).

## Swagger Documentation

* Detailed documentation of this API is available in Swagger format. Access it at 
http://localhost:8000/cake_api/swagger/swagger.json when the server is running. The Swagger documentation provides 
a comprehensive overview of the APIs endpoints, request parameters, and responses.
