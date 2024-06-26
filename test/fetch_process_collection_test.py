import sys
import os
import unittest
from unittest.mock import patch, Mock
from apicurl.user_auth import get_user_credentials
from apicurl.fetch_process_collection import get_user_collection, fetch_all_collection_pages, process_collection, split_artist_release_percentage
import pandas as pd
import matplotlib.pyplot as plt

class TestUserCollection(unittest.TestCase):
    @patch('requests.get')
    @patch('apicurl.user_auth.get_user_credentials')
    @patch.dict(os.environ, {
        'DISCOGS_USER_NAME': 'abc123',
        'DISCOGS_USER_SECRET': 'def456'
    })
    
    def setUp(self, mock_get_user_credentials, mock_get):
        # Sample music collection data for testing
        self.collection = [
            {'Artist': 'Artist A', 'album': 'Album 1', 'genre': 'Rock', 'release_year': 2000},
            {'Artist': 'Artist B', 'album': 'Album 2', 'genre': 'Jazz', 'release_year': 2005},
            {'Artist': 'Artist A', 'album': 'Album 3', 'genre': 'Rock', 'release_year': 2010},
            {'Artist': 'Artist C', 'album': 'Album 4', 'genre': 'Pop', 'release_year': 2015},
        ]
        self.dataframe = pd.DataFrame(self.collection)
        self.mock_get_user_credentials = mock_get_user_credentials
        self.mock_get = mock_get
    
    @patch.dict(os.environ, {
        'DISCOGS_USER_NAME': 'abc123',
        'DISCOGS_USER_SECRET': 'def456'
    })
    @patch('requests.get')
    @patch('apicurl.user_auth.get_user_credentials')
    def test_get_user_collection_success(self, mock_get_user_credentials, mock_get):
        # Setup mock responses
        mock_get_user_credentials.return_value = ('testuser', 'testtoken')
        mock_response = Mock()
        mock_response.json.return_value = {
            'releases': ['release1', 'release2'],
            'pagination': {'pages': 2, 'urls': {'next': 'next_url'}}
        }
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Call the function
        result = get_user_collection()

        # Verify results
        self.assertEqual(result, (['release1', 'release2'], 'next_url'))
        mock_get.assert_called_once()

    @patch.dict(os.environ, {
        'DISCOGS_USER_NAME': 'abc123'
    }, clear=True)
    def test_get_user_credentials_missing_token(self):
        with self.assertRaises(EnvironmentError) as context:
            get_user_credentials('DISCOGS')
        self.assertIn("Environment variable DISCOGS_USER_TOKEN is not set.", str(context.exception))

    @patch.dict(os.environ, {
        'DISCOGS_USER_SECRET': 'def456'
    }, clear=True)
    def test_get_user_credentials_missing_name(self):
        with self.assertRaises(EnvironmentError) as context:
            get_user_credentials('DISCOGS')
        self.assertIn("Environment variable DISCOGS_USER_NAME is not set.", str(context.exception))

    @patch('apicurl.fetch_process_collection.get_user_collection')
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

    @patch('apicurl.fetch_process_collection.split_artist_release_percentage')
    def test_split_artist_release_percentage(self, mock_split):
        # Mock setup
        artist_release_percentage = pd.DataFrame({
            'Artist': ['Artist A', 'Artist B', 'Artist C'],
            'Percentage': [50.0,25.0,25.0]
        })
        mock_split.return_value = artist_release_percentage

        # Call the function
        result = split_artist_release_percentage(self.collection, top_number=3)

        # Assertions
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('Artist', result.columns)
        self.assertIn('Percentage', result.columns)
        pd.testing.assert_frame_equal(result, artist_release_percentage)

        # Edge case: Empty dataframe
        empty_df = pd.DataFrame(columns=['Artist', 'releases'])
        result = split_artist_release_percentage(empty_df, 0)
        self.assertIsNone(result)

    """ @patch('apicurl.fetch_process_collection.visualize_artist_release_percentage')
    def test_visualize_artist_release_percentage(self, mock_visualize):
        # Mock setup
        mock_visualize.return_value = plt.Figure()

        # Call the function
        result = visualize_artist_release_percentage(self.dataframe)

        # Assertions
        self.assertIsInstance(result, plt.Figure)
        mock_visualize.assert_called_once_with(self.dataframe)

        # Edge case: Check with additional columns
        extended_df = self.dataframe.copy()
        extended_df['extra'] = [5, 5, 5, 5]
        result = visualize_artist_release_percentage(extended_df)
        self.assertIsInstance(result, plt.Figure)
        mock_visualize.assert_called_with(extended_df)

    @patch('apicurl.fetch_process_collection.update_data_model_and_storage')
    def test_update_data_model_and_storage(self, mock_update):
        # Mock setup
        mock_update.return_value = True

        # Call the function
        result = update_data_model_and_storage(self.dataframe)

        # Assertions
        self.assertTrue(result)
        mock_update.assert_called_once_with(self.dataframe)

        # Edge case: Handling a larger dataframe
        large_df = pd.concat([self.dataframe] * 1000, ignore_index=True)
        result = update_data_model_and_storage(large_df)
        self.assertTrue(result)
        mock_update.assert_called_with(large_df)

    @patch('apicurl.fetch_process_collection.enhance_ui_with_artist_release_percentage_visualization')
    def test_enhance_ui_with_artist_release_percentage_visualization(self, mock_enhance_ui):
        # Mock setup
        mock_enhance_ui.return_value = True
        visualization = plt.Figure()

        # Call the function
        result = enhance_ui_with_artist_release_percentage_visualization(visualization)

        # Assertions
        self.assertTrue(result)
        mock_enhance_ui.assert_called_once_with(visualization)

        # Edge case: Invalid visualization object
        with self.assertRaises(TypeError):
            enhance_ui_with_artist_release_percentage_visualization("Not a Figure")
        mock_enhance_ui.assert_not_called()

    @patch('apicurl.fetch_process_collection.optimize_performance_for_data_processing_and_visualization')
    def test_optimize_performance_for_data_processing_and_visualization(self, mock_optimize):
        # Mock setup
        mock_optimize.return_value = True

        # Call the function
        result = optimize_performance_for_data_processing_and_visualization(self.dataframe)

        # Assertions
        self.assertTrue(result)
        mock_optimize.assert_called_once_with(self.dataframe)

        # Edge case: Performance with missing data
        incomplete_df = self.dataframe.copy()
        incomplete_df.at[2, 'releases'] = None
        result = optimize_performance_for_data_processing_and_visualization(incomplete_df)
        self.assertTrue(result)
        mock_optimize.assert_called_with(incomplete_df) """

if __name__ == '__main__':
    unittest.main()
