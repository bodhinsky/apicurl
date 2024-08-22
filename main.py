import os
import json
from apicurl.fetch_process_collection import fetch_all_collection_pages, process_collection, save_collection_to_json, split_artist_release_percentage, visualize_artist_release_percentage, list_artist_releases

def fetch_and_process():
    dc_all_releases = fetch_all_collection_pages()
    release_collection_db = process_collection(dc_all_releases)
    print("Fetched and processed collection data.")
    return release_collection_db

if __name__ == "__main__":
    release_collection_db = fetch_and_process()
    save_collection_to_json(release_collection_db, "data/collection.json")
    # print(release_collection_db)
    top_k_artists = split_artist_release_percentage(release_collection_db, 3)
    print(top_k_artists)
    visualize_artist_release_percentage(top_k_artists)
    artist_df = list_artist_releases(release_collection_db, "Biffy Clyro")
    print_unique(release_collection_db)
