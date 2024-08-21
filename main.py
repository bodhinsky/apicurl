import os
import json
from apicurl.fetch_process_collection import fetch_all_collection_pages, process_collection, save_collection_to_json

def fetch_and_process():
    dc_all_releases = fetch_all_collection_pages()
    release_collection_db = process_collection(dc_all_releases)
    print("Fetched and processed collection data.")
    return release_collection_db

if __name__ == "__main__":
    release_collection_db = fetch_and_process()
    save_collection_to_json(release_collection_db, "data/collection.json")
    print(release_collection_db)
