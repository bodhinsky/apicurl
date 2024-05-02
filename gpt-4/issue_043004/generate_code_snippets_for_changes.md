{
  "changes": [
    {
      "file": "src/apicurl/fetchUserCollection.py",
      "code_snippet": "import pandas as pd\nimport matplotlib.pyplot as plt\n\ndef get_user_collection(page=1):\n    # Existing code here\n\n\ndef visualize_collection_data(collection_data):\n    df = pd.DataFrame(collection_data)\n    df['genre'].value_counts().plot(kind='bar')\n    plt.savefig('collection_genre_distribution.png')"
    },
    {
      "file": "tests/main_test.py",
      "code_snippet": "from apicurl.fetchUserCollection import visualize_collection_data\nimport os\n\ndef test_visualize_collection_data():\n    collection_data = [{'genre': 'Rock'}, {'genre': 'Pop'}, {'genre': 'Jazz'}]\n    visualize_collection_data(collection_data)\n    assert os.path.isfile('collection_genre_distribution.png')"
    },
    {
      "file": "src/apicurl/__init__.py",
      "code_snippet": "from .fetchUserCollection import visualize_collection_data"
    },
    {
      "file": "src/sw_dev_crew/__init__.py",
      "code_snippet": "from .visualization import create_visualization"
    },
    {
      "file": "src/sw_dev_crew/visualization.py",
      "code_snippet": "import pandas as pd\nimport matplotlib.pyplot as plt\n\ndef create_visualization(data):\n    df = pd.DataFrame(data)\n    if 'release_year' in df.columns:\n        df['release_year'].value_counts().sort_index().plot(kind='line')\n        plt.title('Number of Releases by Year')\n        plt.xlabel('Year')\n        plt.ylabel('Number of Releases')\n        plt.savefig('releases_by_year.png')\n        plt.close()\n    print('Visualization created')"
    }
  ]
}