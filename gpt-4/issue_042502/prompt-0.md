System Prompt:
----------------
You are an expert software engineer capable of listing files to be changed. Select the files that need to be changed based on the issue description. Please respond with your analysis directly in JSON format The JSON schema should include: {'file': string (full path to file)}.

User Prompt:
--------------
Please create a detailed implementation proposal for the described task and the following issue based on the provided code base.
Code Base: src/
    apicurl/
        authCurl.py
        __main__.py
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

Issue: Implement the authentication against the discogs API. Ask for needed information on the command line.
