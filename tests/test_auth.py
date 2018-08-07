import logging
import unittest
import requests
from config import CURRENT_CONFIG

logging.basicConfig(level=logging.DEBUG)

class TestLogin(unittest.TestCase):
    """ Test login cases """

    CREDENTIALS = {
        'email': 'root@localhost',
        'password': 'toor'
    }

    def setUp(self):
        self.session = requests.session()
        self.session.headers['Content-Type'] = 'application/json'

    def _route(self, route):
        return "http://{}:{}{}".format(
            CURRENT_CONFIG.HOSTNAME,
            CURRENT_CONFIG.PORT,
            str(route)
        )

    def test_post_successful_login(self):
        """ Test that you can login """
        response = self.session.post(
            self._route("/auth/login"),
            json=self.CREDENTIALS
        )
        self.assertEqual(response.status_code, 200, response.text)

    def test_logout_without_login(self):
        """ Test that you cannot logout without prior login """
        response = self.session.get(
            self._route("/auth/logout"),
        )
        self.assertEqual(response.status_code, 401, response.text)

    def test_logout(self):
        """ Test that you can logout """
        response = self.session.post(
            self._route("/auth/login"),
            json=self.CREDENTIALS
        )
        self.assertEqual(response.status_code, 200, response.text)
        response = self.session.get(
            self._route("/auth/logout")
        )
        self.assertEqual(response.status_code, 200, response.text)

    def test_post_unsuccessful_credentials(self):
        """ Test that you can fail at login """
        response = self.session.post(
            self._route("/auth/login"),
            json=dict(self.CREDENTIALS, **{'password': '1234'})
        )
        self.assertEqual(response.status_code, 401, response.text)

    def test_post_wrong_type_credentials(self):
        """ Test that you cannot send just anything """

        response = self.session.post(
            self._route("/auth/login"),
            json=dict(self.CREDENTIALS, **{'password': 1234})
        )
        self.assertEqual(response.status_code, 400, response.text)
        response = self.session.post(
            self._route("/auth/login"),
            json=dict(self.CREDENTIALS, **{'password': None})
        )
        self.assertEqual(response.status_code, 400, response.text)
        response = self.session.post(
            self._route("/auth/login"),
            json=dict(self.CREDENTIALS, **{'password': ['toor']})
        )
        self.assertEqual(response.status_code, 400, response.text)

    def test_post_malformed(self):
        """ No malfored data """
        response = self.session.post(
            self._route("/auth/login"),
            data="{'username':'root','password',}"
        )
        self.assertEqual(response.status_code, 400, response.text)

    def test_put(self):
        """ Methods not allowed """
        response = self.session.put(
            self._route("/auth/login"),
            json=self.CREDENTIALS
        )
        self.assertEqual(response.status_code, 405, response.text)

    def test_delete(self):
        """ Methods not allowed """
        response = self.session.delete(
            self._route("/auth/login"),
            json=self.CREDENTIALS
        )
        self.assertEqual(response.status_code, 405, response.text)


    def test_get(self):
        """ Methods not allowed """
        response = self.session.get(
            self._route("/auth/login"),
            json=self.CREDENTIALS
        )
        self.assertEqual(response.status_code, 405, response.text)






def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestLogin("test_post_successful_login"))
    suite.addTest(TestLogin("test_logout"))
    suite.addTest(TestLogin("test_logout_without_login"))
    suite.addTest(TestLogin("test_post_successful_login"))
    suite.addTest(TestLogin("test_post_unsuccessful_credentials"))
    suite.addTest(TestLogin("test_post_wrong_type_credentials"))
    suite.addTest(TestLogin("test_post_malformed"))
    suite.addTest(TestLogin("test_put"))
    suite.addTest(TestLogin("test_delete"))
    suite.addTest(TestLogin("test_get"))
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
