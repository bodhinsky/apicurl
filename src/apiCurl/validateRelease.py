from getUserToken import get_user_auth_token
import requests
import json

def get_spotify_album(release_name, artist):
    data = get_user_auth_token()
    token_type = data['token_type']
    access_token = data['access_token']
    auth_header = {
        'Authorization': f'{token_type} {access_token}'
    }

    params = {
        'q': f'{release_name} artist:{artist}',
        'type': 'album',
        'limit': '5'
    }

    #print(f"Token still valid for {expiration} Minutes")
    api_url = "https://api.spotify.com/v1/search"


    album_search = requests.get(api_url, headers=auth_header, params=params)
    album_json_object = album_search.json()

    try:
        album_object = album_json_object['albums']['items'][0]
    except IndexError:
        return []

    keys_to_remove = ['available_markets', 'external_urls', 'href', 'images', 'uri', 'type']

    for key in keys_to_remove:
        album_object.pop(key, None)

    artists_name = album_object['artists'][0]['name']
    item_id = album_object['id']
    item_name = album_object['name']
    release_date = album_object['release_date']

    release_info = [{
        'Title': item_name,
        'Artist': artists_name,
        'Year': release_date.split('-')[0],  # Extract year from release date
        'Genre': None,  # You can include genre if available in the data
        'Style': None  # You can include style if available in the data
    }]

    return release_info

def supplement_release_info(release_collection_db):
    for item in release_collection_db:
        title = item['Title']
        artist = item['Artist']
        year = item['Year']
        srelease = get_spotify_album(release_name=title, artist=artist)

        if len(srelease) == 0:
            print(f"{title} by {artist} seems to be missing on Spotify")
            continue

        # In some entries, the year value is not correct
        if year == 0:
            item['Year'] = int(srelease[0]['Year'])
    
    return release_collection_db