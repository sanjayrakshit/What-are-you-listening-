import json
from datetime import datetime, timedelta
import utils
from dataclasses import dataclass, asdict, field
from spotify import get_auth, get_featured_playlist
from db_utils import MongoConnection
from typing import List, Optional, Dict, Union


@dataclass()
class CuratedPlaylistInfo:
    """
    Class to store the curated playlist info
    """
    id: str = ''
    name: str = ''
    description: str = ''
    time: datetime = field(default_factory=datetime)
    external_link: str = ''


def convert_to_structured(data_dump: Dict, time: datetime) -> List:
    """
    Converts the fetched data into a class object with only required params
    :param data_dump: The entire playlist data
    :param time: The time
    :return: List of the class objects
    """
    playlist_infos = []
    for item in data_dump.get('playlists').get('items'):
        playlist_info = CuratedPlaylistInfo(id=item.get('id'),
                                            name=item.get('name'),
                                            description=item.get('description'),
                                            time=time,
                                            external_link=item.get('external_urls').get('spotify'))
        playlist_infos.append(playlist_info)

    return playlist_infos


def push_documents_to_db(documents: List[Union[CuratedPlaylistInfo, Dict]], mdb: MongoConnection) -> None:
    """
    Pushes the documents to db after a bit of restructuring
    :param documents: The documents that you want to push
    :param mdb: the mongo db class object from db_utils
    :return: None
    """
    if isinstance(documents[0], CuratedPlaylistInfo):
        documents = [asdict(i) for i in documents]
    mdb.insert_many_documents(documents)


def runner(spotify_credentials_path: str, db_credentials_path, start_date: datetime, stop_date: datetime,
           delta: timedelta = timedelta(days=1),
           batch_size: int = 10) -> None:
    """
    Runner method which handles all the flow
    :param spotify_credentials_path: Credentials of spotify
    :param db_credentials_path: Credentials of mongo db
    :param start_date: "From date" to start fetching
    :param stop_date: "To date" to stop fetching at
    :param delta: Time difference gap
    :param batch_size: batch_size/interval at which you would want to push to eliminate too frequent write operations
    :return: None
    """
    # Create connection to DB with default connection url and select database and collection
    mongo = MongoConnection()
    mongo.load_creds(db_credentials_path)
    mongo.connect()
    mongo.set_database('spotify_data')
    mongo.set_collection('featured_playlist')

    # Load spotify credentials
    auth_info = get_auth(spotify_credentials_path)

    iter = 1
    dumps = []
    while start_date <= stop_date:
        featured_playlist = get_featured_playlist(auth_info.get('access_token'), start_date)
        extracted_playlist = convert_to_structured(featured_playlist, start_date)
        dumps.extend(extracted_playlist)
        print('Pulled for date: %s' % start_date)
        if iter % batch_size == 0:
            push_documents_to_db(dumps, mongo)
            print('Inserting into DB', '=' * 20)
            dumps = []
        start_date = start_date + delta
        iter += 1
