import requests
import json
from typing import Any, Dict, List
from datetime import datetime, timedelta
import time

class DataGetter:
    base_url: str

    def __init__(self, base_url: str = "https://portail-api-data.montpellier3m.fr/"):
        self.base_url = base_url

    def get_bike_station(self, limit: int = 1000) -> Dict[str, Any]:
        endpoint = f"{self.base_url}bikestation?limit={limit}"
        response = requests.get(endpoint)
        response.raise_for_status()
        data = response.json()
        self._save_data('data/data.json', data)
        return data

    def get_bike_station_timeseries(self, bike_station_id: str, from_date: str, to_date: str) -> Dict[str, Any]:
        endpoint = f"{self.base_url}bikestation_timeseries/{bike_station_id}/attrs/availableBikeNumber"
        params = {
            "fromDate": from_date,
            "toDate": to_date
        }
        response = requests.get(endpoint, params=params)
        
        if response.status_code == 404:
            print(f"Données non trouvées pour la période du {from_date} au {to_date}")
            return {"attrName": "availableBikeNumber", "entityId": bike_station_id, "index": [], "values": []}
        
        response.raise_for_status()
        return response.json()

    def get_bike_station_timeseries_over_period(self, bike_station_id: str, start_date: str, end_date: str, interval_days: int = 7) -> Dict[str, Any]:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        combined_data = {"attrName": "availableBikeNumber", "entityId": bike_station_id, "index": [], "values": []}

        while start < end:
            current_end = min(start + timedelta(days=interval_days), end)
            from_date = start.isoformat()
            to_date = current_end.isoformat()
            
            try:
                data = self.get_bike_station_timeseries(bike_station_id, from_date, to_date)
                if data["index"] and data["values"]:
                    combined_data["index"].extend(data["index"])
                    combined_data["values"].extend(data["values"])
                print(f"Données récupérées pour la période du {from_date} au {to_date}")
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    print(f"Limite de taux atteinte. Attente avant de réessayer...")
                    time.sleep(60)  # Attendre 60 secondes avant de réessayer
                    continue
                else:
                    print(f"Erreur lors de la récupération des données: {e}")
            
            start = current_end

        self._save_data(f'data/timeseries_{bike_station_id.replace(":", "")}.json', combined_data)
        return combined_data

    def _save_data(self, file_path: str, data: Dict[str, Any]) -> None:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

# Exemple d'utilisation
if __name__ == "__main__":
    data_getter = DataGetter()
    
    bike_station_id = "urn:ngsi-ld:station:001"
    
    end_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    start_date = (datetime.now() - timedelta(days=360)).strftime("%Y-%m-%dT%H:%M:%S")
    
    print(f"Récupération des données du {start_date} au {end_date}")
    timeseries_data = data_getter.get_bike_station_timeseries_over_period(bike_station_id, start_date, end_date, interval_days=90)
    print(f"Données récupérées : {len(timeseries_data['index'])} points")