import importlib
import unittest

from app import resolve_app_prefix


class DeploymentConfigTest(unittest.TestCase):
    def test_resolve_app_prefix_defaults_to_prediction_system(self):
        self.assertEqual(resolve_app_prefix("/prediction_system"), "/prediction_system")

    def test_resolve_app_prefix_defaults_to_root_when_not_provided(self):
        self.assertEqual(resolve_app_prefix(), "")

    def test_resolve_app_prefix_supports_root_hosting(self):
        self.assertEqual(resolve_app_prefix(""), "")
        self.assertEqual(resolve_app_prefix("/"), "")

    def test_prefixed_routes_redirect_without_double_prefix(self):
        app_module = importlib.import_module("app")
        client = app_module.application.test_client()
        response = client.get("/prediction_system/production-plan", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/prediction_system/")


if __name__ == "__main__":
    unittest.main()
