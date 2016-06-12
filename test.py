import os
import application
import unittest
import tempfile
class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        application.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        with application.app.app_context():
            flaskr.init_db()
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])
if __name__ == '__main__':
    unittest.main()
