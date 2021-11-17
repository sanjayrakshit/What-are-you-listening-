import requests
import json
import base64
import utils
from datetime import datetime, timedelta
from typing import Dict, List


def get_auth(path: str) -> Dict:
    """
    Gets the authentication token using the Spotify API
    :param path: Path to the credentials file
    :return: Authentication token
    """
    creds_data = utils.load_json_data(path)
    client_id = creds_data.get('client_id')
    client_secret = creds_data.get('client_secret')
    creds = f'{client_id}:{client_secret}'
    b64_creds = base64.b64encode(creds.encode())
    url = 'https://accounts.spotify.com/api/token'
    body = {'grant_type': 'client_credentials'}
    headers = {'Authorization': f'Basic {b64_creds.decode()}'}
    r = requests.post(url=url, data=body, headers=headers)
    return r.json()


def get_current_user_profile(auth_token: str) -> Dict:
    """
    Do not use this method, it will cause a block for you IP
    :param auth_token: authentication token
    :return: User profile details from the API
    """
    raise ConnectionRefusedError('Getting user_profile using current auth_token would result in a ban')
    url = 'https://api.spotify.com/v1/me'
    header = {'Accept': 'application/json',
              'Content-Type': 'application/json',
              'Authorization': f'Bearer {auth_token}'}
    r = requests.get(url=url, headers=header)
    r = r.json()
    return r


def get_featured_playlist(auth_token: str, time: datetime, limit: int = 10) -> Dict:
    """
    Get the featured playlist from the Spotify API
    :param auth_token: authentication token
    :param time: time for which you want the playlist
    :param limit: How many playlists you want to fetch
    :return: Playlist in a Dict
    """
    time = utils.convert_to_iso_format(time)
    url = f'https://api.spotify.com/v1/browse/featured-playlists?timestamp={time}&limit={limit}&offset=0'
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json',
               'Authorization': f'Bearer {auth_token}'}
    r = requests.get(url=url, headers=headers)
    r = r.json()
    return r
