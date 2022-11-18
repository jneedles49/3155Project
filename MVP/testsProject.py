import unittest
import requests


class FlaskTest(unittest.TestCase):

    def test_index(self):
        response = requests.get("http://127.0.0.1:5000/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<h2>Use this site to maintain and organize your projects.</h2>' in response.text, True)

    def test_projects(self):
        response = requests.get("http://127.0.0.1:5000/projects")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Title' and 'Date' in response.text, True)

    def test_project(self):
        response = requests.get("http://127.0.0.1:5000/projects/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        self.assertEqual('First Project' in response.text, False)

    def test_newProject(self):
        response = requests.get("http://127.0.0.1:5000/projects/new")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<form action="new" method="post">' in response.text, True)

    def test_deleteProject(self):
        response = requests.get('http://127.0.0.1:5000/projects/delete')
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)


if __name__ == " __main__":
    unittest.main()
