import json
import requests

def getUserCredentials(service: str) -> tuple:
    """
    Retrieves client ID and secret for a given service from a JSON file.
    
    Args:
        service (str): The name of the service for which to retrieve credentials.

    Returns:
        A tuple containing the client ID and secret for the specified service.

    Raises:
        ValueError: If the service is not found in the JSON file or if the JSON file does not exist.
    """
    # Open and read the JSON file, expecting it to be located at 'src/.ld'
    with open('src/.ld') as f:
        data = json.loads(f.read())

    # Load client ID and secret for the specified service from the JSON data
    login = data[service]
    if not isinstance(login, dict) or 'client_id' not in login or 'client_secret' not in login:
        raise ValueError(f"Invalid credentials found for service '{service}'")
    client_id = login['client_id']
    client_secret = login['client_secret']

    return client_id, client_secret

def get_user_auth_token():
    """
    Retrieves the user's authentication token for a given service.

    This function is used to obtain an authentication token for a specified service.
    The token can then be used to authenticate subsequent requests to the service's API.

    :return: A JSON object containing the user's authentication token
    """
    client_id, client_secret = getUserCredentials(service='Spotify')

    url = "https://accounts.spotify.com/api/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        'grant_type': 'client_credentials',
        'client_id': {client_id},
        'client_secret': {client_secret}
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        # Check for HTTP errors
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()
        return data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred during the request: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"JSON decoding error occurred: {json_err}")

    # If the response status code is 200, return the data
    if response.status_code == 200:
        return data
    else:
        print("ERROR Fetching User Credentials")
