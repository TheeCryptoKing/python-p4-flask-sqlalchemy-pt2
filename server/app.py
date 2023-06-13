#!/usr/bin/env python3
from flask import Flask, make_response
# Flask is used to create the web application, and make_response is used to create HTTP responses.
from flask_migrate import Migrate
# Migrate is a Flask extension used for handling database migrations with SQLAlchemy.
from models import db, Pet, Owner

app = Flask(__name__)
# This line creates an instance of the Flask class and assigns it to the app variable. The __name__ argument is a special Python variable that represents the name of the current module.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# sqlite:///app.db': This line sets the configuration parameter SQLALCHEMY_DATABASE_URI to specify the SQLite database URI. In this case, it uses a SQLite database file named app.db.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# False: This line disables modification tracking for SQLAlchemy. Setting this to False can improve performance.

migrate = Migrate(app, db)
# his line initializes the Migrate extension with the Flask application (app) and the database connection (db).
db.init_app(app)
# This line initializes the database connection with the Flask application. It associates the SQLAlchemy db object with the Flask app.
@app.route('/')
# This line defines a route decorator for the root URL ("/"). It associates the following function with handling requests to this URL.
def index():
    response = make_response(
        '<h1>Welcome to the pet/owner directory!</h1>',
        200
    )
    return response
#  This line defines the handler function for the root URL ("/"). It creates an HTTP response with a welcome message.

@app.route('/pets/<int:id>')
def pet_by_id(id):
    # select method using query and filter 
    pet = Pet.query.filter(Pet.id == id).first()
# accesses the SQLAlchemy query object associated with the Pet model. applies a filter condition to the query. It specifies that the id column of the Pet table should match the provided id value. .first(): This executes the query and returns the first result that matches the filter condition. If no matching result is found, it returns None.
    if not pet:
        response_body = '<h1>404 pet not found</h1>'
        response = make_response(response_body, 404)
        return response

    response_body = f'''
        <h1>Information for {pet.name}</h1>
        <h2>Pet Species is {pet.species}</h2>
        <h2>Pet Owner is {pet.owner.name}</h2>
    '''

    response = make_response(response_body, 200)
    #  This function creates an HTTP response object with the specified response body and status code. In this case, response_body is the HTML content that will be sent as the response, and 200 is the status code indicating a successful response (HTTP status code 200 means "OK").
    

    return response
# This line defines a route decorator for URLs in the form "/owner/<id>", where <id> is a placeholder for the owner's ID. It associates the following function with handling requests to this URL.


@app.route('/owner/<int:id>')
def owner_by_id(id):
    owner = Owner.query.filter(Owner.id == id).first()

    if not owner:
        response_body = '<h1>404 owner not found</h1>'
        response = make_response(response_body, 404)
        return response

    response_body = f'<h1>Information for {owner.name}</h1>'

    pets = [pet for pet in owner.pets]

    if not pets:
        response_body += f'<h2>Has no pets at this time.</h2>'

    else:
        for pet in pets:
            response_body += f'<h2>Has pet {pet.species} named {pet.name}.</h2>'

    response = make_response(response_body, 200)

    return response



if __name__ == '__main__':
    app.run(port=5555, debug=True)
    # app.run(port=5555, debug=True): This line starts the Flask development server on port 5555 with debugging enabled.


