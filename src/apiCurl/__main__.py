import os, logging, pyfiglet, readchar, json
from fetchProcessCollection import fetch_all_collection_pages, process_collection

def fetch_and_process():
    dc_all_releases = fetch_all_collection_pages()
    release_collection_db = process_collection(dc_all_releases)
    print("Fetched and processed collection data.")
    return release_collection_db


if __name__ == "__main__":
    options = ["Fetch and Process Collection", "Supplement Collection", "Export Collection", "Ask about your collection", "Exit"]
    current_selection = 0
    pre_collection = False
    title = pyfiglet.figlet_format("apiCurl")
    collection_path = 'data/Collection.json'

    if os.path.exists(collection_path):
        with open(collection_path) as json_file:
            collection = json.load(json_file)
            pre_collection = True

        release_collection_db = collection

    else:
        release_collection_db = fetch_and_process()

    print(release_collection_db)
