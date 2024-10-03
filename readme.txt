# API Documentation for Kitten Exhibition

## User Registration
### Endpoint
- **POST** `/register/`

### Description
This endpoint allows a new user to register by providing their desired username and password. It's essential for user authentication within the application.

### Request Body
{
    "username": "string",  // Required: Unique username for the user.
    "password": "string"   // Required: Password for the user account. Should be kept secure.
}

### Parameters
- **username:** Required and must be unique across all users in the system.
- **password:** Required; should be securely stored (hashed) in the database.

### Response
- **201 Created:** Registration successful, returns user details (excluding sensitive information).
{
    "id": 1,
    "username": "new_user"
}
- **400 Bad Request:** Validation errors (e.g., username taken).
{
    "error": "This username is already taken."
}

## User Login
### Endpoint
- **POST** `/login/`

### Description
Allows an existing user to log in with their username and password, returning JWTs for access.

### Request Body
{
    "username": "string",  // Required: Username of the user.
    "password": "string"   // Required: User's account password.
}

### Parameters
- **username:** Required; must match the registered username.
- **password:** Required; correct password is needed.

### Response
- **200 OK:** Successful login returns access and refresh tokens.
{
    "access": "string",   // Access token for future requests.
    "refresh": "string"   // Refresh token for obtaining a new access token.
}
- **401 Unauthorized:** Invalid credentials.
{
    "error": "Invalid username or password."
}

## Kitten Management
### List Kittens
#### Endpoint
- **GET** `/kittens/`

### Description
Retrieve a list of all kittens in the exhibition.

### Response
- **200 OK:** Returns a list of kittens.
[
    {
        "id": 1,
        "name": "Fluffy",
        "age_months": 2,
        "breed": "Persian",
        "color": "White"
    },
    ...
]

### Create Kitten
#### Endpoint
- **POST** `/kittens/`

### Description
Create a new kitten entry.

### Request Body
{
    "name": "string",  // Required: Name of the kitten.
    "age_months": "integer",  // Required: Age of the kitten in months.
    "breed": "string", // Required: Breed of the kitten.
    "color": "string"  // Required: Color of the kitten.
}

### Response
- **201 Created:** Returns the created kitten details.
{
    "id": 1,
    "name": "Fluffy",
    "age_months": 2,
    "breed": "Persian",
    "color": "White"
}
- **400 Bad Request:** Validation errors (e.g., invalid age).
{
    "error": "Invalid age value."
}

### Retrieve Kitten
#### Endpoint
- **GET** `/kittens/{id}/`

### Description
Retrieve a specific kitten's details by ID.

### Response
- **200 OK:** Returns the kitten details.
{
    "id": 1,
    "name": "Fluffy",
    "age_months": 2,
    "breed": "Persian",
    "color": "White"
}
- **404 Not Found:** Kitten does not exist.
{
    "error": "Kitten not found."
}

### Update Kitten
#### Endpoint
- **PATCH** `/kittens/{id}/`

### Description
Update a specific kitten's information.

### Request Body
{
    "name": "string",  // Optional: Updated name of the kitten.
    "age_months": "integer",  // Optional: Updated age of the kitten in months.
    "breed": "string", // Optional: Updated breed of the kitten.
    "color": "string"  // Optional: Updated color of the kitten.
}

### Response
- **200 OK:** Returns the updated kitten details.
{
    "id": 1,
    "name": "Fluffy",
    "age_months": 3,
    "breed": "Persian",
    "color": "White"
}
- **400 Bad Request:** Validation errors.
{
    "error": "Invalid age value."
}
- **404 Not Found:** Kitten does not exist.
{
    "error": "Kitten not found."
}

### Delete Kitten
#### Endpoint
- **DELETE** `/kittens/{id}/`

### Description
Delete a specific kitten by ID.

### Response
- **204 No Content:** Successful deletion.
- **404 Not Found:** Kitten does not exist.
{
    "error": "Kitten not found."
}

## Rating Kittens
### List Ratings
#### Endpoint
- **GET** `/kittens/{id}/ratings/`

### Description
Retrieve a list of all ratings for a specific kitten.

### Response
- **200 OK:** Returns a list of ratings.
[
    {
        "id": 1,
        "kitten_id": 1,
        "user": "string",
        "score": 5,
    },
    ...
]

### Create Rating
#### Endpoint
- **POST** `/kittens/{id}/ratings/`

### Description
Submit a new rating for a specific kitten.

### Request Body
{
    "score": "integer",  // Required: Rating score (1 to 5).
}

### Response
- **201 Created:** Returns the created rating.
{
    "id": 1,
    "kitten_id": 1,
    "user": "string",
    "score": 5,
}
- **400 Bad Request:** Validation errors.
{
    "error": "Score must be between 1 and 5."
}

### Update Rating
#### Endpoint
- **PUT** `/kittens/{kitten_id}/ratings/`

### Description
Update a specific rating for a kitten.

### Request Body
{
    "score": "integer",  // Optional: Updated rating score.
}

### Response
- **200 OK:** Returns the updated rating.
{
    "id": 1,
    "kitten_id": 1,
    "user": "string",
    "score": 4,
}
- **400 Bad Request:** Validation errors.
{
    "error": "Score must be between 1 and 5."
}
- **404 Not Found:** Rating does not exist.
{
    "error": "Rating not found."
}

### Delete Rating
#### Endpoint
- **DELETE** `/kittens/{kitten_id}/ratings/`

### Description
Delete a specific rating for a kitten.

### Response
- **204 No Content:** Successful deletion.
- **404 Not Found:** Rating does not exist.
{
    "error": "Rating not found."
}

## Swagger UI
The API documentation can be accessed via Swagger UI for interactive testing and exploration.

### Accessing Swagger UI
- Open your browser and navigate to `/swagger/` to view the API documentation.
