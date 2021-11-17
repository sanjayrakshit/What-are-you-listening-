import json
from datetime import datetime
from typing import Dict


def convert_to_iso_format(given_time: datetime) -> str:
    """
    Convert the time to iso format
    :param given_time: The required time for conversion
    :return: iso format time
    """
    return given_time.isoformat()


def save_json_local(data: Dict, path: str) -> None:
    """
    Saves the json data to local
    :param data: data to save
    :param path: path to save
    :return:
    """
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def load_json_data(path: str) -> Dict:
    """
    loads the json data and returns it
    :param path: the path to load from
    :return: The json data
    """
    with open(path, 'r') as f:
        _creds = json.load(f)
    return _creds
