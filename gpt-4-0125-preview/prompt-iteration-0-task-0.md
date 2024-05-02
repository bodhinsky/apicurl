System Prompt:
----------------
Act as a software engineering expert! Your job is to generate code based on an issue description to be implemented in a repo. Add line numbers in the code!.
Please respond directly in the following JSON format: The JSON schema should include: {'file': string (full path to file), 'code_snippet': string (code snippet)}. Provide nothing but the JSON output.

User Prompt:
--------------
Here is the issue description and the repo.
Issue:
Improve data processing or fetching, so it handles different writings for artists names. There have been errors due to multiple artists with the same names e.g. Band On The Run by Wings (2) seems to be missing on Spotify - while trying to validate additional information
Repo:
src/
    .DS_Store
    .ld
    apiCurl/
        getUserToken.py
            1: from apiCurl.importCredentials import getUserCredentials
            2: import json
            3: import requests
            4: 
            5: def get_user_auth_token():
            6: 
            7:     client_id, client_secret = getUserCredentials(service='Spotify')
            8: 
            9:     url = "https://accounts.spotify.com/api/token"
            10: 
            11:     headers = {
            12:         'Content-Type': 'application/x-www-form-urlencoded'
            13:     }
            14:     payload = {
            15:         'grant_type': 'client_credentials',
            16:         'client_id': {client_id},
            17:         'client_secret': {client_secret}
            18:     }
            19: 
            20:     try:
            21:         response = requests.post(url, data=payload, headers=headers)
            22:         response.raise_for_status()  # Check for HTTP errors
            23: 
            24:         data = response.json()
            25:         return data
            26: 
            27:     except requests.exceptions.HTTPError as http_err:
            28:         print(f"HTTP error occurred: {http_err}")
            29:     except requests.exceptions.RequestException as req_err:
            30:         print(f"An error occurred during the request: {req_err}")
            31:     except json.JSONDecodeError as json_err:
            32:         print(f"JSON decoding error occurred: {json_err}")
            33: 
            34:     if response.status_code == 200:
            35:         return data
            36:     else:
            37:         print("ERROR Fetching User Credentials")
        validateRelease.py
        importCredentials.py
        exportToTable.py
        authCurl.py
        fetchUserCollection.py
        dataProcessing.py
            1: def process_collection(collection):
            2:     if not collection:
            3:         return None
            4: 
            5:     collection_info = []
            6:     for release in collection:
            7:         title = release['basic_information']['title']
            8:         artist = release['basic_information']['artists'][0]['name']
            9:         year = release['basic_information']['year']
            10:         genre = release['basic_information']['genres'][0] if release['basic_information']['genres'] else None
            11:         style = release['basic_information']['styles'][0] if release['basic_information']['styles'] else None
            12:         collection_info.append({
            13:             'Title': title,
            14:             'Artist': artist,
            15:             'Year': year,
            16:             'Genre': genre,
            17:             'Style': style,
            18:         })
            19:     return collection_info
        __main__.py
        __pycache__/
            exportToTable.cpython-311.pyc
            getUserToken.cpython-311.pyc
            validateRelease.cpython-311.pyc
            llm.cpython-311.pyc
            importCredentials.cpython-311.pyc
            fetchUserCollection.cpython-311.pyc
            __main__.cpython-312.pyc
            dataProcessing.cpython-311.pyc
            __main__.cpython-311.pyc
    apiCurl.egg-info/
        PKG-INFO
        SOURCES.txt
        entry_points.txt
        top_level.txt
        dependency_links.txt
tests/
    .DS_Store
    my_test.py
        1: from apiCurl.dataProcessing import process_collection
        2: 
        3: collection_path = 'data/Collection.json'
        4: 
        5: if os.path.exists(collection_path):
        6:     with open(collection_path) as json_file:
        7:         collection = json.load(json_file)
        8: 
        9: def test_process_data():
        10:     assert not process_collection(collection)==[]
        11: 
    __pycache__/
        my_test.cpython-311-pytest-8.1.1.pyc
        my_test.cpython-312-pytest-8.1.1.pyc

