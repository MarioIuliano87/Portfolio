import polars as pl 
import os

def items_to_df(items:list[dict]) -> pl.DataFrame:
    """ Imports tracks data and saves into parquet file. 
    Default path is "data/spotify_tracks.parquet"
    
    """
    rows = []
    for item in items: 
        row = {
        "track_added_at": item['added_at'],
        "track_name": item['track']['name'],
        "track_id": item['track']['id'],
        "track_uri": item['track']['uri'],
        "artist_name": item['track']['artists'][0]['name'],
        "artist_id": item['track']['artists'][0]['id'],
        "artist_uri": item['track']['artists'][0]['uri'],
        "album_name": item['track']['album']['name'],
        "album_id": item['track']['album']['id'],
        "album_uri": item['track']['album']['uri']
    }
        rows.append(row)
    rows_df = pl.from_dicts(rows)
    # create /data directory if it does not exist
    os.makedirs("spotify_recommender/data", exist_ok=True)
    rows_df.write_parquet("spotify_recommender/data/spotify_tracks.parquet")
    return rows_df