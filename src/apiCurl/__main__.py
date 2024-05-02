import os, logging, pyfiglet, readchar, json
from fetchUserCollection import fetch_all_collection_pages
from dataProcessing import process_collection
from validateRelease import supplement_release_info
from exportToTable import export_to_dataframe, export_to_xlsx
from ollama import Client

def fetch_and_process():
    dc_all_releases = fetch_all_collection_pages()
    release_collection_db = process_collection(dc_all_releases)
    print("Fetched and processed collection data.")
    return release_collection_db

def supplement_collection():
    supplemented_collection = supplement_release_info(release_collection_db)
    if supplemented_collection:
        print("Supplemented release information successfully.")
    else:
        print("Failed to supplement release information.")

def export_collection():
    print("test")
    #if 'release_collection_db' in globals():
    if os.path.exists(collection_path):
        try:
            df = export_to_dataframe(release_collection_db)
            print(df)
            export_to_xlsx(df)
            print("Exported collection to Excel successfully.")
        except Exception as e:
            logging.error(f"Error exporting collection: {e}", exc_info=True)
    else:
        print("Release collection database not found. Please fetch and process collection first.")

def ask_llm():
    client = Client(host='http://localhost:11434')

    while True:
        question = input("\nAsk a question about the music release database (type 'exit' to stop): ")
        
        if question.lower() == "exit":
            break
        
        response = client.chat(model='llama3', messages=[
            {
                'role': 'user',
                'content': f'{question}',
                'context': f'my personal music collection = {collection}'
            }
        ])

        print("\nYour question: " + question + "\nAnswer: " + response['message']['content'])

def show_menu(options, current_selection):
    for index, option in enumerate(options):
        if index == current_selection:
            print(f"> {option}")
        else:
            print(f"  {option}")

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

    while True:
        print("\033[H\033[J", end='')  # Clear screen
        print(title + "\n")

        if pre_collection:
            print("INFO:\nCollection file found.\n")

        print("Menu:")
        show_menu(options, current_selection)

        key = readchar.readkey()

        if key == readchar.key.UP:
            current_selection = (current_selection - 1) % len(options)
        elif key == readchar.key.DOWN:
            current_selection = (current_selection + 1) % len(options)
        elif key == readchar.key.ENTER:
            print("\033[H\033[J", end='')  # Clear screen
            if current_selection == 0:
                release_collection_db = fetch_and_process()
                export_to_dataframe(release_collection_db)
            elif current_selection == 1:
                supplement_collection()
            elif current_selection == 2:
                export_collection()
            elif current_selection == 3:
                ask_llm()
            elif current_selection == 4:
                print("Exiting the program.")
                break
            input("Press Enter to continue...")
