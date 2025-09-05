from httpx import Client, Timeout, ConnectError
from fake_useragent import UserAgent
from model import Scraper, ScraperResult

ua = UserAgent()


class ScraperService:
    def __init__(self, scraper: Scraper) -> None:
        self.chart_date = scraper.chart_date
        self.scrape_url = scraper.scrape_url
        self.timeout = Timeout(connect=30, pool=30, read=30, write=30)
        self.header = {"User-Agent": ua.random}

    def fetch_data(self) -> ScraperResult:
        self.scrape_url = f"{self.scrape_url}/{self.chart_date}"
        print("Scrapping started...")
        print(f"Scraping url: {self.scrape_url}")
        try:
            with Client(
                verify=True,
                follow_redirects=True,
                headers=self.header,
                timeout=self.timeout,
            ) as client:
                response = client.get(self.scrape_url)
                response.raise_for_status()
        except ConnectError as e:
            raise e
        else:
            if response.status_code == 200:
                print(f"scrapping succesful!..  status code: {response.status_code}")
                organized_content = ScraperResult(
                    chart_date=self.chart_date, html=response.text
                )
                return organized_content
            else:
                return ScraperResult(chart_date=self.chart_date, html="")
