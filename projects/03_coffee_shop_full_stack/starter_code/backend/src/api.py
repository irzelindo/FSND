import json

from flask import Flask, request, jsonify, abort
from flask_cors import CORS

from .auth.auth import requires_auth
from .database.models import setup_db, Drink

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES
'''
    GET /
    returns the main page
'''


@app.route('/')
def index():
    print('Hello')
    return 'Hello'


'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks')
def get_drinks():
    all_drinks = Drink.query.all()
    drinks = [drink.short() for drink in all_drinks]
    # print(all_drinks)
    return jsonify({
        'success': True,
        'status_code': 200,
        'drinks': drinks
    })



'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drink_details():
    all_drinks = Drink.query.all()
    drinks = [drink.long() for drink in all_drinks]
    # print(drinks)
    return jsonify({
        'success': True,
        'status_code': 200,
        'drinks': drinks
    })



'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drinks():
    all_drinks = Drink.query.all()
    drinks = [drink.short() for drink in all_drinks]
    titles = [drink.get("title").lower() for drink in drinks]
    # print(titles)
    data = request.get_json()
    title = data.get("title")
    recipe = json.dumps(data.get("recipe"))
    drink = Drink()
    drink.title = title
    drink.recipe = str(recipe)
    if title.lower() not in titles:
        drink.insert()
        drink_id = drink.id
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        drink = drink.long()
        # print(drink)
        return jsonify({
            'success': True,
            'status_code': 200,
            'drinks': drink
        })
    else:
        return jsonify({
            'success': False,
            'status_code': 200,
            'drinks': 'This drink already exists update it instead'
        })


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drinks(drink_id):
    data = request.get_json()
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    # print(drink)
    drink.title = data.get('title')
    drink.recipe = str(json.dumps(data.get('recipe')))
    drink.update()
    drink = Drink.query.filter(Drink.id == drink.id).one_or_none()

    drink = drink.long()

    return jsonify({
        'success': True,
        'status_code': 200,
        'drinks': list(drink)
    })


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id}
        where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(drink_id):

    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if drink:
        drink.delete()

        return jsonify({
            'success': True,
            'status_code': 200,
            'drinks': drink_id
        })
    else:
        return jsonify({
            'success': False,
            'status_code': 200,
            'drinks': 'This drink does not exist'
        })


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable_request(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
error handler should conform to general task above
'''


@app.errorhandler(404)
def not_found_request(error):
    """ Returns 404 Resource not found Error """
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource Not Found"
    }), 404


'''
@TODO implement error handler for AuthError
error handler should conform to general task above
'''


@app.errorhandler(401)
def unauthorized_request(error):
    """ Returns 401 Unauthorized authentication required Error """
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized! authentication required"
    }), 401


# @app.errorhandler(403)
# def forbidden_request(error):
#     """ Returns 403 Forbidden Authorization Required Error """
#     return jsonify({
#         "success": False,
#         "error": 403,
#         "message": "Forbidden! Authorization Required"
#     }), 403
