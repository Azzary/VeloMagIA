import pandas as pd
from datetime import datetime
from weather_provider import WeatherProvider
from holiday_provider import HolidayProvider
from school_vacation_provider import SchoolVacationProvider

class DataEnricher:
    def __init__(self, weather_provider: WeatherProvider, holiday_provider: HolidayProvider, school_vacation_provider: SchoolVacationProvider):
        self.weather_provider = weather_provider
        self.holiday_provider = holiday_provider
        self.school_vacation_provider = school_vacation_provider

    def enrich_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df['weather_info'] = df['timestamp'].apply(lambda x: self.weather_provider.get_weather_info(x))
        df['is_weekend'] = df['timestamp'].dt.dayofweek.isin([5, 6])
        df['is_holiday'] = df['timestamp'].apply(lambda x: self.holiday_provider.is_holiday(x))
        df['is_school_vacation'] = df['timestamp'].apply(lambda x: self.school_vacation_provider.is_school_vacation(x))
        df['day_of_week'] = df['timestamp'].dt.dayofweek + 1  # 1 = Monday, 7 = Sunday

        # Extraire les informations météo dans des colonnes séparées
        weather_columns = ['temp', 'max_temp', 'min_temp', 'precipitation', 'wind_speed', 'visibility', 'fog', 'rain', 'snow', 'hail', 'thunder', 'tornado']
        for col in weather_columns:
            df[col] = df['weather_info'].apply(lambda x: x[col] if x else None)

        # Supprimer la colonne weather_info car nous avons extrait toutes les informations nécessaires
        df = df.drop(columns=['weather_info'])

        return df

# Exemple d'utilisation
if __name__ == "__main__":
    # Charger les données
    df = pd.read_csv('data/bike_data.csv', parse_dates=['timestamp'])

    # Initialiser les providers
    weather_provider = WeatherProvider()
    holiday_provider = HolidayProvider()
    school_vacation_provider = SchoolVacationProvider()

    # Créer et utiliser le DataEnricher
    enricher = DataEnricher(weather_provider, holiday_provider, school_vacation_provider)
    enriched_df = enricher.enrich_data(df)

    # Afficher les premières lignes du DataFrame enrichi
    print(enriched_df.head())

    # Sauvegarder les données enrichies
    enriched_df.to_csv('data/enriched_bike_data.csv', index=False)
    print("Données enrichies sauvegardées dans 'data/enriched_bike_data.csv'")