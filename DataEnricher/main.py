import pandas as pd
from weather_provider import WeatherProvider
from holiday_provider import HolidayProvider
from school_vacation_provider import SchoolVacationProvider
from data_enricher import DataEnricher

def main():
    # Charger les données
    df = pd.read_csv('data/bike_data.csv', parse_dates=['timestamp'])

    # Initialiser les providers
    weather_provider = WeatherProvider()
    holiday_provider = HolidayProvider()
    school_vacation_provider = SchoolVacationProvider()

    # Créer et utiliser le DataEnricher
    enricher = DataEnricher(weather_provider, holiday_provider, school_vacation_provider)
    enriched_df = enricher.enrich_data(df)

    # Sauvegarder les données enrichies
    enriched_df.to_csv('data/enriched_bike_data.csv', index=False)
    print(enriched_df.head())

if __name__ == "__main__":
    main()