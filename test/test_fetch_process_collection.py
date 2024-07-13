import os
from unittest.mock import patch, Mock
import pytest
from apicurl.user_auth import get_user_credentials
from apicurl.fetch_process_collection import get_user_collection, fetch_all_collection_pages, process_collection
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from io import BytesIO,StringIO

@pytest.fixture
def sample_collection():
    return [
        {'Artist': 'Artist A', 'album': 'Album 1', 'genre': 'Rock', 'release_year': 2000},
        {'Artist': 'Artist B', 'album': 'Album 2', 'genre': 'Jazz', 'release_year': 2005},
        {'Artist': 'Artist A', 'album': 'Album 3', 'genre': 'Rock', 'release_year': 2010},
        {'Artist': 'Artist C', 'album': 'Album 4', 'genre': 'Pop', 'release_year': 2015},
    ]

@patch('requests.get')
@patch('apicurl.user_auth.get_user_credentials')
@patch.dict(os.environ, {
    'DISCOGS_USER_NAME': 'abc123',
    'DISCOGS_USER_SECRET': 'def456'
})
def test_get_user_collection_success(mock_get_user_credentials, mock_get):
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
    assert result == (['release1', 'release2'], 'next_url')
    mock_get.assert_called_once()

@patch.dict(os.environ, {
    'DISCOGS_USER_NAME': 'abc123'
}, clear=True)
def test_get_user_credentials_missing_token():
    with pytest.raises(EnvironmentError) as context:
        get_user_credentials('DISCOGS')
    assert "Environment variable DISCOGS_USER_TOKEN is not set." in str(context.value)

@patch.dict(os.environ, {
    'DISCOGS_USER_SECRET': 'def456'
}, clear=True)
def test_get_user_credentials_missing_name():
    with pytest.raises(EnvironmentError) as context:
        get_user_credentials('DISCOGS')
    assert "Environment variable DISCOGS_USER_NAME is not set." in str(context.value)

@patch('apicurl.fetch_process_collection.get_user_collection')
def test_fetch_all_collection_pages(mock_get_user_collection):
    # Setup mock responses
    mock_get_user_collection.side_effect = [
        (['release1'], 'next_url'),
        (['release2'], False)
    ]

    # Call the function
    result = fetch_all_collection_pages()

    # Verify results
    assert result == ['release1', 'release2']
    assert mock_get_user_collection.call_count == 2

def test_process_collection_empty():
    # Test processing an empty collection
    result = process_collection([])
    assert result is None

def test_process_collection_valid():
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
    assert result == expected_result

def test_save_collection_to_json():
    # Test case 1: Save a dictionary
    collection = {"key1": "value1", "key2": "value2"}
    filepath = "test_dict.json"
    
    save_collection_to_json(collection, filepath)
    
    assert os.path.exists(filepath)
    with open(filepath, 'r') as f:
        loaded_data = json.load(f)
    assert loaded_data == collection
    
    os.remove(filepath)

    # Test case 2: Save a list
    collection = [1, 2, 3, 4, 5]
    filepath = "data/test_list.json"
    
    save_collection_to_json(collection, filepath)
    
    assert os.path.exists(filepath)
    with open(filepath, 'r') as f:
        loaded_data = json.load(f)
    assert loaded_data == collection
    
    os.remove(filepath)

def test_save_collection_to_json_nested():
    # Test case 3: Save a nested structure
    collection = {
        "name": "John Doe",
        "age": 30,
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "zipcode": "12345"
        },
        "hobbies": ["reading", "cycling", "photography"]
    }
    filepath = "data/test_nested.json"
    
    save_collection_to_json(collection, filepath)
    
    assert os.path.exists(filepath)
    with open(filepath, 'r') as f:
        loaded_data = json.load(f)
    assert loaded_data == collection
    
    os.remove(filepath)

def test_save_collection_to_json_empty():
    # Test case 4: Save an empty collection
    collection = {}
    filepath = "data/test_empty.json"
    
    save_collection_to_json(collection, filepath)
    
    assert os.path.exists(filepath)
    with open(filepath, 'r') as f:
        loaded_data = json.load(f)
    assert loaded_data == collection
    
    os.remove(filepath)

def test_save_collection_to_json_file_error():
    # Test case 5: Test file write permission error
    collection = {"key": "value"}
    filepath = "/var/test.json"  # Assuming no write permission in /root
    
    with pytest.raises(PermissionError):
        save_collection_to_json(collection, filepath)

def test_save_collection_to_json_invalid_json():
    # Test case 6: Test with non-JSON serializable data
    collection = {"key": set([1, 2, 3])}  # set is not JSON serializable
    filepath = "data/test_invalid.json"
    
    with pytest.raises(TypeError):
        save_collection_to_json(collection, filepath)

if __name__ == '__main__':
    pytest.main()
