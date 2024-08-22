from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

def get_user_credentials(service: str) -> tuple:
    """
    Retrieves client ID and secret for a given service from a JSON file.
    
    Args:
        service (str): The name of the service for which to retrieve credentials.

    Returns:
        A tuple containing the client ID and secret for the specified service.

    Raises:
        ValueError: If the service is not found in the JSON file or if the JSON file does not exist.
    """

    user_name = os.getenv(f'{service.upper()}_USER_NAME')
    user_secret = os.getenv(f'{service.upper()}_USER_TOKEN')

    if user_name is None:
        raise EnvironmentError(f"Environment variable {service.upper()}_USER_NAME is not set.")

    if user_secret is None:
        raise EnvironmentError(f"Environment variable {service.upper()}_USER_TOKEN is not set.")
    
    return user_name, user_secret

def get_user_auth_token():
    """
    Retrieves the user's authentication token for a given service.

    This function is used to obtain an authentication token for a specified service.
    The token can then be used to authenticate subsequent requests to the service's API.

    :return: A JSON object containing the user's authentication token
    """
    client_id, client_secret = get_user_credentials(service='Spotify')

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

        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            return data
        else:
            print(f"ERROR Fetching User Credentials\n{response}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred during the request: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"JSON decoding error occurred: {json_err}")
