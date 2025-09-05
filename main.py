from pathlib import Path
from model import Scraper
from spotify_client import SpotifyClientService
from scraper import ScraperService
from parser import MusicParser
from random_day import GetRandomDate


def main() -> None:
    while True:

        chart_date = GetRandomDate().random_billboard_date()
        file_path = Path("music_data") / f"{chart_date}.json"

        if file_path.exists():
            print(f"Playlist data already exists: {file_path}")
        else:
            print("Proceed with scrape + playlist creation...")
            break

    try:
        scraper = Scraper(chart_date)
        scraper_service = ScraperService(scraper=scraper)
        fetched_content = scraper_service.fetch_data()

        music_parser = MusicParser()
        music_parser.parse_content(fetched_content)
        music_parser.write_parsed_content()

    except Exception as e:
        print(f"Error Occured.{e}")
        raise
    else:
        print("Scrapping successful. Please check the results in music_data folder.")

    try:
        spotify_client_service = SpotifyClientService(scraper=scraper)
        spotify_client_service.load_music_title(music_path=music_parser.file_name)
        spotify_client_service.fetch_musics()
        spotify_client_service.create_playlist()

    except Exception as e:
        print(f"Error Occured {e}")
        raise

    else:
        print("Playlist created successfully!")


if __name__ == "__main__":
    main()
