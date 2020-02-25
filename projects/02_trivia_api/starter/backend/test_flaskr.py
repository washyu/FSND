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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Test question',
            'answer': 'Test answer',
            'category': 1,
            'difficulty': 1
        }

        self.search_question = {
            'searchTerm': 'Test question'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_can_get_catagories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(len(data['categories']), 0)

    def test_try_to_delete_an_invalid_question(self):
        res = self.client().delete('/api/questions/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_new_question(self):
        res = self.client().post('/api/questions', json = self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_question(self):
        res = self.client().post('/api/questions', json = self.search_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreaterEqual(len(data['questions']), 1)

    def try_to_delete_a_valid_question(self):
        res = self.client().delete('/api/questions/5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_getting_quetions_page_returns_different_quetions(self):
        res = self.client().get('/api/questions?page=1')
        page1 = json.loads(res.data)
        res = self.client().get('/api/questions?page=2')
        page2 = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(page1['questions'])
        self.assertTrue(len(page1['questions']))
        self.assertTrue(page2['questions'])
        self.assertTrue(len(page2['questions']))
        self.assertNotEqual(page1, page2)

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()