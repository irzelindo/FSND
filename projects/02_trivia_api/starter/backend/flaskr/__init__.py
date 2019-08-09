import os
from flask import Flask, request, abort, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
CATEGORIES_PER_PAGE = 5

def questios_per_page(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = QUESTIONS_PER_PAGE * page
  questions = [question.format() for question in selection]
  current_questions = questions[start:end]
  return current_questions


def categories_per_page(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * CATEGORIES_PER_PAGE
  end = CATEGORIES_PER_PAGE * page
  categories = [category.format() for category in selection]
  current_categories = categories[start:end]
  return current_categories

def retrieve_questions(request):
  questions = Question.query.order_by(Question.id).all()
  current_questions = questios_per_page(request, questions)
  return questions, current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
  '''
  @DEFINING ERROR handlers functions
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Resource Not found"
        }), 404
        
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "Bad Request"
        }), 400

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "Unprocessable Request"
        }), 422

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    try:
      categories = Category.query.order_by(Category.id).all()
      current_categories = categories_per_page(request, categories)

      if len(categories) == 0:
            abort(404)
      else: 
        return jsonify({
          'success': True,
          'response': 200,
          'response_message': 'OK',
          'categories': current_categories,
          'total_categories': len(categories)
        })

    except:
      abort(404)  


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  '''

  @app.route('/questions')
  def get_questions():
    try:
      questions, current_questions = retrieve_questions(request)
      #questions = questios_per_page(request, selection)
      selection = Category.query.order_by(Category.id).all()
      categories = [category.type for category in selection]

      if len(questions) == 0:
            abort(404)
      else: 
        return jsonify({
          'success': True,
          'response': 200,
          'response_message': 'OK',
          'questions': current_questions,
          'total_questions': len(questions),
          'current_category': 2,
          'categories': categories
        })

    except:
      abort(404)  

  '''
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)
      else:
        question.delete()
        questions, current_questions = retrieve_questions(request)

      return jsonify({
        'success': True,
        'response': 200,
        'response_message': 'OK',
        'deleted': question_id,
        'questions': current_questions,
        'total_questions': len(questions)
      })
    except:
      abort(422)

  '''
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    