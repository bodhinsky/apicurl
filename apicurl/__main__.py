import os
import json
from apicurl.fetch_process_collection import fetch_all_collection_pages, process_collection,split_artist_release_percentage,visualize_artist_release_percentage,list_artist_releases

def fetch_and_process():
    dc_all_releases = fetch_all_collection_pages()
    release_collection_db = process_collection(dc_all_releases)
    print("Fetched and processed collection data.")
    return release_collection_db


if __name__ == "__main__":
    release_collection_db = fetch_and_process()

    print("Saving to file.")
    with open('data/Collection.json', 'w') as json_file:
        json.dump(release_collection_db, json_file)
        print("Saved collection data to file.")

        print("Fetched and processed collection data.")
