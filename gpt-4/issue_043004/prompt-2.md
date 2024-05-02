System Prompt:
----------------
You are an expert software engineer capable of generating code snippets for changes. Generate the code snippets that need to be changed based on the issue description. Please respond with your analysis directly in JSON format The JSON schema should include: {'file': string (full path to file), 'code_snippet': string (code snippet)}.

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
Affected files: {
  "files": [
    {
      "file": "src/apicurl/fetchUserCollection.py"
    },
    {
      "file": "tests/main_test.py"
    },
    {
      "file": "src/apicurl/__init__.py"
    },
    {
      "file": "src/sw_dev_crew/__init__.py"
    },
    {
      "file": "src/sw_dev_crew/visualization.py"
    }
  ]
}
Lines to be changed: {
  "files": [
    {
      "file": "src/apicurl/fetchUserCollection.py",
      "lines_to_be_changed_in_original_and_changed_file": [
        "@@ -22,3 +22,10 @@",
        "+import pandas as pd",
        "+import matplotlib.pyplot as plt",
        "+",
        "+def visualize_collection_data(collection_data):",
        "+    # Transform collection data into a pandas DataFrame",
        "+    df = pd.DataFrame(collection_data)",
        "+    # Example visualization: Histogram of genres",
        "+    df['genre'].value_counts().plot(kind='bar')",
        "+    plt.savefig('collection_genre_distribution.png')"
      ]
    },
    {
      "file": "tests/main_test.py",
      "lines_to_be_changed_in_original_and_changed_file": [
        "@@ -6,3 +6,10 @@",
        "+from apicurl.fetchUserCollection import visualize_collection_data",
        "+",
        "+def test_visualize_collection_data():",
        "+    # Assumes collection_data is a mock or sample data structure matching the expected format",
        "+    collection_data = [{'genre': 'Rock'}, {'genre': 'Pop'}, {'genre': 'Jazz'}]",
        "+    visualize_collection_data(collection_data)",
        "+    assert os.path.isfile('collection_genre_distribution.png')"
      ]
    },
    {
      "file": "src/apicurl/__init__.py",
      "lines_to_be_changed_in_original_and_changed_file": [
        "@@ -0,0 +1,3 @@",
        "+from .fetchUserCollection import visualize_collection_data"
      ]
    },
    {
      "file": "src/sw_dev_crew/__init__.py",
      "lines_to_be_changed_in_original_and_changed_file": [
        "@@ -0,0 +1,1 @@",
        "+from .visualization import create_visualization"
      ]
    },
    {
      "file": "src/sw_dev_crew/visualization.py",
      "lines_to_be_changed_in_original_and_changed_file": [
        "@@ -0,0 +1,15 @@",
        "+import pandas as pd",
        "+import matplotlib.pyplot as plt",
        "+",
        "+def create_visualization(data):",
        "+    # Assuming 'data' needs to be processed into a pandas DataFrame",
        "+    df = pd.DataFrame(data)",
        "+    # Implement specific visualization logic here, for example:",
        "+    if 'release_year' in df.columns:",
        "+        df['release_year'].value_counts().sort_index().plot(kind='line')",
        "+        plt.title('Number of Releases by Year')",
        "+        plt.xlabel('Year')",
        "+        plt.ylabel('Number of Releases')",
        "+        plt.savefig('releases_by_year.png')",
        "+        plt.close()",
        "+    print('Visualization created')"
      ]
    }
  ]
}
