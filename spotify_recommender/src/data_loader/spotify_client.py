def get_saved_tracks(sp): 
    results = sp.current_user_saved_tracks(offset=0, limit=50)
    return results['items']