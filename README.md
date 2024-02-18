# README for API Endpoints

## Overview

This documentation details the API endpoints for a notes application built using Flask for the backend, MySQL as the database, and JWT for authentication. The API is split into two main sections: Notes and Authentication, each with its endpoints for specific operations. The base URL for accessing the Notes API is `/api/v1/notes`, and for the Authentication API, it's `/api/v1/auth`.

## Deployment Details

-   **Application URL:** The application is deployed on Render at [https://neofi-notes-api.onrender.com](https://neofi-notes-api.onrender.com).
-   **Database Hosting:** The MySQL database is hosted on Clever Cloud.
  
Note: The backend and database are hosted on the free tier of their respective platforms. As a result, response times might exceed 30 seconds, especially if the service has been inactive for more than 10 minutes. This delay occurs because Render automatically spins down inactive services to conserve resources, and restarting them can take some time.

## Quick API Testing with Postman

To quickly test the API endpoints, you can use the provided Postman collection:

[Postman Collection Link](https://www.postman.com/telecoms-participant-25788623/workspace/public/collection/17892250-d1b30929-4fdc-48b9-be11-0bd583ead23e?action=share&creator=17892250)

This collection includes pre-configured requests for all the API endpoints, making it easier to test the functionality without manual setup.

## Setting Up the Project Locally

Follow these steps to set up the project locally:

1. **Clone the Repository**
   Clone the project repository to your local machine using the following command:

    ```
    git clone https://github.com/sachanayush47/notes-flask-app.git
    ```

2. **Install Requirements**
   Navigate to the project directory and install the required dependencies using:

    ```
    pip install -r requirements.txt
    ```

3. **Run Migrations**
   Initialize and apply the database migrations to set up your MySQL database structure:

    ```
    flask db init
    flask db migrate
    flask db upgrade
    ```

4. **Run the Server**
   Start the Flask server with the following command:
    ```
    flask run
    ```
    This will serve your API locally, and you can access it through the base URL provided by Flask, typically `http://127.0.0.1:5000/`.

## Technologies

-   **Backend Framework:** Flask
-   **Database:** MySQL
-   **Authentication:** JWT (JSON Web Tokens)

## Authentication

### Login

-   **Endpoint:** `/api/v1/auth/login`
-   **Method:** `POST`
-   **Description:** Authenticates a user and returns a token for subsequent requests.
-   **Request Body:**
    -   `username` (string): The user's username.
    -   `password` (string): The user's password.
-   **Response:** On successful login, returns user data (excluding the token) and sets the token in a cookie using `httponly` for security. On failure, returns an error message.

### Signup

-   **Endpoint:** `/api/v1/auth/signup`
-   **Method:** `POST`
-   **Description:** Registers a new user.
-   **Request Body:**
    -   `name` (string): The user's full name.
    -   `username` (string): The desired username.
    -   `password` (string): The desired password.
-   **Response:** Returns a message indicating the success or failure of the signup process.

## Notes

### Create Note

-   **Endpoint:** `/api/v1/notes/create`
-   **Method:** `POST`
-   **Description:** Allows authenticated users to create a new note.
-   **Authentication Required:** Yes
-   **Request Body:**
    -   `title` (string): The title of the note.
    -   `content` (string): The content of the note.
-   **Response:** Returns the created note's details along with the status code.

### Get Note

-   **Endpoint:** `/api/v1/notes/<int:note_id>`
-   **Method:** `GET`
-   **Description:** Retrieves the details of a specific note by its ID for the authenticated user.
-   **Authentication Required:** Yes
-   **Parameters:**
    -   `note_id` (int): The unique identifier of the note.
-   **Response:** Returns the requested note's details along with the status code.

### Update Note

-   **Endpoint:** `/api/v1/notes/<int:note_id>`
-   **Method:** `PUT`
-   **Description:** Updates the details of an existing note for the authenticated user.
-   **Authentication Required:** Yes
-   **Parameters:**
    -   `note_id` (int): The unique identifier of the note to be updated.
-   **Request Body:** A JSON object containing the fields to update.
-   **Response:** Returns the updated note's details along with the status code.

### Share Note

-   **Endpoint:** `/api/v1/notes/share`
-   **Method:** `POST`
-   **Description:** Allows authenticated users to share a note with other users.
-   **Authentication Required:** Yes
-   **Request Body:**
    -   `note_id` (int): The unique identifier of the note to be shared.
    -   `usernames` (array of strings): A list of usernames with whom the note should be shared.
-   **Response:** Returns a message indicating the success or failure of the sharing process along with the status code.

### Get Note Version History

-   **Endpoint:** `/api/v1/notes/version-history/<int:note_id>`
-   **Method:** `GET`
-   **Description:** Retrieves the version

history of a specific note for the authenticated user.

-   **Authentication Required:** Yes
-   **Parameters:**
    -   `note_id` (int): The unique identifier of the note.
-   **Response:** Returns a list of note versions along with the status code.

## Running Unit Tests

Ensure the reliability and functionality of the API with unit tests:

-   For authentication routes:
    ```
    python -m unittest tests/auth/test_auth_routes.py
    ```
-   For notes routes:
    ```
    python -m unittest tests/auth/test_notes_routes.py
    ```

## Authentication Required

Endpoints marked "Authentication Required" need users to be logged in with a valid token included in their request's header or a cookie.

## Status Codes

The API uses standard HTTP status codes for request outcomes:

-   `200 OK`: Request succeeded.
-   `201 Created`: New resource created successfully.
-   `400 Bad Request`: Invalid syntax in request.
-   `401 Unauthorized`: Missing or invalid authentication credentials.
-   `404 Not Found`: Resource not found.
