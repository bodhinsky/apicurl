import unittest
from unittest.mock import patch, mock_open
from apiCurl.userAuth import getUserCredentials, get_user_auth_token

class TestUserAuth(unittest.TestCase):
    @patch('apiCurl.userAuth.open', new_callable=mock_open, read_data='{"Spotify": {"client_id": "abc123", "client_secret": "def456"}}')
    def test_getUserCredentials_success(self, mock_file):
        # Test successful retrieval of credentials
        client_id, client_secret = getUserCredentials('Spotify')
        self.assertEqual(client_id, 'abc123')
        self.assertEqual(client_secret, 'def456')

    @patch('apiCurl.userAuth.open', new_callable=mock_open, read_data='{}')
    def test_getUserCredentials_failure(self, mock_file):
        # Test failure when service is not in JSON file
        with self.assertRaises(ValueError):
            getUserCredentials('Spotify')

    @patch('apiCurl.userAuth.getUserCredentials')
    @patch('apiCurl.userAuth.requests.post')
    def test_get_user_auth_token_success(self, mock_post, mock_getUserCredentials):
        # Setup mock responses
        mock_getUserCredentials.return_value = ('abc123', 'def456')
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

    @patch('apiCurl.userAuth.requests.post')
    @patch('apiCurl.userAuth.getUserCredentials')
    def test_get_user_auth_token_failure(self, mock_getUserCredentials, mock_post):
        # Setup mock to raise an HTTP error
        mock_getUserCredentials.return_value = ('abc123', 'def456')
        mock_post.side_effect = requests.exceptions.HTTPError("HTTP error occurred")

        # Call the function and check for no return value
        result = get_user_auth_token()
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
