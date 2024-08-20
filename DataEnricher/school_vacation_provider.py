import requests
from datetime import datetime, date
from typing import List, Tuple

class SchoolVacationProvider:
    def __init__(self):
        self.vacations: List[Tuple[date, date]] = []
        self.update_vacations()

    def update_vacations(self):
        url = "https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-en-calendrier-scolaire&q=&facet=description&facet=population&facet=start_date&facet=end_date&facet=zones&facet=annee_scolaire&refine.zones=Zone+C&refine.location=Montpellier"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            self.vacations = [
                (
                    datetime.fromisoformat(record['fields']['start_date']).date(),
                    datetime.fromisoformat(record['fields']['end_date']).date()
                )
                for record in data['records']
            ]
        except requests.RequestException as e:
            print(f"Erreur lors de la récupération des vacances scolaires: {e}")

    def is_school_vacation(self, date_to_check: datetime) -> bool:
        date_to_check = date_to_check.date()  # Convert to date object
        return any(start <= date_to_check <= end for start, end in self.vacations)

# Exemple d'utilisation
if __name__ == "__main__":
    provider = SchoolVacationProvider()
    today = date.today()
    is_vacation = provider.is_school_vacation(today)
    print(f"Aujourd'hui ({today}) est un jour de vacances scolaires: {is_vacation}")