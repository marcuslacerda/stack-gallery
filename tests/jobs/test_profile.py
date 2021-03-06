from tests import mock_util, config_resource_path
from config import Config
from people import Profile
import unittest
import os

class ProfileTestCase(unittest.TestCase):

    def setUp(self):
        """Setup API settings for tests."""
        config = Config(config_resource_path, False)
        self.profile = Profile(config)
        # self.profile.save(doc=build_marcus_doc(), refresh='wait_for')
        id = 'kdkdkdkdkd-2012'
        self.mock_project = build_marcus_doc()
        mock_util.post(
            config.get('PROFILE_ELASTICSEARCH_HOST'),
            'people',
            'profile',
            self.mock_project['login'],
            self.mock_project
        )

    def tearDown(self):
        """Destroy settings created for tests."""
        doc = build_marcus_doc()
        self.profile.delete(doc['login'])

    def test_has_people_load(self):
        data = self.profile.find_all()
        # list_people = data['hits']['hits']
        count_people = data['hits']['hits']
        self.assertGreaterEqual(count_people, 1)


def build_marcus_doc():
    doc = {
        "login": "mlacerda",
        "name": "MARCUS VINICIUS DE OLIVEIRA LACERDA",
        "area": {
          "code": 20,
          "name": "BU South"
        },
        "company": {
          "code": 1,
          "name": "CIT Software S.A."
        },
        "cityBase": {
          "acronym": "BH",
          "code": 6,
          "name": "Belo Horizonte"
        },
        "project": {
          "code": 9347,
          "name": "Coca Cola"
        },
        "role": {
          "code": 96,
          "name": "Developer"
        }
    }

    return doc
