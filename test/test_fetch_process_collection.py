import os
from unittest.mock import patch, Mock, MagicMock
import pytest
from apicurl.user_auth import get_user_credentials
from apicurl.fetch_process_collection import get_user_collection, fetch_all_collection_pages, process_collection, save_collection_to_json, split_artist_release_percentage, visualize_artist_release_percentage, list_artist_releases
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from io import BytesIO,StringIO
from datetime import datetime, timedelta
from freezegun import freeze_time

@pytest.fixture
def sample_collection():
    return [
        {'Artist': 'Artist A', 'Album': 'Album 1', 'Genre': 'Rock', 'Release Year': 2000},
        {'Artist': 'Artist B', 'Album': 'Album 2', 'Genre': 'Jazz', 'Release Year': 2005},
        {'Artist': 'Artist A', 'Album': 'Album 3', 'Genre': 'Rock', 'Release Year': 2010},
        {'Artist': 'Artist C', 'Album': 'Album 4', 'Genre': 'Pop', 'Release Year': 2015},
    ]

@patch('requests.get')
@patch('apicurl.user_auth.get_user_credentials')
@patch.dict(os.environ, {
    'DISCOGS_USER_NAME': 'abc123',
    'DISCOGS_USER_TOKEN': 'def456'
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
    'DISCOGS_USER_TOKEN': 'def456'
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

def test_save_collection_to_json_invalid_json():
    # Test case 6: Test with non-JSON serializable data
    collection = {"key": set([1, 2, 3])}  # set is not JSON serializable
    filepath = "data/test_invalid.json"
    
    with pytest.raises(TypeError):
        save_collection_to_json(collection, filepath)

def test_save_collection_new_file(sample_collection, tmp_path):
    filepath = "data/new_file.json"
    
    result = save_collection_to_json(sample_collection, filepath)
    
    assert result == True
    assert os.path.exists(filepath)
    with open(filepath, 'r') as f:
        loaded_data = json.load(f)
    assert loaded_data == sample_collection

def test_save_collection_overwrite_old_file(sample_collection, tmp_path):
    filepath = "data/overwrite_old.json"
    
    # Create an initial file
    with open(filepath, 'w') as f:
        json.dump({"old": "data"}, f)
    
    # Set file modification time to 25 hours ago
    old_time = datetime.now() - timedelta(hours=25)
    os.utime(filepath, (old_time.timestamp(), old_time.timestamp()))
    
    result = save_collection_to_json(sample_collection, filepath)
    
    assert result == True
    with open(filepath, 'r') as f:
        loaded_data = json.load(f)
    assert loaded_data == sample_collection

    os.remove(filepath)

def test_save_collection_do_not_overwrite_recent_file(sample_collection, tmp_path):
    filepath = "data/not_overwrite_recent.json"
    
    # Create an initial file
    initial_data = {"old": "data"}
    with open(filepath, 'w') as f:
        json.dump(initial_data, f)
    
    # Set file modification time to 23 hours ago
    old_time = datetime.now() - timedelta(hours=23)
    os.utime(filepath, (old_time.timestamp(), old_time.timestamp()))
    
    result = save_collection_to_json(sample_collection, filepath)
    
    assert result == False
    with open(filepath, 'r') as f:
        loaded_data = json.load(f)
    assert loaded_data == initial_data

    os.remove(filepath)

@freeze_time("2023-01-01 12:00:00")
def test_save_collection_exact_24_hours(sample_collection, tmp_path):
    filepath = "data/exact_day.json"
    
    # Create an initial file
    initial_data = {"old": "data"}
    with open(filepath, 'w') as f:
        json.dump(initial_data, f)
    
    # Set file modification time to exactly 24 hours ago
    old_time = datetime.now() - timedelta(hours=24)
    os.utime(filepath, (old_time.timestamp(), old_time.timestamp()))
    
    result = save_collection_to_json(sample_collection, filepath)
    
    assert result == True
    with open(filepath, 'r') as f:
        loaded_data = json.load(f)
    assert loaded_data == sample_collection
    os.remove(filepath)

def test_save_collection_file_error(sample_collection, tmp_path):
    filepath = "data/nonexistent_dir/test.json"
    
    with pytest.raises(FileNotFoundError):
        save_collection_to_json(sample_collection, filepath)

def test_save_collection_invalid_json():
    collection = {"key": set([1, 2, 3])}  # set is not JSON serializable
    filepath = "data/test.json"
    
    with pytest.raises(TypeError):
        save_collection_to_json(collection, filepath)

def test_split_artist_release_percentage_normal(sample_collection):
    result = split_artist_release_percentage(sample_collection, 2)
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3  # Top 2 + Others
    assert result['Artist'].tolist() == ['Artist A', 'Artist B', 'Others']
    assert result['Percentage'].sum() == pytest.approx(100)
    assert result.loc[result['Artist'] == 'Artist A', 'Percentage'].values[0] == pytest.approx(50)
    assert result.loc[result['Artist'] == 'Artist B', 'Percentage'].values[0] == pytest.approx(25)
    assert result.loc[result['Artist'] == 'Others', 'Percentage'].values[0] == pytest.approx(25)

def test_split_artist_release_percentage_empty_list():
    result = split_artist_release_percentage([], 3)
    assert result is None

def test_split_artist_release_percentage_not_list():
    result = split_artist_release_percentage({}, 3)
    assert result is None

def test_split_artist_release_percentage_no_artist_column():
    invalid_collection = [{'album': 'Album 1', 'genre': 'Rock', 'release_year': 2000}]
    with pytest.raises(ValueError, match="The collection does not contain an 'artist' column"):
        split_artist_release_percentage(invalid_collection, 3)

def test_split_artist_release_percentage_all_unique(sample_collection):
    result = split_artist_release_percentage(sample_collection, 3)
    
    assert len(result) == 3  # All unique artists, no 'Others'
    assert 'Others' not in result['Artist'].tolist()
    assert result['Percentage'].tolist() == [50, 25, 25]

def test_split_artist_release_percentage_no_others(sample_collection):
    result = split_artist_release_percentage(sample_collection, 4)
    
    assert len(result) == 3  # All unique artists, no 'Others'
    assert 'Others' not in result['Artist'].tolist()
    assert result['Percentage'].sum() == pytest.approx(100)

def test_split_artist_release_percentage_large_top_number(sample_collection):
    result = split_artist_release_percentage(sample_collection, 10)
    
    assert len(result) == 3  # All unique artists, no 'Others'
    assert 'Others' not in result['Artist'].tolist()
    assert result['Percentage'].sum() == pytest.approx(100)

@pytest.mark.parametrize("top_number", [1, 2, 3])
def test_split_artist_release_percentage_different_top_numbers(sample_collection, top_number):
    result = split_artist_release_percentage(sample_collection, top_number)
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) <= top_number + 1  # Top N + possibly Others
    assert result['Percentage'].sum() == pytest.approx(100)

def test_split_artist_release_percentage_single_artist():
    single_artist_collection = [
        {'Artist': 'Artist A', 'album': 'Album 1', 'genre': 'Rock', 'release_year': 2000},
        {'Artist': 'Artist A', 'album': 'Album 2', 'genre': 'Rock', 'release_year': 2005},
    ]
    result = split_artist_release_percentage(single_artist_collection, 3)
    
    assert len(result) == 1
    assert result['Artist'].tolist() == ['Artist A']
    assert result['Percentage'].values[0] == pytest.approx(100)

@pytest.fixture
def sample_percentage_dataframe():
    return pd.DataFrame({
        'Artist': ['Artist A', 'Artist B', 'Others'],
        'Percentage': [50, 30, 20]
    })

def test_visualize_artist_release_percentage_normal(sample_percentage_dataframe):
    with patch('matplotlib.pyplot.figure') as mock_figure, \
         patch('matplotlib.pyplot.pie') as mock_pie, \
         patch('matplotlib.pyplot.title') as mock_title, \
         patch('matplotlib.pyplot.show') as mock_show:
        
        mock_fig = MagicMock()
        mock_ax = MagicMock()

        mock_subplots.return_value = (mock_fig, mock_ax)

        visualize_artist_release_percentage(sample_percentage_dataframe)
        
        mock_subplots.assert_called_once_with(figsize=(8, 8))
        mock_show.assert_called_once()

def test_visualize_artist_release_percentage_empty_dataframe():
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError, match="The dataframe is empty"):
        visualize_artist_release_percentage(empty_df)

def test_visualize_artist_release_percentage_missing_columns():
    invalid_df = pd.DataFrame({'Artist': ['A', 'B'], 'InvalidColumn': [1, 2]})
    with pytest.raises(ValueError, match=r"The dataframe must contain the following columns: \{('Artist', 'Percentage'|'Percentage', 'Artist')\}"):
        visualize_artist_release_percentage(invalid_df)

@pytest.mark.parametrize("test_df", [
    pd.DataFrame({'Artist': ['A', 'B'], 'Percentage': [60, 40]}),
    pd.DataFrame({'Artist': ['A', 'B', 'C', 'D'], 'Percentage': [25, 25, 25, 25]}),
    pd.DataFrame({'Artist': ['A'], 'Percentage': [100]})
])
def test_visualize_artist_release_percentage_various_inputs(test_df):
    with patch('matplotlib.pyplot.subplots') as mock_subplots, \
         patch('matplotlib.pyplot.show') as mock_show:
        
        # Create mock objects for fig and ax
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        
        # Configure the return value of subplots to be a tuple of the mock objects
        mock_subplots.return_value = (mock_fig, mock_ax)

        visualize_artist_release_percentage(test_df)
        
        mock_subplots.assert_called_once_with(figsize=(8, 8))

        # Check if the correct data is passed to plt.pie
        args, kwargs = mock_ax.pie.call_args
        assert (args[0] == test_df['Percentage']).all()
        assert (kwargs['labels'] == test_df['Artist']).all()

def test_visualize_artist_release_percentage_plot_details(sample_percentage_dataframe):
    with patch('matplotlib.pyplot.figure') as mock_figure, \
         patch('matplotlib.pyplot.pie') as mock_pie, \
         patch('matplotlib.pyplot.title') as mock_title, \
         patch('matplotlib.pyplot.show') as mock_show:
        
        mock_fig = MagicMock()
        mock_ax =  MagicMock()

        mock_subplots.return_value = (mock_fig, mock_ax)

        visualize_artist_release_percentage(sample_percentage_dataframe)
        
        # Check figure size
        mock_subplots.assert_called_once_with(figsize=(8, 8))

        # Check pie chart details
        args, kwargs = mock_pie.call_args

        assert (args[0] == sample_percentage_dataframe['Percentage']).all()
        assert (kwargs['labels'] == sample_percentage_dataframe['Artist']).all()
        assert kwargs['autopct'] == '%1.1f%%'
        assert kwargs['startangle'] == 140

        mock_show.assert_called_once()

def test_list_artist_releases_all(sample_collection, capsys):
    result = list_artist_releases(sample_collection)
    
    captured = capsys.readouterr()
    assert "Artist A" in captured.out
    assert "Artist B" in captured.out
    assert "Artist C" in captured.out
    assert "Album 1" in captured.out
    assert "Album 2" in captured.out
    assert "Album 3" in captured.out
    assert "Album 4" in captured.out
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 4

def test_list_artist_releases_specific_artist(sample_collection, capsys):
    result = list_artist_releases(sample_collection, artist="Artist A")
    
    captured = capsys.readouterr()
    assert "Artist A" in captured.out
    assert "Album 1" in captured.out
    assert "Album 3" in captured.out
    assert "Artist B" not in captured.out
    assert "Artist C" not in captured.out
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2

def test_list_artist_releases_nonexistent_artist(sample_collection, capsys):
    result = list_artist_releases(sample_collection, artist="Nonexistent Artist")
    
    captured = capsys.readouterr()
    assert "No releases found." in captured.out
    
    assert isinstance(result, pd.DataFrame)
    assert result.empty

def test_list_artist_releases_empty_collection(capsys):
    result = list_artist_releases([])
    
    captured = capsys.readouterr()
    assert "No releases found." in captured.out
    
    assert isinstance(result, pd.DataFrame)
    assert result.empty

def test_list_artist_releases_output_format(sample_collection, capsys):
    list_artist_releases(sample_collection)
    
    captured = capsys.readouterr()
    # Check if the output is formatted as a table
    assert "Artist" in captured.out
    assert "Album" in captured.out
    assert "Genre" in captured.out
    assert "Release Year" in captured.out
    
    # Check if the data is aligned in columns
    lines = captured.out.strip().split('\n')
    assert len(set(len(line) for line in lines)) == 2  # All lines should have the same length

def test_list_artist_releases_return_value(sample_collection):
    result = list_artist_releases(sample_collection)
    
    assert isinstance(result, pd.DataFrame)
    assert set(result.columns) == {'Artist', 'Album', 'Genre', 'Release Year'}
    assert len(result) == 4

@pytest.mark.parametrize("artist, expected_count", [
    ("Artist A", 2),
    ("Artist B", 1),
    ("Artist C", 1),
    ("Nonexistent Artist", 0),
])
def test_list_artist_releases_various_artists(sample_collection, artist, expected_count):
    result = list_artist_releases(sample_collection, artist=artist)
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) == expected_count
    if expected_count > 0:
        assert all(result['Artist'] == artist)

if __name__ == '__main__':
    pytest.main()
