import os
from unittest.mock import patch, Mock
import pytest
from apicurl.user_auth import get_user_credentials
from apicurl.fetch_process_collection import get_user_collection, fetch_all_collection_pages, process_collection, split_artist_release_percentage, visualize_artist_release_percentage
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from io import BytesIO

# Set the Agg backend for matplotlib
plt.switch_backend('Agg')

@pytest.fixture
def valid_dataframe():
    return pd.DataFrame({
        'Artist': ['Artist A', 'Artist B', 'Artist C'],
        'Percentage': [40, 30, 30]
    })

@pytest.fixture
def empty_dataframe():
    return pd.DataFrame({
        'Artist': [],
        'Percentage': []
    })

@pytest.fixture
def invalid_dataframe():
    return pd.DataFrame({
        'Artist': ['Artist A', 'Artist B', 'Artist C'],
        'Percent': [40, 30, 30]
    })


def test_valid_dataframe(valid_dataframe):
    try:
        visualize_artist_release_percentage(valid_dataframe)
    except Exception as e:
        pytest.fail(f"visualize_artist_release_percentage raised an exception with valid dataframe: {e}")

def test_empty_dataframe(empty_dataframe):
    with pytest.raises(ValueError):
        visualize_artist_release_percentage(empty_dataframe)

def test_invalid_dataframe(invalid_dataframe):
    with pytest.raises(ValueError):
        visualize_artist_release_percentage(invalid_dataframe)

def test_plot_creation(valid_dataframe):
    plt.ioff()  # Turn off interactive mode to prevent plot from showing

    visualize_artist_release_percentage(valid_dataframe)
    
    fig = plt.gcf()  # Get current figure
    ax = fig.gca()
    wedges = [patch for patch in ax.patches if isinstance(patch, Wedge)]

    plt.close(fig)  # Close the figure after capturing its content

    # Ensure the plot has wedges (pie slices)
    assert len(wedges) == len(valid_dataframe), "Plot was not created correctly."


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

@patch('apicurl.fetch_process_collection.split_artist_release_percentage')
def test_split_artist_release_percentage(mock_split, sample_collection):
    # Mock setup
    artist_release_percentage = pd.DataFrame({
        'Artist': ['Artist A', 'Artist B', 'Artist C'],
        'Percentage': [50.0, 25.0, 25.0]
    })
    mock_split.return_value = artist_release_percentage

    # Call the function
    result = split_artist_release_percentage(sample_collection, top_number=3)

    # Assertions
    assert isinstance(result, pd.DataFrame)
    assert 'Artist' in result.columns
    assert 'Percentage' in result.columns
    pd.testing.assert_frame_equal(result, artist_release_percentage)

    # Edge case: Empty dataframe
    empty_df = pd.DataFrame(columns=['Artist', 'releases'])
    result = split_artist_release_percentage(empty_df, 0)
    assert result is None


if __name__ == '__main__':
    pytest.main()