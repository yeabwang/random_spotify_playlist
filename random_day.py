import random
from datetime import datetime, timedelta


class GetRandomDate:

    def random_billboard_date(self):
        start_date = datetime(1958, 8, 4)
        end_date = datetime.today()

        delta = end_date - start_date
        random_days = random.randint(0, delta.days)

        random_date = start_date + timedelta(days=random_days)

        return random_date.strftime("%Y-%m-%d")
