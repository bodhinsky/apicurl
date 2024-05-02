from apiCurl.importCredentials import getUserCredentials
import json
import requests

def get_user_auth_token():

    client_id, client_secret = getUserCredentials(service='Spotify')

    url = "https://accounts.spotify.com/api/token"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'grant_type': 'client_credentials',
        'client_id': {client_id},
        'client_secret': {client_secret}
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()  # Check for HTTP errors

        data = response.json()
        return data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred during the request: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"JSON decoding error occurred: {json_err}")

    if response.status_code == 200:
        return data
    else:
        print("ERROR Fetching User Credentials")
