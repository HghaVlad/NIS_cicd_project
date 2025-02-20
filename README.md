# The simple FLask app for working with Users

A simple Flask app with CRUD operations for users using PostgreSQL.

---
## Using
### How to start?
1. Ensure you have installed the docker and docker-compose
2. Make .env file using the example from .env.example
3. Run `docker-compose up -d`
<br>Well. The project started!

### How to end?
1. Write `docker-compose down`
<br>The project stopped.


## Available methods
| Method | Endpoint          | Description               |
|--------|-------------------|---------------------------|
| GET    | `/ping`           | Check server availability |
| GET    | `/users`          | Get all users             |
| GET    | `/users/<user_id>`| Get a user by ID          |
| POST   | `/users`          | Create a new user         |
| PUT    | `/users/<user_id>`| Update a user by ID       |
| DELETE | `/users/<user_id>`| Delete a user by ID       |


* Made by Vlad Bukharin 
* БПИ-249-2