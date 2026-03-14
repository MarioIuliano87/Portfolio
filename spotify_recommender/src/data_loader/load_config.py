from dotenv import load_dotenv
import os 

def load_config() -> dict:
    """Load configuration from environment variables."""
    load_dotenv()
    return {
        "client_id": os.getenv("SPOTIPY_CLIENT_ID"),
        "redirect_uri": os.getenv("SPOTIPY_REDIRECT_URI"),
        "scope": os.getenv("SPOTIPY_SCOPE"),
    }
