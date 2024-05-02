System Prompt:
----------------
Act as a software engineering expert! Your job is to create patch strings for a given Python repository. Make sure to consider the line numbers in the patch!.
Please respond directly in the following JSON format: The JSON schema should include: {'patch_string': string (diff --git a/...)}. Provide nothing but the JSON output.

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

Here is the output from a previous task that might be useful:
Code snippets for changes: {
"file": "src/apiCurl/fetchUserCollection.py",
"code_snippet": "1: from importCredentials import getUserCredentials\n2: import requests\n3: \n4: def get_user_collection(page=1):\n5:     \"\"\"Fetches a user's collection from Discogs for a specified page.\n6: \n7:     Args:\n8:         page (int, optional): The page number to fetch. Defaults to 1.\n9: \n10:     Returns:\n11:         tuple: A tuple containing the list of releases and either the URL to the next page or False if there is no next page.\n12:     \"\"\"\n13:     user_name, user_token = getUserCredentials(service='Discogs')\n14: \n15:     headers = {\n16:         'Authorization': f'Discogs token={user_token}',\n17:         'User-Agent': 'DiscogsCollectionExporter/1.0'\n18:     }\n19:     url = f'https://api.discogs.com/users/{user_name}/collection/folders/0/releases?page={page}'\n20: \n21:     try:\n22:         response = requests.get(url, headers=headers)\n23:         response.raise_for_status()  # Raise an exception for bad status codes\n24:         collection_data = response.json()\n25:         max_pages = collection_data['pagination']['pages']\n26:         if page < max_pages:\n27:             return collection_data['releases'], collection_data['pagination']['urls']['next']\n28:         else:\n29:             return collection_data['releases'], False\n30:     except requests.exceptions.RequestException as e:\n31:         print(f\"Error fetching collection: {e}\")\n32:         return [], False\n33: \n34: def fetch_all_collection_pages():\n35:     \"\"\"Fetches all pages of a user's collection from Discogs.\n36: \n37:     Returns:\n38:         list: A list of all releases in the user's collection.\n39:     \"\"\"\n40:     all_releases = []\n41:     next_page = True\n42:     page_number = 1\n43: \n44:     while next_page:\n45:         releases, next_page_url = get_user_collection(page_number)\n46:         next_page = next_page_url\n47:         all_releases.extend(releases)\n48:         page_number += 1\n49: \n50:     return all_releases\n"
}
