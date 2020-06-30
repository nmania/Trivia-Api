import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432',
                                                       self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operationand for
    expected errors.
    """

    def test_retrieve_categories(self):
        """
        get categories endpoint test function
        """
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'])

    def test_retrieve_questions(self):
        """
        get questions endpoint test function
        """
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(data['categories'])

    def test_retrieve_questions_422(self):
        """
        get questions endpoint error test function
        """

        response = self.client().get('/questions?page=5000')
        data = json.loads(response.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable')
        self.assertTrue(data['error'], 422)

    def test_delete_questions_422(self):
        """
        delete questions endpoint error test function
        """
        response = self.client().delete('questions/5000')
        data = json.loads(response.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable')
        self.assertTrue(data['error'], 422)

    def test_delete_questions(self):
        """
        delete questions endpoint test function
        """
        response = self.client().delete('questions/6')
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_create_question(self):
        """
        questions creation endpoint test function
        """
        new_question = {
            'question': 'test question',
            'answer': 'test_answer',
            'category': 1,
            'difficulty': '1'
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_message'], 'OK')

    def test_create_question_422(self):
        """
        questions creation endpoint error test function
        """
        new_question = {
            'question': '',
            'answer': '',
            'category': 1,
            'difficulty': ''
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_questions_by_cat(self):
        """
        get questions by category endpoint test function
        """
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_message'], 'OK')

    def test_questions_by_cat_422(self):
        """
        get questions by category error endpoint test function
        """
        response = self.client().get('/categories/5000/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_questions_search(self):
        """
        questions search endpoint test function
        """
        response = self.client().post('/questions_by_phrase',
                                      json={'searchTerm': "did"})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_message'], 'OK')

    def test_questions_search_400(self):
        """
        questions search endpoint error test function
        """
        response = self.client().post('/questions_by_phrase',
                                      json={'searchTerm': "abcdefghijklmn"})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_play_quizz(self):
        """
        play quizz endpoint test function
        """
        response = self.client().post('/quizzes',
                                      json={'previous_questions': [],
                                            'quiz_category': {'type': 'History',  # noqa
                                                              'id': '3'
                                                              }
                                            })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_message'], 'OK')

    def test_play_quizz_404(self):
        """
        play quizz endpoint error test function
        """
        response = self.client().post('/quizzes',
                                      json={'previous_questions': [],
                                            'quiz_category': {'type': 'abcde',
                                                              'id': '9999'
                                                              }
                                            })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
