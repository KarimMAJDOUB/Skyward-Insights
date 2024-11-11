import requests
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

def fetchFlightData(url, flight_type='arrivals'):
    """Fetches flight data arriving to or departing from Tunisia using the AirLabs API.

    Parameters:
        - flight_type (str): Type of flights to fetch ('arrivals' for incoming flights, 'departures' for outgoing flights).
        - url              : API URL
        
    Returns:
        - data (list): List of dictionaries containing information for each flight.
    """
    # Retrieve the API key from environment variables
    api_key = os.getenv('API_KEY')

    # Check if the API key is present
    if api_key is None:
        raise ValueError("API_KEY not found. Please ensure the .env file is present and contains the API_KEY")

    params = {
        'api_key': api_key,
        f"{'arr_iata' if flight_type == 'arrivals' else 'dep_iata'}" : 'TUN'
    }

    # Perform the API request
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'response' in data:
            return data['response']
        else:
            print('Error: Flight data not available')
            return[]
        
    except requests.exceptions.RequestException as e:
        print(f"API connection error: {e}")
        return []
