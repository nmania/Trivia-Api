import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    '''
    questions paginator
    '''
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after
    completing the TODOs
    '''
    CORS(app)

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods",
                             "GET,PUT,POST,DELETE,OPTIONS")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories')
    def retrieve_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            cat_items = [(
                category.id, category.type) for category in categories]
            if len(cat_items) == 0:
                abort(404)

            else:
                return jsonify({
                    "success": True,
                    "status_code": 200,
                    "status_message": 'OK',
                    "categories": {key: value for (key, value) in cat_items},
                    "total_categories": len(categories)
                })

        except Exception:
            abort(422)

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for
    three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions')
    def retrieve_questions():
        try:
            questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)
            categories = Category.query.order_by(Category.id).all()
            cat_items = [(
                category.id, category.type) for category in categories]

            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                "success": True,
                "status_code": 200,
                "status_message": 'OK',
                "questions": current_questions,
                "total_questions": len(questions),
                "current_category": list(set([question['category'] for question in current_questions])),  # noqa
                "categories": {key: value for (key, value) in cat_items}
            })

        except Exception:
            abort(422)

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will
    be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)
            else:
                question.delete()
                questions = question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, questions)

            return jsonify({
                "success": True,
                "status_code": 200,
                "status_message": 'OK',
                "deleted": question_id,
                "questions": current_questions,
                "total_questions": len(questions)
            })

        except Exception:
            abort(422)

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the
    last page of the questions list in the "List" tab.
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        if body:
            question = body.get('question')
            answer = body.get('answer')
            category = body.get('category')
            dificulty = body.get('difficulty')

            # checking if form is empty
            if question == '' or answer == ''\
                    or category == ''\
                    or dificulty == '':
                abort(422)

            try:
                new_question = Question(question=question,
                                        answer=answer,
                                        category=category,
                                        difficulty=dificulty)
                new_question.insert()

                # clearing request body and temporal variables
                question, answer, category, dificulty = '', '', '', ''
                body.clear()

                questions = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, questions)

                categories = Category.query.order_by(Category.id).all()
                cat_items = [(
                    category.id, category.type) for category in categories]

                if len(current_questions) == 0:
                    abort(404)

                return jsonify({
                    "success": True,
                    "status_code": 200,
                    "status_message": "OK",
                    "questions": current_questions,
                    "total_questions": len(questions),
                    "current_category": list(set([question['category'] for question in current_questions])),  # noqa
                    "categories": {key: value for (key, value) in cat_items}
                })

            except Exception:
                abort(422)
        else:
            abort(422)

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/questions_by_phrase', methods=['POST'])
    def questions_search():
        body = request.get_json()
        phrase = '%{}%'.format(body.get('searchTerm'))

        try:
            questions = Question.query.filter(Question.question.
                                              ilike(phrase)).\
                                              order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)

            categories = Category.query.order_by(Category.id).all()
            cat_items = [(
                category.id, category.type) for category in categories]

            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                "success": True,
                'status_code': 200,
                "status_message": "OK",
                "questions": current_questions,
                "total_questions": len(questions),
                "current_category": list(set([question['category'] for question in current_questions])),  # noqa
                "categories": {key: value for (key, value) in cat_items}
            })

        except Exception:
            abort(400)

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<int:category_id>/questions')
    def questions_by_cat(category_id):
        try:
            questions = Question.query.filter(Question.category ==
                                              category_id).\
                                              order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)

            categories = Category.query.filter(Category.id == category_id).\
                order_by(Category.id).all()
            cat_items = [(
                category.id, category.type) for category in categories]

            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                "success": True,
                "status_code": 200,
                "status_message": "OK",
                "questions": current_questions,
                "total_questions": len(questions),
                "current_category": list(set([question['category'] for question in current_questions])),  # noqa
                "categories": {key: value for (key, value) in cat_items}
            })

        except Exception:
            abort(422)

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
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        category = body.get('quiz_category').get('id')
        prev_question = body.get('previous_questions')

        # play on all categories or an specific one:
        if category != 0:
            questions = Question.query.filter(Question.category == category)\
                                  .all()
        else:
            questions = Question.query.order_by(Question.id).all()

        questions = [question.format() for question in questions]

        if len(questions) == 0:
            abort(404)
        current_question = random.choice(questions)
        keep_playing = True

        try:
            while keep_playing:
                if current_question.get('id') not in prev_question:
                    return jsonify({
                            "success": True,
                            "status_code": 200,
                            "status_message": "OK",
                            "question": current_question
                        })
                else:
                    if len(questions) > len(prev_question):
                        current_question = random.choice(questions)
                    else:
                        keep_playing = False

            return jsonify({
                    "success": True,
                    "status_code": 200,
                    "status_message": "OK",
                    "question": current_question
            })

        except Exception:
            abort(400)

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(404)
    def not_found(error):
        """
        404 Error handler
        """
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        """
        400 Error handler
        """
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(422)
    def unprocessable_entity(error):
        """
        422 Error handler
        """
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    return app
