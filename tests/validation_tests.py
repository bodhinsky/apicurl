import pytest
from apiCurl.validateRelease import get_spotify_album, supplement_release_info

# Test 1: Valid input returns expected album data
def test_get_spotify_album_valid_input():
    release_name = "Puzzle"
    artist = "Biffy Clyro"
    album_data = get_spotify_album(release_name, artist)
    assert len(album_data) == 1
    assert album_data[0]['Title'] == 'Opposites'
    assert album_data[0]['Artist'] == 'Biffy Clyro'

# Test 2: Invalid input returns empty list
def test_get_spotify_album_invalid_input():
    release_name = "Nonexistent Album"
    artist = "Unknown Artist"
    album_data = get_spotify_album(release_name, artist)
    assert len(album_data) == 0

# Test 3: Supplement release info correctly updates year for invalid input
def test_supplement_release_info_valid_update():
    release_collection_db = [
        {'Title': 'Opposites', 'Artist': 'Biffy Clyro', 'Year': 0},
        {'Title': 'Bon Iver, Bon Iver', 'Artist': 'Bon Iver', 'Year': 2011}
    ]
    supplemented_data = supplement_release_info(release_collection_db)
    assert supplemented_data[0]['Year'] == 2007
    assert supplemented_data[1]['Year'] == 2011

# Test 4: Supplement release info handles missing Spotify data correctly
def test_supplement_release_info_missing_spotify_data():
    release_collection_db = [
        {'Title': 'Nonexistent Album', 'Artist': 'Unknown Artist', 'Year': 0}
    ]
    supplemented_data = supplement_release_info(release_collection_db)
    assert len(supplemented_data) == 1
    assert supplemented_data[0]['Year'] == 0
    print(f"{supplemented_data[0]['Title']} by {supplemented_data[0]['Artist']} seems to be missing on Spotify")

# Test 5: Supplement release info correctly prints error message for missing data
def test_supplement_release_info_error_message():
    release_collection_db = [
        {'Title': 'Opposites', 'Artist': 'Biffy Clyro', 'Year': 0}
    ]
    supplemented_data = supplement_release_info(release_collection_db)
    assert len(supplemented_data) == 1
    print(f"{supplemented_data[0]['Title']} by {supplemented_data[0]['Artist']} seems to be missing on Spotify")