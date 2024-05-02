System Prompt:
----------------
You are an expert software engineer capable of creating patch strings. Create a patch string based on the issue description. Please respond with your analysis directly in JSON format The JSON schema should include: {'patch_string': string (diff --git a/...)}.

User Prompt:
--------------
Please create a detailed implementation proposal for the described task and the following issue based on the provided code base.
Code Base: src/
    apicurl/
        authCurl.py
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

Issue: I want to fetch my user collection from discogs and save it permanently onto my machine.
Affected files: {
  "files": [
    {"file": "src/apicurl/authCurl.py"},
    {"file": "src/apicurl/__main__.py"},
    {"file": "src/sw_dev_crew/config/tasks.yaml"},
    {"file": "src/sw_dev_crew/runit.py"},
    {"file": "tests/main_test.py"}
  ]
}
Lines to be changed: {
  "files": [
    {
      "file": "src/apicurl/authCurl.py",
      "lines_to_be_changed_in_original_and_changed_file": [
        "@@ -1,2 +1,10 @@"
      ]
    },
    {
      "file": "src/apicurl/__main__.py",
      "lines_to_be_changed_in_original_and_changed_file": [
        "@@ -1,2 +1,10 @@"
      ]
    },
    {
      "file": "src/sw_dev_crew/config/tasks.yaml",
      "lines_to_be_changed_in_original_and_changed_file": [
        "@@ -1,2 +1,10 @@"
      ]
    },
    {
      "file": "src/sw_dev_crew/runit.py",
      "lines_to_be_changed_in_original_and_changed_file": [
        "@@ -1,2 +1,10 @@"
      ]
    },
    {
      "file": "tests/main_test.py",
      "lines_to_be_changed_in_original_and_changed_file": [
        "@@ -6,2 +6,10 @@"
      ]
    }
  ]
}
Code snippets for changes: {
  "implementation_proposal": [
    {
      "file": "src/apicurl/authCurl.py",
      "code_snippet": "import requests\n\n# Existing authentication function\n\ndef save_discogs_collection(user_token, file_path):\n    \"\"\"Fetch and save user's Discogs collection.\"\"\"\n    base_url = 'https://api.discogs.com/users/'\n    headers = {'Authorization': 'Discogs token=' + user_token}\n    response = requests.get(f'{base_url}/{user_id}/collection/folders/0/releases', headers=headers)\n    with open(file_path, 'w') as f:\n        f.write(response.text)"
    },
    {
      "file": "src/apicurl/__main__.py",
      "code_snippet": "from .authCurl import save_discogs_collection\n\nif __name__ == '__main__':\n    user_token = 'YOUR_DISCOGS_TOKEN'\n    file_path = 'path/to/save/collection.json'\n    save_discogs_collection(user_token, file_path)"
    },
    {
      "file": "src/sw_dev_crew/config/tasks.yaml",
      "code_snippet": "tasks:\n  - fetch_discogs_collection:\n      description: Fetch and save Discogs music collection\n      enabled: true\n      user_token: YOUR_DISCOGS_TOKEN\n      file_path: 'path/to/save/collection.json'"
    },
    {
      "file": "src/sw_dev_crew/runit.py",
      "code_snippet": "import yaml\nfrom apicurl.authCurl import save_discogs_collection\n\nwith open('config/tasks.yaml', 'r') as file:\n    tasks = yaml.safe_load(file)\n\ntask = tasks['tasks'][0]['fetch_discogs_collection']\nif task['enabled']:\n    save_discogs_collection(task['user_token'], task['file_path'])"
    },
    {
      "file": "tests/main_test.py",
      "code_snippet": "from apicurl.authCurl import save_discogs_collection\nimport os\n\ndef test_save_discogs_collection(tmp_path):\n    user_token = 'FAKE_TOKEN_FOR_TEST'\n    file_path = tmp_path / 'collection_test.json'\n    save_discogs_collection(user_token, file_path)\n    assert os.path.exists(file_path)\n    assert os.path.getsize(file_path) > 0"
    }
  ]
}
