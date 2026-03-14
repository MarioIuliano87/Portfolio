# 🎧 Instant Seed → Creative Playlist  
## MVP Specification

---

## 1. Overview

This project builds a **session-aware music recommender** that:

1. Takes a single seed track  
2. Instantly generates a Top 10 playlist  
3. Maintains high similarity for the first few tracks (exploit phase)  
4. Gradually injects controlled creativity (explore phase)  
5. Adapts based on implicit feedback (skip vs listen-through)

The goal is to demonstrate:
- Vector-based retrieval
- Exploration vs exploitation
- Session modeling
- Clean product thinking
- Reproducible architecture

---

## 2. Problem It Solves

When starting from one song, users want:

- Immediate continuation of the vibe  
- Gradual variation to avoid boredom  
- Smooth listening flow  
- Adaptation when they skip  

This system creates playlists **on the fly**, balancing coherence and novelty.

---

## 3. Track Representation

Each track is represented as a numeric vector using Spotify audio features:

    V = [
      danceability,
      energy,
      valence,
      tempo,
      loudness,
      acousticness,
      instrumentalness,
      liveness,
      speechiness
    ]

Before similarity comparison, features are standardized using z-score normalization.

---

## 4. Similarity Function

Cosine similarity is used:

    sim(u, v) = (u · v) / (||u|| * ||v||)

---

## 5. Session Vector

We maintain a session vector `S`.

### Initialization

    S = vector(seed_track)

### Update Rule

If listened ≥ 80%:

    S = 0.7 * S + 0.3 * v_track

If skipped early (< 20%):

    S = 0.95 * S + 0.05 * v_track

Otherwise:

    S remains unchanged

---

## 6. Exploit Phase (First 5 Tracks)

- Rank candidates by cosine similarity to `S`
- Exclude:
  - Current track
  - Optionally same artist
  - Recently played tracks

Scoring:

    score_exploit = sim(S, v_track)

Return Top 10.

---

## 7. Explore Phase (Controlled Creativity)

After 5 tracks, inject novelty.

### Method A — Distance Band

Compute Euclidean distance:

    d = ||v_track - S||

Select tracks whose distance lies between:

- 70th percentile  
- 85th percentile  

Rank with hybrid score:

    score_creative = 0.5 * sim(S, v) + 0.5 * novelty(v)

Where novelty penalizes:
- Same artist
- Same cluster
- Recently played

---

### Method B — Temperature Sampling

Convert similarities into probabilities:

    p_i ∝ exp(sim(S, v_i) / T)

- Small T (0.1) → exploit  
- Larger T (0.7) → explore  

After track 5, increase T.

---

## 8. Creativity Schedule (MVP Defaults)

    seed_batch_size = 10
    creativity_start_after = 5
    exploit_count = 8
    creative_count = 2

Behavior:
- First 5 tracks → 100% exploit
- After → 80% exploit, 20% creative

---

## 9. Data Modes

### Demo Mode (No Login Required)

- Uses bundled dataset (2–5k tracks)
- Fully reproducible
- Works offline

### Personal Mode (Spotify OAuth)

Required scopes:
- user-library-read
- playlist-read-private
- playlist-read-collaborative
- user-read-currently-playing
- user-read-playback-state

Premium is NOT required unless controlling playback.

---

## 10. Optional API Layer

### POST /playlist/generate

Request:

    {
      "seed_track_id": "...",
      "top_k": 10,
      "exclude_same_artist": true,
      "creativity_start_after": 5,
      "creative_ratio": 0.2
    }

Response:

    {
      "playlist": [
        {"track_id": "...", "score": 0.93, "type": "exploit"},
        {"track_id": "...", "score": 0.88, "type": "exploit"},
        {"track_id": "...", "score": 0.41, "type": "creative"}
      ]
    }

---

## 11. Streamlit Demo Plan

Left panel:
- Seed track search
- Toggle: Demo mode / Personal mode
- Toggle: Creativity level
- Button: Generate playlist

Right panel:
- Top 10 list with exploit/creative labels
- 2D visualization (UMAP)
  - Blue = exploit
  - Orange = creative
  - Black = seed

Simulation buttons:
- Mark as listened (≥80%)
- Skip (<20%)

---

## 12. 2D Visualization (Optional)

Use UMAP:

    X_2D = UMAP(n_components=2).fit_transform(X_standardized)

This visually demonstrates:
- Coherent cluster formation
- Creative picks being farther but not random

---

## 13. Evaluation Metrics

- Mean cosine similarity of playlist
- Average creative distance
- Simulated skip rate
- Artist diversity (entropy)

---

## 14. Tech Stack

- Python 3.10+
- numpy
- pandas
- scikit-learn
- umap-learn
- spotipy
- streamlit
- optional: fastapi

---

## 15. Portfolio Value

This project demonstrates:

- Vector retrieval
- Session-aware reranking
- Controlled exploration
- Adaptive feedback loop
- Reproducible demo mode
- Product-oriented ML thinking

---

## 16. Summary

This MVP:

- Starts from one track  
- Builds an immediate coherent playlist  
- Gradually injects novelty  
- Adapts to user behavior  
- Is reproducible without login  
- Can scale to personal real-time sessions  

It is simple, explainable, and strong as a portfolio data product.

---

## 17. Workflow Diagram

The workflow is easiest to read in three connected layers:
- State: seed track, feature vector, session vector, candidate pool
- Ranking: score candidates, split into exploit and explore paths, build the next queue
- Feedback: listen/skip behavior updates the next session vector

```text
  [Seed Track]
       |
       v
  [Extract / Load Audio Feature Vector]
       |
       v
  [Initialize Session Vector S]
       |
       v
  [Retrieve Candidate Tracks]
       |
       v
  [Score Candidates vs Session Vector]
       |
       +-----------------------------+
       |                             |
       v                             v
  [Exploit Path]                [Explore Path]
  High similarity to S          Creative selection
  Nearest neighbors             Distance band or temperature
       |                             |
       +-------------+---------------+
                     |
                     v
          [Build Next Queue / Playlist]
                     |
                     v
            [User listens or skips]
                     |
                     v
          [Update Session Vector S]
                     |
                     v
              [Repeat next cycle]

```
  ## Session Update Logic
```
  [User listens or skips]
           |
           v
  [Did user listen >= 80%?] ---- yes ----> [Strong update: S = 0.7S + 0.3v]
           |
           no
           v
  [Did user skip < 20%?] ------ yes ----> [Weak update: S = 0.95S + 0.05v]
           |
           no
           v
                 [No update]
```
  ## Explore Logic
```
  [Explore Path]
       |
       +--> [Method A: Distance Band]
       |     Select tracks with distance from S in P70-P85
       |
       +--> [Method B: Temperature Sampling]
             Sample from similarity distribution with higher T
