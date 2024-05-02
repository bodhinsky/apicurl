from importCredentials import getUserCredentials
import requests

def get_user_collection(page=1):

    user_name, user_token = getUserCredentials(service='Discogs')

    headers = {
        'Authorization': f'Discogs token={user_token}',
        'User-Agent': 'DiscogsCollectionExporter/1.0'
    }
    url = f'https://api.discogs.com/users/{user_name}/collection/folders/0/releases?page={page}'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        collection_data = response.json()
        max_pages = collection_data['pagination']['pages']
        if page < max_pages:
            return collection_data['releases'], collection_data['pagination']['urls']['next']
        else:
            return collection_data['releases'], False
    except requests.exceptions.RequestException as e:
        print(f"Error fetching collection: {e}")
        return [], False

def fetch_all_collection_pages():
    all_releases = []
    next_page = True
    page_number = 1
    
    while next_page:
        releases, next_page_url = get_user_collection(page_number)
        next_page = next_page_url
        all_releases.extend(releases)
        page_number += 1
    
    return all_releases
