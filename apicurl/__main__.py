import os
import json
from apicurl.fetch_process_collection import fetch_all_collection_pages, process_collection,split_artist_release_percentage,visualize_artist_release_percentage,list_artist_releases

def fetch_and_process():
    dc_all_releases = fetch_all_collection_pages()
    release_collection_db = process_collection(dc_all_releases)
    print("Fetched and processed collection data.")
    return release_collection_db


if __name__ == "__main__":
    pre_collection = False
    collection_path = 'data/Collection.json'

    if os.path.exists(collection_path):
        with open(collection_path) as json_file:
            collection = json.load(json_file)
            pre_collection = True

        release_collection_db = collection

    else:
        print("No previous collection data found. Fetching...")
        release_collection_db = fetch_and_process()

        ### POSSIBLE ISSUE
        print("Saving to file.")
        with open('data/Collection.json', 'w') as json_file:
            json.dump(release_collection_db, json_file)
            print("Saved collection data to file.")

            print("Fetched and processed collection data.")

    ### Another issue
    print("Splitting data into n top artists and others")
    artist_percentages = split_artist_release_percentage(release_collection_db, top_number=10)
    print("Visualize percentages of artists")
    visualize_artist_release_percentage(artist_percentages)
    list_artist_releases(release_collection_db)
