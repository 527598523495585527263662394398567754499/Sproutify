import time, random, spotipy, sys  # type: ignore
from spotipy.oauth2 import SpotifyOAuth  # type: ignore
from spotipy.exceptions import SpotifyException  # type: ignore

CONFIG = {
    "client_id": 'YOUR_SPOTIFY_CLIENT_ID',
    "client_secret": 'YOUR_SPOTIFY_CLIENT_SECRET',
    "redirect_uri": 'YOUR_REDIRECT_URI',
    "scope": 'user-follow-modify playlist-read-private',
    "artist_list": ["SZA", "Jhené Aiko", "Sonder"],
    "pages": 5, "page_size": 50, "max_followers": 5,
    "delay_range": (2.5, 6.0),
    "max_retries": 3,
    "rate_limit_threshold": 3,
    "shuffle_artists": True,
    "print_summary": True
}

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CONFIG["client_id"],
    client_secret=CONFIG["client_secret"],
    redirect_uri=CONFIG["redirect_uri"],
    scope=CONFIG["scope"]
))

rate_limit_hits = 0  # 🧠 Global tracker

def safe_call(func, *args, **kwargs):
    global rate_limit_hits
    for _ in range(CONFIG["max_retries"]):
        try:
            result = func(*args, **kwargs)
            time.sleep(random.uniform(0.5, 1.2))  # brief recovery pause
            return result
        except SpotifyException as e:
            if e.http_status == 429:
                rate_limit_hits += 1
                wait = int(e.headers.get("Retry-After", 5))
                print(f"⏳ Rate limited. Waiting {wait}s...")
                time.sleep(wait + 1)
                if rate_limit_hits >= CONFIG["rate_limit_threshold"]:
                    print("🛑 Too many rate limits. Backing off for 5 minutes...")
                    time.sleep(300)
                    rate_limit_hits = 0
            else:
                print(f"⚠️ SpotifyException {e.http_status}: {e.msg}")
                break
        except Exception as ex:
            print(f"⚠️ Unexpected error: {ex}")
            break
    return None

def generate_queries(artist):
    return [f"{artist}{s}" for s in ("", " playlist", " best of", " fan mix", " + chill", " + indie", " + sad", " + driving", " + late night")]

def find_and_follow_smaller_playlists(cfg):
    followed = set()
    artists = cfg["artist_list"]
    if cfg["shuffle_artists"]: random.shuffle(artists)

    for artist in artists:
        query = random.choice(generate_queries(artist))
        print(f"\n🎧 {artist} → '{query}'")
        for page in range(cfg["pages"]):
            print(f"  → Page {page+1}/{cfg['pages']}")
            time.sleep(random.uniform(*cfg["delay_range"]))  # slow before each page
            res = safe_call(sp.search, q=query, type='playlist', limit=cfg["page_size"], offset=page * cfg["page_size"])
            if not res: continue
            for pl in res.get('playlists', {}).get('items', []):
                pid, uid = pl.get('id'), pl.get('owner', {}).get('id')
                if not pid or not uid or uid in followed: continue
                time.sleep(random.uniform(1.5, 3.0))  # pace deep lookups
                pdata = safe_call(sp.playlist, pid)
                items = safe_call(sp.playlist_items, pid, limit=100)
                if not pdata or not items: continue
                if pdata.get('followers', {}).get('total', 0) > cfg["max_followers"]: continue
                tracks = items.get('items', [])
                if any(artist.lower() in a.get('name', '').lower()
                       for i in tracks if (t := i.get('track')) for a in t.get('artists', [])):
                    profile = safe_call(sp.user, uid)
                    if not profile: continue
                    name = profile.get("display_name", uid)
                    safe_call(sp.user_follow_users, [uid])
                    followed.add(uid)
                    print(f"✅ Followed: {name} | Followers: {pdata['followers']['total']} | Artist: {artist}")
            time.sleep(random.uniform(*cfg["delay_range"]))
    if cfg["print_summary"]: print(f"\n🎯 Total followed: {len(followed)}")

try:
    find_and_follow_smaller_playlists(CONFIG)
except Exception as e:
    print(f"\n💥 Script crashed: {e}")
    if getattr(sys, 'frozen', False): input("\nPress Enter to close...")
