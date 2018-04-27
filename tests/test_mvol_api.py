import unittest
import json
from os import environ

# Defer any configuration to the tests setUp()
environ['MVOL_API_DEFER_CONFIG'] = "True"

import mvol_api


class Tests(unittest.TestCase):
    def setUp(self):
        # Perform any setup that should occur
        # before every test
        self.app = mvol_api.app.test_client()

    def tearDown(self):
        # Perform any tear down that should
        # occur after every test
        pass

    def testPass(self):
        self.assertEqual(True, True)

    def testVersionAvailable(self):
        x = getattr(mvol_api, "__version__", None)
        self.assertTrue(x is not None)

    def testVersion(self):
        version_response = self.app.get("/version")
        self.assertEqual(version_response.status_code, 200)
        version_json = json.loads(version_response.data.decode())
        api_reported_version = version_json['version']
        self.assertEqual(
            mvol_api.blueprint.__version__,
            api_reported_version
        )


if __name__ == "__main__":
    unittest.main()
