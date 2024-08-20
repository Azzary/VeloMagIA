# Montpellier Bike Predictor

This project predicts the number of available bikes in Montpellier, France, using a small machine learning model that can be executed directly in a web browser.

## Data Sources

- Bike station data: [Montpellier Open Data Portal](https://portail-api.montpellier3m.fr/#/)
- Weather data: [NOAA Global Summary of the Day](https://www.ncei.noaa.gov/access/search/data-search/global-summary-of-the-day)

## Features

The model uses the following features for prediction:

```
['is_weekend', 'is_holiday', 'is_school_vacation', 'day_of_week', 'temp', 'max_temp', 'min_temp', 'precipitation', 'wind_speed', 'visibility', 'fog', 'rain', 'snow', 'hail', 'thunder', 'tornado', 'hour', 'minute']
```

Note: Some features (e.g., tornado) may not be particularly relevant for Montpellier but are included for model completeness.

## Model Details

- Framework: PyTorch
- Web Implementation: ONNX Runtime for browser-based execution

## Project Structure

The `bike_predictor_web` directory contains the implementation of the web-based prediction interface.

## Model Performance

Based on 8000 test samples:

- Mean Absolute Error: 0.38
- Maximum Error: 3.58
  - Actual Value: 8.00
  - Predicted Value: 4.42
- Number of errors > 1: 428
- Number of errors ≤ 1: 7572
- Percentage of errors > 1: 5.35%

Sample predictions:
1. Actual: 5.00, Predicted: 4.83, Error: 0.17
2. Actual: 6.00, Predicted: 5.75, Error: 0.25
3. Actual: 6.00, Predicted: 5.68, Error: 0.32
4. Actual: 4.00, Predicted: 3.94, Error: 0.06
5. Actual: 6.00, Predicted: 5.64, Error: 0.36

## Usage

To test the model:

1. Install Flask:
   ```
   pip install flask
   ```

2. Run the web application:
   ```
   python bike_predictor_web/app.py
   ```

3. Open a web browser and navigate to `http://localhost:5000`

4. Use the following sample data to test the model:
   - Day: Tuesday (day_of_week: 2)
   - Is weekend: No
   - Is holiday: No
   - Is school vacation: Yes
   - Temperature: 22.5°C
   - Max Temperature: 27.4°C
   - Min Temperature: 18.5°C
   - Precipitation: 0.0 mm
   - Wind Speed: 7.9 m/s
   - Visibility: 11.9 km
   - Fog, Rain, Snow, Hail, Thunder, Tornado: No
   - Time: 10:15

With these inputs, the model should return a prediction close to 8 available bikes.