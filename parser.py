from bs4 import BeautifulSoup
from model import ScraperResult, MusicEntry
from dataclasses import asdict
from typing import List
import json


class MusicParser:

    def __init__(self) -> None:
        self.fetched_conetnt = ""
        self.chart_date = ""
        self.all_musics = []
        self.parsed_counter = 0
        self.file_name = ""

    def parse_content(self, raw_content: ScraperResult) -> List[MusicEntry]:
        self.chart_date = raw_content.chart_date
        self.fetched_conetnt = raw_content.html

        print(" Parsing started...")
        if len(self.fetched_conetnt) > 0:
            soup = BeautifulSoup(self.fetched_conetnt, "lxml")
            music_card = soup.select(selector="div.o-chart-results-list-row-container")

            for music in music_card:
                self.parsed_counter += 1
                music_title = music.select_one("li h3")
                artist_name = music.select_one("li span > a")
                music_rank = music.select_one(" div li span")

                if music_title and artist_name and music_rank:

                    single_music = MusicEntry(
                        title=music_title.text.strip(),
                        artist=artist_name.text.strip(),
                        rank=music_rank.text.strip(),
                    )

                    self.all_musics.append(single_music)
            else:
                print("Parsing Successful!")
                print(f"Total Parsed musics: {self.parsed_counter}")
                return self.all_musics
        else:
            print("Parsing Failed!")
            return self.all_musics

    def write_parsed_content(self):
        self.file_name = f"music_data/{self.chart_date}.json"
        try:
            with open(file=self.file_name, mode="w", encoding="utf-8") as file:
                json.dump(
                    [asdict(music) for music in self.all_musics],
                    file,
                    indent=4,
                    ensure_ascii=False,
                )
        except Exception as e:
            raise e
