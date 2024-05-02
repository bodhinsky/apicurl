System Prompt:
----------------
Act as a software engineering expert! Your job is to generate code based on an issue description to be implemented in a repo. Add line numbers in the code!.
Please respond directly in the following JSON format: The JSON schema should include: {'file': string (full path to file), 'code_snippet': string (code snippet)}. Provide nothing but the JSON output.

User Prompt:
--------------
Here is the issue description and the repo.
Issue:
Provide comprehensive docstrings for the code supplied
Repo:
src/
    .DS_Store
    .ld
    apiCurl/
        getUserToken.py
        validateRelease.py
        importCredentials.py
        exportToTable.py
        fetchUserCollection.py
            1: from importCredentials import getUserCredentials
            2: import requests
            3: 
            4: def get_user_collection(page=1):
            5: 
            6:     user_name, user_token = getUserCredentials(service='Discogs')
            7: 
            8:     headers = {
            9:         'Authorization': f'Discogs token={user_token}',
            10:         'User-Agent': 'DiscogsCollectionExporter/1.0'
            11:     }
            12:     url = f'https://api.discogs.com/users/{user_name}/collection/folders/0/releases?page={page}'
            13: 
            14:     try:
            15:         response = requests.get(url, headers=headers)
            16:         response.raise_for_status()  # Raise an exception for bad status codes
            17:         collection_data = response.json()
            18:         max_pages = collection_data['pagination']['pages']
            19:         if page < max_pages:
            20:             return collection_data['releases'], collection_data['pagination']['urls']['next']
            21:         else:
            22:             return collection_data['releases'], False
            23:     except requests.exceptions.RequestException as e:
            24:         print(f"Error fetching collection: {e}")
            25:         return [], False
            26: 
            27: def fetch_all_collection_pages():
            28:     all_releases = []
            29:     next_page = True
            30:     page_number = 1
            31: 
            32:     while next_page:
            33:         releases, next_page_url = get_user_collection(page_number)
            34:         next_page = next_page_url
            35:         all_releases.extend(releases)
            36:         page_number += 1
            37: 
            38:     return all_releases
        dataProcessing.py
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
        1: from apiCurl.fetchUserCollection import fetch_all_collection_pages
        2: 
        3: def test_collection_data():
        4:     assert len(fetch_all_collection_pages()) == 0
    __pycache__/
        my_test.cpython-311-pytest-8.1.1.pyc
        my_test.cpython-312-pytest-8.1.1.pyc

