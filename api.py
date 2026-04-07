from flask import Flask, request, jsonify
from datetime import timedelta
from dateutil.parser import isoparse
import openmeteo_requests
import requests_cache
import numpy as np
import pandas as pd
from retry_requests import retry
from scipy.stats import gamma, norm
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Setup Open-Meteo API client with caching and retry
cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("filecredentials.json")
firebase_admin.initialize_app(cred)

# Get Firestore database instance
db = firestore.client()

# Define the Open-Meteo API URL
API_URL = "https://archive-api.open-meteo.com/v1/archive"

# Function to categorize the RAI value
def categorize_rai(rai_value):
    if rai_value >= 4.00:
        return "Extremely rainy"
    elif 3.00 <= rai_value < 4.00:
        return "Highly rainy"
    elif 2.00 <= rai_value < 3.00:
        return "Moderately rainy"
    elif 0.50 <= rai_value < 2.00:
        return "Low rainfall"
    elif -0.49 <= rai_value < 0.50:
        return "Normal"
    elif -1.99 <= rai_value < -0.50:
        return "Slight reduction in rainfall"
    elif -2.99 <= rai_value < -2.00:
        return "Moderate reduction in rainfall"
    elif -3.99 <= rai_value < -3.00:
        return "Large reduction in rainfall"
    elif rai_value <= -4.00:
        return "Extreme reduction in rainfall"

# Function to categorize the SPI value
def categorize_spi(spi):
    if spi <= -2.0:
        return "Extremely Dry"
    elif -2.0 < spi <= -1.5:
        return "Severely Dry"
    elif -1.5 < spi <= -1.0:
        return "Moderately Dry"
    elif -1.0 < spi <= 1.0:
        return "Near Normal"
    elif 1.0 < spi <= 1.5:
        return "Moderately Wet"
    elif 1.5 < spi <= 2.0:
        return "Severely Wet"
    else:
        return "Extremely Wet"
    
# Function to send RAI and SPI data to Firebase
def send_rai_spi_to_firebase(user_id, farm_id, rai_value, rai_category, spi_value, spi_category):
    try:
        # Reference Firestore collection and document
        doc_ref = db.collection("users").document(user_id).collection("farms").document(farm_id)

        # Data to be sent
        rai_spi_data = {
            "RAI": {
                "value": float(rai_value.item()),  # Convert NumPy float to Python float
                "category": rai_category
            },
            "SPI": {
                "value": float(spi_value.item()),  # Convert NumPy float to Python float
                "category": spi_category
            },
            "timestamp": firestore.SERVER_TIMESTAMP  # Add timestamp
        }

        # Update or set the document with RAI and SPI data
        doc_ref.update({"weather_analysis": rai_spi_data})

        print("RAI and SPI data successfully sent to Firebase.")
    except Exception as e:
        print(f"Error sending data to Firebase: {str(e)}")
        

@app.route('/', methods=['POST'])
def calculate_historical_data():
    try:
        # Retrieve data from the request
        data = request.json
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        event_start_date_str = data.get("eventStartDate")
        event_end_date_str = data.get("eventEndDate")
        user_id = data.get("userId")  # User ID from request
        farm_id = data.get("farmId")  # Farm ID from request


        if not (latitude and longitude and event_start_date_str and event_end_date_str):
            return jsonify({"error": "Missing required fields: latitude, longitude, eventStartDate, eventEndDate"}), 400

        # Parse dates
        event_start_date = isoparse(event_start_date_str).date()
        event_end_date = isoparse(event_end_date_str).date()

        # Calculate historical date range
        historical_start_date = event_start_date - timedelta(days=365 * 10)
        historical_end_date = event_start_date - timedelta(days=1)

        # Fetch recent weather data
        recent_weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": event_start_date.strftime("%Y-%m-%d"),
            "end_date": event_end_date.strftime("%Y-%m-%d"),
            "daily": "precipitation_sum"
        }
        recent_weather_response = openmeteo.weather_api(API_URL, params=recent_weather_params)

        # Fetch historical weather data
        historical_weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": historical_start_date.strftime("%Y-%m-%d"),
            "end_date": historical_end_date.strftime("%Y-%m-%d"),
            "daily": "precipitation_sum"
        }
        historical_weather_response = openmeteo.weather_api(API_URL, params=historical_weather_params)

        # Process recent weather data
        recent_data = recent_weather_response[0].Daily()
        recent_precipitation = np.array(recent_data.Variables(0).ValuesAsNumpy())
        recent_total_precipitation = np.sum(recent_precipitation)

        # Process historical weather data
        historical_data = historical_weather_response[0].Daily()
        historical_precipitation = np.array(historical_data.Variables(0).ValuesAsNumpy())

        # Calculate RAI
        historical_mean = np.mean(historical_precipitation)
        historical_std = np.std(historical_precipitation)
        rai_value = (recent_total_precipitation - historical_mean) / historical_std
        rai_category = categorize_rai(rai_value)

        # Calculate SPI
        # Step 1: Fit Gamma distribution to historical data
        shape, loc, scale = gamma.fit(historical_precipitation)

        # Step 2: Calculate cumulative probability for recent total precipitation
        cumulative_prob = gamma.cdf(recent_total_precipitation, shape, loc, scale)

        # Step 3: Transform cumulative probability into standard normal distribution
        spi_value = norm.ppf(cumulative_prob)
        spi_category = categorize_spi(spi_value)
        
         # Send data to Firebase
        send_rai_spi_to_firebase(user_id, farm_id, rai_value, rai_category, spi_value, spi_category)

        # Prepare response data
        response_data = {
            "latitude": latitude,
            "longitude": longitude,
            "recentWeather": {
                "start_date": recent_weather_params["start_date"],
                "end_date": recent_weather_params["end_date"],
                "precipitation_sum": recent_precipitation.tolist(),  # Convert to list
                "total_precipitation": float(recent_total_precipitation.item())  # Convert to Python float
            },
            "historicalWeather": {
            "start_date": historical_weather_params["start_date"],
            "end_date": historical_weather_params["end_date"],
            "precipitation_sum": historical_precipitation.tolist()  # Convert to list
            },
            "RAI": {
                "value": float(rai_value.item()),  # Convert to Python float
                "category": rai_category
            },
            "SPI": {
                "value": float(spi_value.item()),  # Convert to Python float
                "category": spi_category
            }
        }
        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
