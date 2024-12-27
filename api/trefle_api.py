import requests

# API Constants
API_KEY = "-d9grLMzpYCFjJplOQLjR3rGjkEBLtBSPpY2WA55RiY"
BASE_URL = "https://trefle.io/api/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}


def fetch_plants(filter_key=None, filter_value=None):
    """
    Fetch plants from the Trefle API using filters, searching through all pages.

    Args:
        filter_key (str): The key to filter by (e.g., 'common_name', 'scientific_name', 'family').
        filter_value (str): The value to filter by (e.g., 'Rose', 'Rosa', 'Rosaceae').

    Returns:
        list: A list of plants matching the filters across all pages.
    """
    url = f"{BASE_URL}/plants"
    page = 1
    all_plants = []

    valid_filters = {'common_name', 'scientific_name', 'family'}
    if filter_key and filter_key not in valid_filters:
        raise ValueError(f"Invalid filter_key: {filter_key}. Valid keys are: {valid_filters}")

    while True:
        params = {"page": page}

        # Add filter if provided
        if filter_key and filter_value:
            params[f"filter[{filter_key}]"] = filter_value

        try:
            response = requests.get(url, headers=HEADERS, params=params)
            response.raise_for_status()
            data = response.json()

            if "data" in data:
                all_plants.extend(data["data"])  # Add fetched plants to the result list

                # Check if there is a next page
                if data.get("links", {}).get("next"):
                    page += 1  # Move to the next page
                else:
                    break  # No more pages, exit the loop
            else:
                break  # If no data is found, exit the loop

        except requests.exceptions.RequestException as e:
            print(f"Error fetching plants: {e}")
            break  # Exit on error

    return all_plants
def fetch_plant_care_details(plant_name):
    url = f"{BASE_URL}/plants"
    params = {"page": 1}
    all_plants = []

    try:
        # Fetch all pages of plant data
        while True:
            print(f"Fetching page {params['page']}...")
            response = requests.get(url, headers=HEADERS, params=params)
            response.raise_for_status()
            data = response.json()

            if "data" in data and data["data"]:
                all_plants.extend(data["data"])
                print(f"Number of plants fetched on page {params['page']}: {len(data['data'])}")
            else:
                print(f"No data found on page {params['page']}.")
                break

            # Check if there is a next page
            if not data.get("links", {}).get("next"):
                break
            params["page"] += 1

        print(f"Total plants fetched: {len(all_plants)}")

        # Find the plant by name
        matching_plants = [
            plant for plant in all_plants if plant_name.lower() in (plant.get("common_name") or "").lower()
        ]
        if not matching_plants:
            print(f"No matching plants found for: {plant_name}")
            return None

        # Fetch detailed data for the first matching plant
        plant_link = matching_plants[0].get("links", {}).get("self")
        if not plant_link:
            print(f"No detailed link found for: {plant_name}")
            return None

        response = requests.get(plant_link, headers=HEADERS)
        response.raise_for_status()
        plant_details = response.json()

        # Extract key growth information
        growth = plant_details.get("data", {}).get("main_species", {}).get("growth", {})
        if not growth:
            print(f"No growth details found for: {plant_name}")
            return None

        care_details = {
            "light": growth.get("light"),  # Light requirement (scale 0-10)
            "ph_range": (growth.get("ph_minimum"), growth.get("ph_maximum")),  # Soil pH range
            "temperature_range": (
                growth.get("minimum_temperature", {}).get("celsius"),
                growth.get("maximum_temperature", {}).get("celsius"),
            ),  # Min and max temperature
            "soil_humidity": growth.get("soil_humidity"),  # Soil moisture (scale 0-10)
            "description": growth.get("description"),  # Growth description
        }

        return care_details

    except requests.exceptions.RequestException as e:
        print(f"Error fetching plant care details: {e}")
        return None

def fetch_plant_care_details_new_plant(plant_name, species=None, description=None):
    """
    Fetch plant care details based on the plant name, species, and description from an API.

    Args:
        plant_name (str): The common name of the plant.
        species (str, optional): The scientific name of the plant. Defaults to None.
        description (str, optional): Additional description or plant details. Defaults to None.

    Returns:
        dict: A dictionary containing plant care details or None if not found.
    """

    # URL for the API (e.g., Trefle API or another plant care API)
    api_url = "https://api.trefle.io/v1/plants"  # plant API URL


    # Prepare the search parameters
    params = {"q": plant_name, "token": API_KEY, 'filter[common_Name]': plant_name}

    if species:
        params["species"] = species
    if description:
        params["description"] = description

    try:
        # Make the request to the plant care API
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Check if the request was successful

        # Parse the response JSON
        data = response.json()

        # Check if the plant is found in the API response
        if data["data"]:
            plant_info = data["data"][0]  # Assuming the first result is the best match

            # Extract plant care details from the response
            care_details = {
                "light": plant_info.get("light", "Unknown"),
                "watering": plant_info.get("watering", "Unknown"),
                "temperature": plant_info.get("temperature", "Unknown"),
                "humidity": plant_info.get("humidity", "Unknown"),
                "fertilization": plant_info.get("fertilization", "Unknown"),
                "description": plant_info.get("description", "No description available.")
            }

            return care_details
        else:
            return None  # No plant details found for the given name and species

    except requests.exceptions.RequestException as e:
        print(f"Error fetching plant details: {e}")
        return None
