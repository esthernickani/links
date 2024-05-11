from unittest import TestCase

from app import app

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///link_test'
app.config['SQLALCHEMY_ECHO'] = False



class UserTestCase(TestCase):
    """tests for model for users"""
    def test_see_home(self):
        """can you see home"""

        with app.test_client() as client:
            resp = client.get('/')

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Brand Recognition', html)