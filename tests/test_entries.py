import logging
import unittest
import requests
from config import CURRENT_CONFIG
from api.models import Entry, User, get_session
from crypt import crypt

logging.basicConfig(level=logging.DEBUG)

class TestEntries(unittest.TestCase):
    """ Test login cases """

    CREDENTIALS = {
        'email': 'root@localhost',
        'password': 'toor'
    }

    def setUp(self):
        self.session = requests.session()
        self.session.headers['Content-Type'] = 'application/json'
        response = self.session.post(
            self._route("/auth/login"),
            json=self.CREDENTIALS
        )
        self.assertEqual(response.status_code, 200, response.text)


    def _route(self, route):
        return "http://{}:{}{}".format(
            CURRENT_CONFIG.HOSTNAME,
            CURRENT_CONFIG.PORT,
            str(route)
        )

    def test_list(self):
        """ Test that you can list """
        us = User(
            email = "test@localhost",
            password = crypt('tset')
        )
        db_sess = get_session()
        db_sess.add(us)
        db_sess.commit()

        e_a = Entry(
            userid=us.userid,
            title="test",
            completed=True,
            description="test desc"
        )
        e_b = Entry(
            userid=us.userid,
            title="test2",
            completed=False,
            description="test2 desc"
        )

        db_sess.add(e_a)
        db_sess.add(e_b)
        db_sess.commit()

        response = self.session.post(
            self._route("/auth/login"),
            json={
                'email': us.email,
                'password': us.password
            }
        )
        self.assertEqual(response.status_code, 200, response.text)

        response = self.session.get(
            self._route("/todo/entry"),
        )
        expected = [
            e_a.as_dict(),
            e_b.as_dict()
        ]
        db_sess.close()
        self.assertEqual(response.json(), expected , response.text)
        self.assertEqual(response.status_code, 200, response.text)

    def test_post(self):
        """ Test that you can list """
        response = self.session.post(
            self._route("/todo/entry"),
            json={
                'title': 'test title',
                'completed': True,
                'description': 'test description'
            }
        )
        self.assertEqual(response.status_code, 201, response.text)
        db_sess = get_session()
        entry = db_sess.query(Entry).filter(
            Entry.entryid == response.json()['entryid']
        ).one()
        db_sess.close()
        self.assertEqual(response.json(), entry.as_dict(), response.text)

    def test_get(self):
        """ Test that you can list """
        us = User(
            email = "test@localhost",
            password = "tset"
        )
        db_sess = get_session()
        db_sess.add(us)
        db_sess.commit()
        entry = Entry(
            userid=us.userid,
            title="test",
            completed=True,
            description="test desc"
        )
        db_sess.add(entry)
        db_sess.commit()
        response = self.session.post(
            self._route("/auth/login"),
            json={
                'email': us.email,
                'password': us.password
            }
        )
        self.assertEqual(response.status_code, 200, response.text)

        response = self.session.get(
            self._route("/todo/entry/{}".format(entry.entryid)
            ),
        )
        db_sess.close()
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json(), entry.as_dict(), response.text)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestEntries("test_list"))
    suite.addTest(TestEntries("test_post"))
    suite.addTest(TestEntries("test_get"))
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
