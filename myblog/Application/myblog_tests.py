import os
import myblog
import unittest
import tempfile

class MyblogTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, myblog.app.config['DATABASE'] = tempfile.mkstemp()
        myblog.app.config['TESTING'] = True
        self.app = myblog.app.test_client()
        myblog.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(myblog.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/entries')
        #print rv
        #print rv.data
        assert 'No entries here so far' in rv.data

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data

if __name__ == '__main__':
    unittest.main()