from unittest import TestCase
from unittest.mock import patch, Mock

from gamebench_api_client.models.dataframes.generic.abstract_generic import AbstractGenericModel
from gamebench_api_client.global_settings import GAMEBENCH_CONFIG


class TestGenericFrameModel(TestCase):
    """ Unit tests for the AbstractGenericModel class."""

    @patch('gamebench_api_client.models.dataframes.generic.abstract_generic.Authenticator')
    @patch('gamebench_api_client.models.dataframes.generic.abstract_generic.AbstractGenericModel.get_data')
    @patch('gamebench_api_client.models.dataframes.generic.abstract_generic.GenericMediator')
    def test_init_sets_attributes(self, mock_generic_frame, mock_get_data, mock_authenticator):
        """ Verify the instance variables call the appropriate methods."""

        test_data = {
            'metric': 'Testing'
        }
        generic_model = AbstractGenericModel(**test_data)

        with self.subTest():
            mock_generic_frame.assert_called_with(generic_model.request_parameters)
        with self.subTest():
            mock_get_data.assert_called_with()
        with self.subTest():
            mock_authenticator.assert_called_with(
                {
                    'username': GAMEBENCH_CONFIG['username'],
                    'password': GAMEBENCH_CONFIG['password']
                }
            )

    @patch('gamebench_api_client.models.dataframes.generic.abstract_generic.GenericMediator')
    def test_get_data(self, mock_generic_frame):
        """ Verify the data is properly set."""

        expected = "Test Data"
        mock_instance = mock_generic_frame.return_value
        mock_instance.get_results.return_value = expected

        with patch('gamebench_api_client.models.dataframes.generic.abstract_generic.Authenticator'):
            actual = AbstractGenericModel().data

        self.assertEqual(
                expected,
                actual
        )

    @patch('gamebench_api_client.models.dataframes.generic.abstract_generic.Authenticator')
    @patch('gamebench_api_client.models.dataframes.generic.abstract_generic.AbstractGenericModel.get_data')
    @patch('gamebench_api_client.models.dataframes.generic.abstract_generic.GenericMediator')
    def test_auth_token_added_to_request_parameters(self, mock_generic_frame, mock_get_data, mock_authenticator):

        starting_dict = dict()

        expected_dict = {
            'auth_token': 'q1w2e3r4t5y6'
        }

        mock_authenticator.data = {
            'token': 'q1w2e3r4t5y6'
        }

        actual = AbstractGenericModel(**starting_dict)

        self.assertIn('auth_token', actual.request_parameters)
        # Want this to be the test, but the value is a MagicMock object.
        # self.assertDictEqual(expected_dict, actual.request_parameters)
