import pandas as pd
from datetime import datetime
from typing import Optional, Dict, List

class WeatherProvider:
    def __init__(self, data_file: str = './data/weather.csv'):
        self.data = self._load_data(data_file)

    def _load_data(self, data_file: str) -> pd.DataFrame:
        df = pd.read_csv(data_file, parse_dates=['DATE'])
        df['DATE'] = pd.to_datetime(df['DATE']).dt.date
        
        # Convertir les températures de Fahrenheit à Celsius
        for col in ['TEMP', 'MAX', 'MIN', 'DEWP']:
            df[col] = (df[col] - 32) * 5/9
        
        # Assurez-vous que FRSHTT est traité comme une chaîne
        df['FRSHTT'] = df['FRSHTT'].astype(str).str.zfill(6)
        
        return df.set_index('DATE')

    def get_weather_info(self, date: datetime) -> Optional[Dict[str, any]]:
        date = date.date()
        try:
            row = self.data.loc[date]
            weather_conditions = self._interpret_frshtt(row['FRSHTT'])
            
            return {
                'temp': round(row['TEMP'], 1),
                'max_temp': round(row['MAX'], 1),
                'min_temp': round(row['MIN'], 1),
                'precipitation': round(row['PRCP'] * 25.4, 1),  # Convert inches to mm
                'wind_speed': round(row['WDSP'] * 0.514444, 1),  # Convert knots to m/s
                'visibility': round(row['VISIB'] * 1.60934, 1),  # Convert miles to km
                'fog': weather_conditions['fog'],
                'rain': weather_conditions['rain'],
                'snow': weather_conditions['snow'],
                'hail': weather_conditions['hail'],
                'thunder': weather_conditions['thunder'],
                'tornado': weather_conditions['tornado']
            }
        except KeyError:
            print(f"Pas de données météo disponibles pour le {date}")
            return None

    def _interpret_frshtt(self, frshtt: str) -> Dict[str, int]:
        frshtt = str(frshtt).zfill(6)  # Assurez-vous que c'est une chaîne de 6 caractères
        return {
            'fog': int(frshtt[0]),  # 1 si brouillard ou nuageux, 0 sinon
            'rain': int(frshtt[1]),  # 1 si pluie ou bruine, 0 sinon
            'snow': int(frshtt[2]),  # 1 si neige ou grésil, 0 sinon
            'hail': int(frshtt[3]),  # 1 si grêle, 0 sinon
            'thunder': int(frshtt[4]),  # 1 si orage, 0 sinon
            'tornado': int(frshtt[5])  # 1 si tornade ou trombe, 0 sinon
        }

# Exemple d'utilisation
if __name__ == "__main__":
    provider = WeatherProvider()
    date = datetime(2023, 1, 1)
    weather_info = provider.get_weather_info(date)
    
    if weather_info:
        print(f"Conditions météo à Montpellier le {date.date()}:")
        print(f"Température moyenne: {weather_info['temp']}°C")
        print(f"Température maximale: {weather_info['max_temp']}°C")
        print(f"Température minimale: {weather_info['min_temp']}°C")
        print(f"Précipitations: {weather_info['precipitation']} mm")
        print(f"Vitesse du vent: {weather_info['wind_speed']} m/s")
        print(f"Visibilité: {weather_info['visibility']} km")
        print(f"Brouillard/Nuageux: {weather_info['fog']}")
        print(f"Pluie: {weather_info['rain']}")
        print(f"Neige: {weather_info['snow']}")
        print(f"Grêle: {weather_info['hail']}")
        print(f"Orage: {weather_info['thunder']}")
        print(f"Tornade: {weather_info['tornado']}")
    else:
        print("Données météo non disponibles pour cette date.")