# 🌱 Sproutify
Grow your network, one hidden curator at a time.
Sproutify finds underrated Spotify playlists featuring your favorite artists and quietly follows their creators—organically expanding your musical circle with authentic, low-follower connections.
# 🚀 Features
- Targets lesser-known playlists (configurable follower cap)
- Verifies artist presence before following
- Automatically follows playlist creators
- Built-in rate limiting and backoff handling
- Fully configurable behavior via `CONFIG`
# ⚙️ Setup
1. **Clone the repo**
```
git clone https://github.com/527598523495585527263662394398567754499/sproutify.git
cd sproutify
```
2. **Install dependencies**
```
pip install spotipy
```
3. **Configure credentials** Replace values in the `CONFIG` block of `sproutify.py`:
```
"client_id": "YOUR_CLIENT_ID",
"client_secret": "YOUR_CLIENT_SECRET",
"redirect_uri": "http://127.0.0.1:8000/callback"
```
3. Create a Spotify app here: [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
4. **Run the script**
```
python sproutify.py
```

# 🧠 How it works
Sproutify uses artist-related search terms to locate small public playlists, checks that your artist is actually in the tracklist, and follows the playlist’s creator—respecting rate limits and pacing requests to blend in naturally.
# ✨ Customization
Tweak any of the following options in `CONFIG`:
```
"artist_list": ["SZA", "Jhené Aiko", "Sonder"],         # Artists to search for
"pages": 5,                   # How deep to search per query
"max_followers": 5,           # Only follow users with fewer than this
"delay_range": (2.5, 6.0),    # Delay between requests
"shuffle_artists": True
```

# 🛡️ Disclaimer
Sproutify is intended for personal educational use only. Use responsibly and respect Spotify’s API terms.
