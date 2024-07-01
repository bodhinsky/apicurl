import requests
from apicurl.user_auth import get_user_credentials
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def get_user_collection(page=1):
    """
    Retrieves a user's Discogs collection, one page at a time.

    Args:
        page (int): The page number to fetch. Default is 1.

    Returns:
        tuple: A tuple containing the list of releases and the URL of the next page if available.
    """

    user_name, user_token = get_user_credentials(service='discogs')

    # Define the headers for the request
    headers = {
        'Authorization': f'Discogs token={user_token}',
        'User-Agent': 'DiscogsCollectionExporter/1.0'
    }

    # Construct the URL for the request
    url = f'https://api.discogs.com/users/{user_name}/collection/folders/0/releases?page={page}'
    
    try:
        # Send a GET request to the API and handle any exceptions
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the JSON response
        collection_data = response.json()

        # Determine if there are more pages to fetch
        max_pages = collection_data['pagination']['pages']
        if page < max_pages:
            return collection_data['releases'], collection_data['pagination']['urls']['next']
        else:
            return collection_data['releases'], False

    except requests.exceptions.RequestException as e:
        print(f'Error fetching collection: {e}')
        return [], False


def fetch_all_collection_pages():
    """
    Fetches all pages of a user's Discogs collection.
    
    Returns:
        list: A list of all releases in the user's collection.
    """

    all_releases = []
    next_page = True
    page_number = 1
    
    while next_page:
        # Get the releases for the current page and determine if there's a next page
        releases, next_page_url = get_user_collection(page_number)
        next_page = next_page_url
        all_releases.extend(releases)  # Add the releases to the list
        page_number += 1

    return all_releases

def process_collection(collection):  # Process a collection of Discogs releases.
    """
    Processes a collection of Discogs releases and returns a structured representation.

    Args:
        collection (list): A list of Discogs release data.

    Returns:
        list: A structured list of releases, with each release represented as a dictionary.
    """

    if not collection:  # If the collection is empty, return None
        return None
    
    collection_info = []  # Initialize an empty list to store the processed collection
    
    for release in collection:  # Iterate over each release in the collection
        title = release['basic_information']['title']  # Get the title of the release
        artist = release['basic_information']['artists'][0]['name']  # Get the name of the primary artist
        year = release['basic_information']['year']  # Get the release year
        genre = release['basic_information']['genres'][0] if release['basic_information']['genres'] else None  # Get the primary genre or None if no genres are present
        style = release['basic_information']['styles'][0] if release['basic_information']['styles'] else None  # Get the primary style or None if no styles are present
        
        collection_info.append({  # Create a dictionary to represent the release and add it to the list
            'Title': title,
            'Artist': artist,
            'Year': year,
            'Genre': genre,
            'Style': style,
        })
    
    return collection_info  # Return the processed collection

def split_artist_release_percentage(collection, top_number):
    if isinstance(collection, list) and len(collection) > 0:   # If the collection is a list and contains at least one item, process it
        df = pd.DataFrame(collection)

        # Check if 'Artist' column exists in the DataFrame
        if 'Artist' not in df.columns:
            raise ValueError("The collection does not contain an 'artist' column")

        # Calculate the percentage of releases for each artist
        artist_counts = df['Artist'].value_counts(normalize=True) * 100
        artist_percentages = artist_counts.reset_index()
        artist_percentages.columns = ['Artist', 'Percentage']

        # Separate the top 10 artists
        top_artists = artist_percentages.head(top_number)

        # Calculate the percentage for "Others"
        others_percentage = artist_percentages['Percentage'][top_number:].sum()

        # Append the "Others" row
        if others_percentage > 0:
            top_artists = top_artists._append({'Artist': 'Others', 'Percentage': others_percentage}, ignore_index=True)
        return top_artists
    else:
        return None

def visualize_artist_release_percentage(dataframe):
    # Create a bar plot to show the percentage of artists
    plt.figure(figsize=(10, 6))
    plt.pie(dataframe['Percentage'], labels=dataframe['Artist'], autopct='%1.1f%%', startangle=140)

    # Adding titles
    plt.title('Percentage of Music Releases by Artist')

    # Display the plot
    plt.show()

def update_data_model_and_storage(dataframe):
    return

def enhance_ui_with_artist_release_percentage_visualization(visualization):
    return

def optimize_performance_for_data_processing_and_visualization(dataframe):
    return
    