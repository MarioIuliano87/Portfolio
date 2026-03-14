import spotipy
from spotipy.oauth2 import SpotifyPKCE

def build_spotify_client(
        client_id: str, 
        redirect_uri: str, 
        scope: str
) -> spotipy.Spotify:
    return spotipy.Spotify(
        auth_manager=SpotifyPKCE(
            client_id=client_id,
            redirect_uri=redirect_uri,
            scope=scope,
            open_browser=True,
        )
    )