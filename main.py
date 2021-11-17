from data_feed import runner
from datetime import datetime

if __name__ == '__main__':
    runner(
        spotify_credentials_path='credentials/spotify_creds.json',
        db_credentials_path='credentials/db_creds.json',
        start_date=datetime(2020, 1, 1),
        stop_date=datetime(2021, 1, 1),
    )
