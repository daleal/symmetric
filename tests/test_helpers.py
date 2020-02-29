"""
A module to test the helpers of symmetric.
"""

import os
import unittest

import symmetric.errors
import symmetric.helpers
import symmetric.constants


class PathParserTestCase(unittest.TestCase):
    """Tests the path parser helper method."""
    def setUp(self):
        self.correct_paths = [
            "/",
            "/symmetric",
            "/hi/hello",
            "/hello-world/basic_syntax",
            "/_element/BIGelement"
        ]
        self.incorrect_paths = [
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

    def test_correct_paths(self):
        """Tests that correct paths don't raise errors."""
        for iii in range(len(self.correct_paths)):
            with self.subTest(run=iii):
                symmetric.helpers.parse_url(self.correct_paths[iii])

    def test_incorrect_paths(self):
        """Tests that incorrect paths raise a IncorrectURLFormatError error."""
        for iii in range(len(self.incorrect_paths)):
            with self.subTest(run=iii):
                with self.assertRaises(
                        symmetric.errors.IncorrectURLFormatError):
                    symmetric.helpers.parse_url(self.incorrect_paths[iii])


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
            body={},
            auth_token=False,
            client_token_name=symmetric.constants.API_CLIENT_TOKEN_NAME,
            server_token_name=symmetric.constants.API_SERVER_TOKEN_NAME
        )

    def test_correct_token(self):
        """Tests that an error isn't raised when the correct token is given."""
        symmetric.helpers.authenticate(
            body={
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
                body={
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
                body={},
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
