System Prompt:
----------------
You are an expert software engineer capable of listing files to be changed. Select the files that need to be changed based on the issue description. Please respond with your analysis directly in JSON format The JSON schema should include: {'file': string (full path to file)}.

User Prompt:
--------------
Please create a detailed implementation proposal for the described task and the following issue based on the provided code base.
Code Base: src/
    apicurl/
        authCurl.py
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
            25:         return [], None
            26: 
            27: def fetch_all_collection_pages():
            28:     all_releases = []
            29:     next_page = True
            30:     page_number = 1
            31: 
            32:     while next_page:
            33:         releases, next_page_url = get_user_collection()
            34:         all_releases.extend(releases)
            35:         next_page = next_page_url
            36:         page_number += 1
            37: 
            38:     return all_releases
        __main__.py
    sw_dev_crew/
        crew.py
        runit.py
        config/
            agents.yaml
            tasks.yaml
    diff_patch_search.egg-info/
        PKG-INFO
        SOURCES.txt
        entry_points.txt
        top_level.txt
        dependency_links.txt
    diff_patch_search/
        describe_repo.py
        repo-description.txt
        generate_patch.py
        sandbox.py
        call_openai.py
        __main__.py
        __pycache__/
            call_openai.cpython-311.pyc
            describe_repo.cpython-311.pyc
            generate_patch.cpython-311.pyc
            __main__.cpython-311.pyc
tests/
    main_test.py
        1: from apicurl import authenticate, getdata
        2: 
        3: def test_authenticate_against_api(url: Str):
        4:     assert authenticate(url) == True
        5: 
        6: def test_data_curl(url: Str):
        7:     assert getdata(url)

Issue: Given the file, please extend the code so that the user collection data will be visualized as graphs based on sensible attributes in a pandas context and save the graphs into files and write tests
