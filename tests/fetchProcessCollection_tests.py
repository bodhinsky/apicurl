import unittest
from unittest.mock import patch, Mock
from apiCurl import get_user_collection, fetch_all_collection_pages, process_collection

class TestUserCollection(unittest.TestCase):
    @patch('apiCurl.requests.get')
    @patch('apiCurl.getUserCredentials')
    def test_get_user_collection_success(self, mock_getUserCredentials, mock_get):
        # Setup mock responses
        mock_getUserCredentials.return_value = ('testuser', 'testtoken')
        mock_response = Mock()
        mock_response.json.return_value = {
            'releases': ['release1', 'release2'],
            'pagination': {'pages': 2, 'urls': {'next': 'next_url'}}
        }
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Call the function
        result = get_user_collection(1)

        # Verify results
        self.assertEqual(result, (['release1', 'release2'], 'next_url'))
        mock_get.assert_called_once()

    @patch('apiCurl.requests.get')
    @patch('apiCurl.getUserCredentials')
    def test_get_user_collection_failure(self, mock_getUserCredentials, mock_get):
        mock_getUserCredentials.return_value = ('testuser', 'testtoken')
        mock_get.side_effect = Exception('Error fetching collection')

        # Call the function
        result = get_user_collection(1)

        # Verify results
        self.assertEqual(result, ([], False))

    @patch('apiCurl.get_user_collection')
    def test_fetch_all_collection_pages(self, mock_get_user_collection):
        # Setup mock responses
        mock_get_user_collection.side_effect = [
            (['release1'], 'next_url'),
            (['release2'], False)
        ]

        # Call the function
        result = fetch_all_collection_pages()

        # Verify results
        self.assertEqual(result, ['release1', 'release2'])
        self.assertEqual(mock_get_user_collection.call_count, 2)

    def test_process_collection_empty(self):
        # Test processing an empty collection
        result = process_collection([])
        self.assertIsNone(result)

    def test_process_collection_valid(self):
        # Test processing a valid collection
        collection = [{
            'basic_information': {
                'title': 'Album1',
                'artists': [{'name': 'Artist1'}],
                'year': 2020,
                'genres': ['Rock'],
                'styles': ['Alternative']
            }
        }]
        expected_result = [{
            'Title': 'Album1',
            'Artist': 'Artist1',
            'Year': 2020,
            'Genre': 'Rock',
            'Style': 'Alternative'
        }]
        result = process_collection(collection)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
