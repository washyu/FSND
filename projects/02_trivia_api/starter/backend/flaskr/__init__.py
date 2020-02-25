import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  @app.route('/api/categories')
  def get_categories():
    categories = Category.query.all()
    formated_categorys = {}
    for category in categories:
        formated_categorys[category.id] = category.type
    
    if formated_categorys:
      return jsonify({
        'success': True,
        'categories': formated_categorys
      })
    abort(404)

  @app.route('/api/questions', methods=['GET','POST'])
  def questions():
    if request.method == 'GET':
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE 
      end = start + QUESTIONS_PER_PAGE

      questions = Question.query.all()
      formated_questions = [question.format() for question in questions]

      categories = Category.query.all()
      formated_categorys = {}
      for category in categories:
          formated_categorys[category.id] = category.type

      if formated_questions and formated_categorys:
        return jsonify({
          'success': True,
          'questions': formated_questions[start:end],
          'categories': formated_categorys,
          'total_questions': len(formated_questions),
          'current_category': 1
        })
      #if we didn't return then there probably was an issue 
      abort(422)

    if request.method == 'POST':
      question_json = request.get_json()
      
      # If this is a search post we should have a search term
      if 'searchTerm' in question_json:
        if not question_json['searchTerm']:
          abort(422)

        search_term = question_json['searchTerm']
        questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

        return jsonify({
          'success': True,
          'questions': [question.format() for question in questions],
          'totalQuestions': len(questions),
          'currentCategory': 1
        })

      if set(('question', 'answer', 'category', 'difficulty')) == question_json.keys():
        question = Question(question_json['question'],
                            question_json['answer'],
                            question_json['category'],
                            question_json['difficulty'])
      else:
        abort(422)
      try:
        question.insert()

        return jsonify({
          'success': True
        })
      except Exception as e:
        abort(422)

  @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter_by(id = question_id).first()

    if question:
      try:
        question.delete()
        return jsonify({
          'success': True
        })
      except Exception as e:
        abort(422)
    else:
      abort(404)
    
  @app.route('/api/categories/<int:category_id>/questions', methods=['GET'])
  def get_question(category_id):
      questions = Question.query.filter_by(category = category_id).all()
      formated_questions = [question.format() for question in questions]
      
      if formated_questions:
        return jsonify({
          'success': True,
          'questions': formated_questions,
          'current_category': str(category_id),
          'total_questions': len(formated_questions)
        })
      abort(404)

  @app.route('/api/quizzes', methods=["POST"])
  def get_quizzes():
    quiz_json = request.get_json()
    previous_questions = quiz_json['previous_questions']
    category = quiz_json['quiz_category']['id']

    question = Question.query.filter_by(
      category = category
      ).filter(
        ~Question.id.in_(previous_questions)
      ).order_by(func.random()).first()

    if question:
      return jsonify({
        'success': True,
        'question': question.format() if question else None 
      })
    abort(404)
  
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Not Found'
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'
    }), 422

  return app

    