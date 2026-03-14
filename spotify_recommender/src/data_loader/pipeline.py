from .load_config import load_config
from .auth import build_spotify_client
from .spotify_client import get_saved_tracks
from  .transform import items_to_df 

def run(): 
    cfg = load_config()
    sp = build_spotify_client(**cfg)
    saved_tracks = get_saved_tracks(sp)
    df = items_to_df(saved_tracks)
    print(df)