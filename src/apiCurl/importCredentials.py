import json

def getUserCredentials(service: str):
    with open('src/.ld') as f:
        data = f.read()

    login = json.loads(data)

    client_id = login[f'{service}']['client_id']
    client_secret = login[f'{service}']['client_secret']

    return client_id, client_secret