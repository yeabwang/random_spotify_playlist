import json
import requests
import time
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from model import SpotifyClient, Scraper


class SpotifyClientService:
    def __init__(self, scraper: Scraper) -> None:
        self.sp = Spotify(
            auth_manager=SpotifyOAuth(
                client_id=SpotifyClient.client_id,
                client_secret=SpotifyClient.client_secret,
                redirect_uri=SpotifyClient.redirect_url,
                scope=SpotifyClient.scope,
            )
        )
        self.chart_date = scraper.chart_date
        self.fetched_musics = []
        self.track_ids = []
        self.user_id = self.sp.current_user().get("id", "")  # type: ignore
        self.playlist = None

    def load_music_title(self, music_path: str):
        try:
            with open(music_path, "r") as file:
                self.fetched_musics = json.load(file)
        except Exception as e:
            raise RuntimeError(f"Failed to load music titles: {e}")

    def safe_search(self, query, retries=3, delay=2):
        for attempt in range(retries):
            try:
                return self.sp.search(q=query, type="track", limit=1, market="US")
            except requests.exceptions.ChunkedEncodingError as e:
                print(f"ChunkedEncodingError: {e}. Retrying {attempt+1}/{retries}...")
                time.sleep(delay * (attempt + 1))
        return None

    def fetch_musics(self):
        for music_ in self.fetched_musics:
            track_title = music_.get("title")
            artist_name = music_.get("artist")

            if not track_title or not artist_name:
                continue

            query = f"track:{track_title} artist:{artist_name}"
            results = self.safe_search(query)

            if results.get("tracks", {}).get("items"):  # type: ignore
                track = results["tracks"]["items"][0]  # type: ignore
                track_id = track["id"]
                self.track_ids.append(track_id)
                print(
                    f"Found: {track['name']} by {', '.join(a['name'] for a in track['artists'])}"
                )
            else:
                print(f"Not found: {track_title} by {artist_name}")

    def create_playlist(self):
        self.playlist = self.sp.user_playlist_create(
            user=self.user_id,
            name=f"Billboard Hot 100 - {self.chart_date}",
            public=True,
            description=f"Playlist of the Hot 100 songs on {self.chart_date}",
        )

        playlist_url = self.playlist["external_urls"]["spotify"]  # type: ignore
        print("Playlist created:", playlist_url)

        for i in range(0, len(self.track_ids), 100):
            batch = self.track_ids[i : i + 100]
            self.sp.playlist_add_items(playlist_id=self.playlist["id"], items=batch)  # type: ignore

        print("All tracks added successfully!")
