"""
A module to test the helpers of symmetric.
"""

import os
import unittest

import symmetric.errors
import symmetric.helpers
import symmetric.constants


class ModuleNameGetterTestCase(unittest.TestCase):
    """Tests the get_module_name helper method."""
    def setUp(self):
        class SymmetricTest:
            def __init__(self, endpoints):
                self.endpoints = endpoints

        class FunctionTest:
            def __init__(self):
                self.function = lambda x: x + 1

        self.empty_object = SymmetricTest([])
        self.object = SymmetricTest([FunctionTest()])

        self.module_names = [
            {"name": "test_module", "expected": "test_module"},
            {"name": "test.module", "expected": "test"},
            {"name": "test.module.string", "expected": "test"}
        ]

    def test_empty_object_module_getter(self):
        """
        Tests that the method fails to find an endpoint and returns 'symmetric'
        """
        self.assertEqual(
            symmetric.helpers.get_module_name(self.empty_object),
            "symmetric"
        )

    def test_object_module_getter(self):
        """Tests that the method gets the expected root module name."""
        for iii in range(len(self.module_names)):
            with self.subTest(run=iii):
                func = self.object.endpoints[0].function
                func.__module__ = self.module_names[iii]["name"]
                self.assertEqual(
                    symmetric.helpers.get_module_name(self.object),
                    self.module_names[iii]["expected"]
                )


class TypeGetterTestCase(unittest.TestCase):
    """Tests the type_to_string helper method."""
    def setUp(self):
        self.types = [
            {"type": str, "expected": "string"},
            {"type": float, "expected": "number"},
            {"type": int, "expected": "integer"},
            {"type": bool, "expected": "boolean"},
            {"type": type(None), "expected": "null"},
            {"type": list, "expected": "array"},
            {"type": dict, "expected": "object"},
            {"type": tuple, "expected": "object"},
            {"type": range, "expected": "object"},
            {"type": hash, "expected": "object"},
            {"type": set, "expected": "object"},
            {"type": frozenset, "expected": "object"},
            {"type": bytes, "expected": "object"},
            {"type": bytearray, "expected": "object"},
            {"type": memoryview, "expected": "object"}
        ]

    def test_type_getter(self):
        """Tests that the method transforms types correctly."""
        for iii in range(len(self.types)):
            with self.subTest(run=iii):
                self.assertEqual(
                    symmetric.helpers.type_to_string(self.types[iii]["type"]),
                    self.types[iii]["expected"]
                )


class HumanizerTestCase(unittest.TestCase):
    """Tests the humanize helper method."""
    def setUp(self):
        self.easy_pre_humanized = [
            "app",
            "APP",
            "App",
            "aPp",
            "apP",
            "APp",
            "ApP",
            "aPP"
        ]
        self.easy_humanized = "App"
        self.standard_pre_humanized = [
            "cool_app_name",
            "cool-app-name",
            "cool app name",
            "COOL_APP_NAME",
            "COOL-APP-NAME",
            "COOL APP NAME"
        ]
        self.standard_humanized = "Cool App Name"

    def test_easy_humanization(self):
        """Tests that the method humanizes easy cases."""
        for iii in range(len(self.easy_pre_humanized)):
            with self.subTest(run=iii):
                self.assertEqual(
                    symmetric.helpers.humanize(self.easy_pre_humanized[iii]),
                    self.easy_humanized
                )

    def test_incorrect_routes(self):
        """Tests that the method humanizes standard cases."""
        for iii in range(len(self.standard_pre_humanized)):
            with self.subTest(run=iii):
                self.assertEqual(
                    symmetric.helpers.humanize(
                        self.standard_pre_humanized[iii]
                    ),
                    self.standard_humanized
                )


class RouteParserTestCase(unittest.TestCase):
    """Tests the route parser helper method."""
    def setUp(self):
        self.correct_routes = [
            "/",
            "/symmetric",
            "/hi/hello",
            "/hello-world/basic_syntax",
            "/_element/BIGelement"
        ]
        self.incorrect_routes = [
            "/hi//hello",
            "element",
            "/another-element/",
            "/bad-_composition",
            "/-worse",
            "/element__two",
            "/element2",
            "/oof-number-one-",
            "/oof_number_two_"
        ]

    def test_correct_routes(self):
        """Tests that correct routes don't raise errors."""
        for iii in range(len(self.correct_routes)):
            with self.subTest(run=iii):
                symmetric.helpers.parse_route(self.correct_routes[iii])

    def test_incorrect_routes(self):
        """
        Tests that incorrect routes raise a IncorrectRouteFormatError error.
        """
        for iii in range(len(self.incorrect_routes)):
            with self.subTest(run=iii):
                with self.assertRaises(
                        symmetric.errors.IncorrectRouteFormatError):
                    symmetric.helpers.parse_route(self.incorrect_routes[iii])


class AuthenticationTestCase(unittest.TestCase):
    """Tests the authentication helper method."""
    def setUp(self):
        self.client_token_name = symmetric.constants.API_CLIENT_TOKEN_NAME
        self.server_token_name = symmetric.constants.API_SERVER_TOKEN_NAME
        self.token = "test_token"
        self.incorrect_token = "im_not_a_correct_token"
        os.environ[self.server_token_name] = self.token

    def test_no_token_required(self):
        """Tests that an error isn't raised when there is no token required."""
        symmetric.helpers.authenticate(
            headers={},
            auth_token=False,
            client_token_name=symmetric.constants.API_CLIENT_TOKEN_NAME,
            server_token_name=symmetric.constants.API_SERVER_TOKEN_NAME
        )

    def test_correct_token(self):
        """Tests that an error isn't raised when the correct token is given."""
        symmetric.helpers.authenticate(
            headers={
                self.client_token_name: self.token
            },
            auth_token=True,
            client_token_name=symmetric.constants.API_CLIENT_TOKEN_NAME,
            server_token_name=symmetric.constants.API_SERVER_TOKEN_NAME
        )

    def test_no_token_given(self):
        """Tests that an error is raised when the token is not given."""
        with self.assertRaises(symmetric.errors.AuthenticationRequiredError):
            symmetric.helpers.authenticate(
                headers={
                    self.client_token_name: self.incorrect_token
                },
                auth_token=True,
                client_token_name=symmetric.constants.API_CLIENT_TOKEN_NAME,
                server_token_name=symmetric.constants.API_SERVER_TOKEN_NAME
            )

    def test_incorrect_token(self):
        """Tests that an error is raised when an incorrect token is given."""
        with self.assertRaises(symmetric.errors.AuthenticationRequiredError):
            symmetric.helpers.authenticate(
                headers={},
                auth_token=True,
                client_token_name=symmetric.constants.API_CLIENT_TOKEN_NAME,
                server_token_name=symmetric.constants.API_SERVER_TOKEN_NAME
            )

    def tearDown(self):
        del os.environ[self.server_token_name]


class FunctionParametersFilterTestCase(unittest.TestCase):
    """Tests the function parameters filter helper method."""
    def setUp(self):
        self.function = lambda x, y, z: x + y + z
        self.kwarg_function = lambda x, y, z, **kwargs: x + y + z
        self.no_params_function = lambda: None
        self.token_key = symmetric.constants.API_CLIENT_TOKEN_NAME

        # Before filtering
        self.data_extra = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "x": 5,
            "y": 6,
            "z": 7
        }
        self.data_exactly = {
            "x": 1,
            "y": 2,
            "z": 3
        }
        self.data_little = {
            "x": 1,
            "y": 2
        }

    def test_data_extra_filter(self):
        """
        Tests that, without removing auth token, the params shrunk to
        just the ones of the function.
        """
        params = symmetric.helpers.filter_params(
            function=self.function,
            data=self.data_extra,
            has_token=False,
            token_key="irrelevant"
        )
        self.assertEqual(params, {
            "x": 5,
            "y": 6,
            "z": 7
        })

    def test_data_exactly_filter(self):
        """
        Tests that, without removing auth token, the params stayed
        just the ones of the function.
        """
        params = symmetric.helpers.filter_params(
            function=self.function,
            data=self.data_exactly,
            has_token=False,
            token_key="irrelevant"
        )
        self.assertEqual(params, {
            "x": 1,
            "y": 2,
            "z": 3
        })

    def test_data_little_filter(self):
        """
        Tests that, without removing auth token, the params stayed
        less than the ones of the function.
        """
        params = symmetric.helpers.filter_params(
            function=self.function,
            data=self.data_little,
            has_token=False,
            token_key="irrelevant"
        )
        self.assertEqual(params, {
            "x": 1,
            "y": 2
        })

    def test_data_extra_kwarg_filter(self):
        """
        Tests that, without removing auth token, the params did not shrunk to
        just the ones of the kwarg function.
        """
        params = symmetric.helpers.filter_params(
            function=self.kwarg_function,
            data=self.data_extra,
            has_token=False,
            token_key="irrelevant"
        )
        self.assertEqual(params, {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "x": 5,
            "y": 6,
            "z": 7
        })

    def test_data_exactly_kwarg_filter(self):
        """
        Tests that, without removing auth token, the params stayed
        just the ones of the kwarg function.
        """
        params = symmetric.helpers.filter_params(
            function=self.kwarg_function,
            data=self.data_exactly,
            has_token=False,
            token_key="irrelevant"
        )
        self.assertEqual(params, {
            "x": 1,
            "y": 2,
            "z": 3
        })

    def test_data_little_kwarg_filter(self):
        """
        Tests that, without removing auth token, the params stayed
        less than the ones of the kwarg function.
        """
        params = symmetric.helpers.filter_params(
            function=self.kwarg_function,
            data=self.data_little,
            has_token=False,
            token_key="irrelevant"
        )
        self.assertEqual(params, {
            "x": 1,
            "y": 2
        })

    def test_no_args_function(self):
        """Tests that a function with no args returns an empty dictionary."""
        params = symmetric.helpers.filter_params(
            function=self.no_params_function,
            data=self.data_extra,
            has_token=False,
            token_key="irrelevant"
        )
        self.assertEqual(params, {})

    def test_no_auth_data(self):
        """
        Tests that trying to remove the auth token when it does not exist
        does not make the function fail.
        """
        params = symmetric.helpers.filter_params(
            function=self.no_params_function,
            data={},
            has_token=True,
            token_key="does_not_exist"
        )
        self.assertNotIn("does_not_exist", params)

    def test_authed_data(self):
        """
        Tests that, when given a kwarg function, the auth token is removed.
        """
        params = symmetric.helpers.filter_params(
            function=self.kwarg_function,
            data=self.data_extra,
            has_token=True,
            token_key="a"
        )
        self.assertNotIn("a", params)
