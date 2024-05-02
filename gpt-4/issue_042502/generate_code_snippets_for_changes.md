{
  "changes": [
    {
      "file": "src/apicurl/authCurl.py",
      "code_snippet": "import requests\nfrom getpass import getpass\n\ndef authenticate(url):\n    user = input('Enter your username:')\n    password = getpass('Enter your password:')\n    response = requests.get(url, auth=(user, password))\n    return response.status_code == 200\n"
    },
    {
      "file": "src/apicurl/__main__.py",
      "code_snippet": "from .authCurl import authenticate\n\nif __name__ == '__main__':\n    url = 'https://api.discogs.com'\n    if authenticate(url):\n        print('Authentication successful')\n    else:\n        print('Authentication failed')\n"
    }
  ]
}