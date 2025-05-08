#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
##############################################################################
This module is designed to fetch flight data from the AviationStack API, 
validate the structure of the received data, and save it to a JSON file.
##############################################################################
"""
import requests
import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

log_file = 'flight_data_fetch.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

def ingestFlightData(url, flight_type='arrivals'):
    """Fetch flight data from the API, ensuring API_KEY is not exposed.
    
    Parameters:
        url (str): The API endpoint to fetch data from.
        flight_type (str): The type of flights to fetch, either 'arrivals' or 'departures'. Defaults to 'arrivals'.
    
    Returns:
        list: A list containing the flight data retrieved from the API, or an empty list if an error occurs.
    """
    api_key = os.getenv('m_API_KEY')
    if not api_key:
        logger.error("API_KEY not found. Please ensure the .env file is present and contains the API_KEY")
        raise ValueError("API_KEY not found. Please ensure the .env file is present and contains the API_KEY")
    
    tunisian_airports = ["TUN", "MIR", "NBE", "DJE", "TOE", "GAE", "GAF", "SFA", "TBJ", "EBM"]
    all_flight_data = []

    for airport in tunisian_airports:
        params = {
            'access_key': api_key,
            f"{'arr_iata' if flight_type == 'arrivals' else 'dep_iata'}": airport 
        }

        try:
            logger.info(f"Fetching {flight_type} flight data for {airport} from {url}...")
            response = requests.get(url, params=params)
            response.raise_for_status()  
            data = response.json()
            if isinstance(data, dict) and data.get('data'): 
                logger.info(f"SUCCESS - Successfully fetched {flight_type} flight data for {airport}.")
                all_flight_data.extend(data['data'])
            else:
                logger.critical(f"FAILED - No valid flight data found in the response for {airport}.")
        
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while accessing {url} for {airport}: {http_err}")
        
        except requests.exceptions.ConnectionError as conn_err:
            logger.error(f"Connection error occurred for {airport}: {conn_err}")
        
        except requests.exceptions.Timeout as timeout_err:
            logger.error(f"Request timed out for {airport}: {timeout_err}")
        
        except requests.exceptions.RequestException as req_err:
            logger.error(f"API connection error for {airport}: {req_err}")
        
        except Exception as e:
            logger.critical(f"Unexpected error occurred for {airport}: {e}")

    return all_flight_data

def validateData(data):
    """Validate if the fetched data is a list of dictionaries.
    
    Parameters:
        data (any): The data to validate.
    
    Returns:
        bool: True if data is a list of dictionaries, False otherwise.
    """
    if isinstance(data, list):
        return all(isinstance(item, dict) for item in data)
    return False

def saveFlights(flight_data):
    """
    Save the flight data to a JSON file in the 'raw_data' directory under the 'data' folder.

    The filename will be dynamically generated using the current date in the format:
    'raw_flights_DDMMYYYY.json'.
    """
    current_dir = os.getcwd()
    raw_data_dir = os.path.join(current_dir, '..', '..', 'data', 'raw_data')
    raw_data_dir = os.path.abspath(raw_data_dir)

    if not os.path.exists(raw_data_dir):
        os.makedirs(raw_data_dir)
    
    date_str = datetime.now().strftime('%d%m%Y')
    filename = f'raw_flights_{date_str}.json'
    file_path = os.path.join(raw_data_dir, filename)

    try:
        with open(file_path, 'w') as json_file:
            json.dump(flight_data, json_file, indent=4)
        logger.info(f"Flight data saved successfully in {file_path}")
    except Exception as e:
        logger.error(f"Error saving flight data: {e}")

if __name__ == "__main__":
    url = 'https://api.aviationstack.com/v1/flights'
    flight_types = ['arrivals', 'departures']
    for flight_type in flight_types:
        flight_data = ingestFlightData(url, flight_type=flight_type)
        if validateData(flight_data):
            saveFlights(flight_data, flight_type=flight_type)
        else:
            logger.error(f"Invalid data format for {flight_type}. Expected a list of dictionaries.")
