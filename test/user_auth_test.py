import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import requests
import unittest
from unittest.mock import patch, mock_open
from apicurl.user_auth import get_user_credentials, get_user_auth_token

class TestUserAuth(unittest.TestCase):
    @patch.dict(os.environ, {
        'SPOTIFY_USER_NAME': 'abc123',
        'SPOTIFY_USER_SECRET': 'def456'
    })
    def test_get_user_credentials_success(self):
        # Test successful retrieval of credentials
        client_id, client_secret = get_user_credentials('Spotify')
        self.assertEqual(client_id, 'abc123')
        self.assertEqual(client_secret, 'def456')

    def test_get_user_credentials_failure(self):
        # Test failure when service is not in JSON file
        with self.assertRaises(EnvironmentError):
            get_user_credentials('Spotify')

    @patch('apicurl.user_auth.get_user_credentials')
    @patch('apicurl.user_auth.requests.post')
    def test_get_user_auth_token_success(self, mock_post, mock_get_user_credentials):
        # Setup mock responses
        mock_get_user_credentials.return_value = ('abc123', 'def456')
        mock_response = unittest.mock.Mock()
        mock_response.raise_for_status = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "token123"}
        mock_post.return_value = mock_response

        # Call the function
        result = get_user_auth_token()

        # Verify results
        self.assertEqual(result, {"access_token": "token123"})
        mock_post.assert_called_once()

    @patch('requests.post')
    @patch('apicurl.user_auth.get_user_credentials')
    def test_get_user_auth_token_failure(self, mock_get_user_credentials, mock_post):
        # Setup mock to raise an HTTP error
        mock_get_user_credentials.return_value = ('abc123', 'def456')
        mock_post.side_effect = requests.exceptions.HTTPError("HTTP error occurred")

        # Call the function and check for no return value
        result = get_user_auth_token()
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
