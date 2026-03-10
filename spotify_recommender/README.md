# Spotify “On-the-Go” Next Song Recommender (MVP)

## What it does
A Streamlit app that generates **real-time “next song” recommendations** based on the track you’re listening to right now (or a track you type in). It builds an **adaptive playlist on the fly** and re-ranks recommendations when you **skip** tracks or **listen through** (e.g., ≥80% completion).

---

## Problem it solves
When you’re in a listening flow, you don’t want to curate playlists manually. You want the next track to:
- match the current vibe (energy / tempo / loudness / etc.),
- stay inside *your* taste space (your liked songs & playlists),
- adapt quickly if you skip.

**Outcome:** auto-generated playlists “on the go” that improve from implicit feedback.

---

## MVP Scope
### Inputs
- **Mode A (Search):** user types a song title
- **Mode B (Now Playing):** app reads the current Spotify track

### Outputs
- Top 10 ranked next-track recommendations (with similarity score)
- “Session playlist” list that evolves as you listen/skip

### Core signal
Spotify **audio features** as track vectors:
`danceability, energy, valence, tempo, loudness, acousticness, instrumentalness, liveness, speechiness`

---

## Feasibility & Constraints (important for portfolio credibility)

### ✅ Streamlit “type a song → recommendations”
Feasible. You can resolve a title to a track via Search, then fetch audio features, then do similarity search in your local corpus.

### ✅ “Now playing” integration
Feasible. Spotify provides an endpoint to read the **currently playing track** for the user.  [oai_citation:0‡Spotify for Developers](https://developer.spotify.com/documentation/web-api/reference/get-the-users-currently-playing-track?utm_source=chatgpt.com)  
Requires user authorization scopes such as `user-read-currently-playing` and/or `user-read-playback-state`.  [oai_citation:1‡Spotify for Developers](https://developer.spotify.com/documentation/web-api/concepts/scopes?utm_source=chatgpt.com)

### ✅ Detect skipping + re-rank with “listen ≥80%” rule
Feasible, but done via **polling**, not events/webhooks.
Spotify does not push skip events to your app; instead, you periodically call the “currently playing” endpoint and infer:
- **skip:** track changes before completion threshold
- **good listen:** `progress_ms / duration_ms >= 0.80` (computed client-side)

### ⚠️ Rate limits
Spotify enforces Web API rate limits. If you hit them you’ll receive HTTP 429 responses, and you should back off accordingly.  [oai_citation:2‡Spotify for Developers](https://developer.spotify.com/documentation/web-api/concepts/rate-limits?utm_source=chatgpt.com)  
For the MVP, polling every ~5–10 seconds is typically enough to detect track changes without being aggressive.

### ⚠️ “Running in Spotify” vs “controlling Spotify”
- Reading playback state (what’s playing) is doable (above).
- Controlling playback (e.g., “skip next”, “add to queue”) is also possible via Player APIs, **but some endpoints only work for Spotify Premium** users (e.g., “Skip To Next”).  [oai_citation:3‡Spotify for Developers](https://developer.spotify.com/documentation/web-api/reference/skip-users-playback-to-next-track?utm_source=chatgpt.com)  
For a portfolio MVP, you can keep it as **read-only + recommend** and optionally add playback control later behind a “Premium required” note.

### ✅ Overall feasibility verdict
**Yes, this is a strong and realistic portfolio project.**
It demonstrates:
- API integration + OAuth scopes
- building a personal dataset
- vector similarity retrieval
- online adaptation from implicit feedback
- product thinking (constraints, fallbacks, explainability)

---

## System Design (MVP)

### Data layer (local corpus)
Build a local store from:
- Liked songs (`/me/tracks`)
- User playlists + playlist tracks

For each track store:
- Track metadata: id, name, artists, album, release_date, duration_ms, popularity
- Audio features: the vector fields above

### Retrieval
1. Get query track (typed OR currently playing).
2. Fetch its audio features vector `v`.
3. Retrieve candidates from local corpus (optionally filter out same artist / recent history).
4. Rank by similarity (cosine) on standardized features.
5. Return Top 10.

### Adaptive session (“on-the-go playlist”)
Maintain a session vector `S`.

- Initialize: `S = v(track_1)`
- If user listens ≥80%: update towards the track:
  - `S = 0.7*S + 0.3*v(track_k)`
- If user skips early: update weakly or apply penalties:
  - `S = 0.95*S + 0.05*v(track_k)` (or keep S unchanged + blacklist neighborhood)

Then recommend from `S` rather than only the current track.

---

## Step-by-step project plan

### Phase 0 — Setup (1–2 hours)
1. Create Spotify Developer App (Client ID, Redirect URI).
2. Implement OAuth Authorization Code flow (scopes below).
3. Create a `.env` and ensure secrets are not committed.

**Scopes to request (MVP)**
- Read playback: `user-read-currently-playing`, `user-read-playback-state`  [oai_citation:4‡Spotify for Developers](https://developer.spotify.com/documentation/web-api/concepts/scopes?utm_source=chatgpt.com)
- Read library: `user-library-read`
- Read playlists: `playlist-read-private`, `playlist-read-collaborative`

### Phase 1 — Data ingestion (half day)
4. Download your liked songs + playlists track lists.
5. Batch-fetch audio features for all track IDs.
6. Store locally (SQLite or Parquet).

Deliverable: `data/tracks.parquet` (or `spotify.db`)

### Phase 2 — Retrieval baseline (half day)
7. Feature preprocessing:
   - handle missing values
   - standardize numeric features
8. Implement similarity search:
   - cosine similarity
   - filters: exclude current track, optionally exclude same artist
9. Write unit tests for:
   - vector shapes
   - ranking stability
   - filters

Deliverable: `src/recommend.py`

### Phase 3 — Streamlit app (half day)
10. Build Streamlit UI with two modes:
   - “Search by title”
   - “Now Playing”
11. Display Top 10 recommendations with:
   - song + artist
   - similarity score
   - optionally “feature match” explanation (top contributing dimensions)

Deliverable: `app.py`

### Phase 4 — Adaptive behavior (1 day)
12. Implement polling loop:
   - call currently-playing endpoint every ~5–10 seconds
   - track changes → infer skip vs completion
13. Implement session vector update rules
14. Re-rank recommendations after each inferred event
15. Add simple “history” state (avoid repeats)

Deliverable: adaptive playlist behavior + “session timeline” debug panel

### Phase 5 — Portfolio polish (half day)
16. Write a short “Product & Engineering” section in README:
   - assumptions & constraints
   - rate limits/backoff strategy  [oai_citation:5‡Spotify for Developers](https://developer.spotify.com/documentation/web-api/concepts/rate-limits?utm_source=chatgpt.com)
   - Premium-only playback control note  [oai_citation:6‡Spotify for Developers](https://developer.spotify.com/documentation/web-api/reference/skip-users-playback-to-next-track?utm_source=chatgpt.com)
17. Add screenshots / demo GIF
18. Add “How to run” + “Troubleshooting” (OAuth redirect, scopes, no device active, etc.)

---

## Stretch ideas (optional)
- Diversity constraint (avoid too-similar sequence)
- Hybrid score: audio similarity + artist-genre similarity
- Add-to-queue button (with Premium note)
- Export session playlist to a new Spotify playlist

---

## Repo structure suggestion
- `app.py` (Streamlit)
- `src/spotify_client.py` (API wrapper + OAuth)
- `src/data_ingest.py` (download + persist)
- `src/recommend.py` (vector prep + retrieval + session logic)
- `data/` (local store; gitignored)
- `tests/`
- `.env.example`