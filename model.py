from dataclasses import dataclass
from typing import NamedTuple
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass
class Scraper:
    chart_date: str
    scrape_url: str = os.getenv("FETCH_URL", "")


@dataclass
class ScraperResult:
    chart_date: str
    html: str


@dataclass
class MusicEntry:
    title: str
    artist: str
    rank: str


@dataclass
class SpotifyClient:
    client_id: str = os.getenv("SPOTIPY_CLIENT_ID", "")
    client_secret: str = os.getenv("SPOTIPY_CLIENT_SECRET", "")
    redirect_url: str = os.getenv("SPOTIPY_REDIRECT_URI", "")
    scope: str = "playlist-modify-private playlist-modify-public"
