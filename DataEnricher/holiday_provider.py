import requests
from datetime import datetime
from typing import Set

class HolidayProvider:
    def __init__(self):
        self.holidays: Set[datetime] = set()
        self.update_holidays()

    def update_holidays(self):
        url = "https://calendrier.api.gouv.fr/jours-feries/metropole.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            self.holidays = set(datetime.fromisoformat(date).date() for date in data.keys())
        except requests.RequestException as e:
            print(f"Erreur lors de la récupération des jours fériés: {e}")

    def is_holiday(self, date: datetime) -> bool:
        return date.date() in self.holidays

# Exemple d'utilisation
if __name__ == "__main__":
    provider = HolidayProvider()
    is_holiday = provider.is_holiday(datetime.now())
    print(f"Aujourd'hui est un jour férié: {is_holiday}")