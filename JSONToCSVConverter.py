import json
import csv
from typing import List, Dict, Any
import pandas as pd
from datetime import datetime

class JSONToCSVConverter:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file

    def load_json(self) -> Dict[str, Any]:
        with open(self.input_file, 'r') as file:
            return json.load(file)

    def convert_to_csv(self, additional_columns: List[str] = None) -> None:
        data = self.load_json()
        
        df = pd.DataFrame({
            'timestamp': [datetime.fromisoformat(ts.replace('Z', '+00:00')) for ts in data['index']],
            'numberBike': [value for value in data['values']]
        })

        df.sort_values('timestamp', inplace=True)

        df.to_csv(self.output_file, index=False)
        print(f"Fichier CSV sauvegardé : {self.output_file}")

    @staticmethod
    def read_csv_with_pandas(file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path, parse_dates=['timestamp'])

if __name__ == "__main__":
    input_file = 'data/timeseries_urnngsi-ldstation001.json'
    output_file = 'data/bike_data.csv'
    
    converter = JSONToCSVConverter(input_file, output_file)
    converter.convert_to_csv(additional_columns=['availableStands'])

    df = JSONToCSVConverter.read_csv_with_pandas(output_file)
    print(df.head())