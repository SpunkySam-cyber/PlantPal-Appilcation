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


import requests

def fetch_plant_care_details(plant_name):
    """
    Fetch plant care details using the provided plant name (common or scientific name).
    It fetches the plant details and care information based on the name.

    Args:
        plant_name (str): The name of the plant to fetch care details for (common or scientific name).

    Returns:
        dict: A dictionary containing care details for the plant (light, pH range, temperature range, etc.)
              or None if no plant was found.
    """
    API_KEY = "-d9grLMzpYCFjJplOQLjR3rGjkEBLtBSPpY2WA55RiY"  # Your Trefle API key
    BASE_URL = "https://trefle.io/api/v1"
    HEADERS = {
        "Authorization": f"Bearer {API_KEY}"
    }

    url = f"{BASE_URL}/species"
    params = {"filter[common_name]": plant_name.lower()}  # Search by common name

    try:
        # Search for the plant by common name
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()

        if "data" not in data or not data["data"]:
            print(f"No data found for plant: {plant_name}")
            return None

        # If data is found, extract the slug for more detailed information
        plant = data["data"][0]  # Assuming the first result is the correct one
        species_slug = plant.get("slug")

        if species_slug:
            species_url = f"{BASE_URL}/species/{species_slug}"
            species_response = requests.get(species_url, headers=HEADERS)
            species_response.raise_for_status()
            species_data = species_response.json()

            # Extract care details from the response
            if "data" in species_data and species_data["data"]:
                plant_data = species_data["data"]
                care_details = {
                    "light": plant_data.get("growth", {}).get("light"),
                    "humidity": plant_data.get("growth", {}).get("atmospheric_humidity"),
                    "temperature": plant_data.get("growth", {}).get("temperature"),
                    "soil_type": plant_data.get("growth", {}).get("soil_type"),
                    "ph_maximum": plant_data.get("growth", {}).get("ph_maximum"),
                    "ph_minimum": plant_data.get("growth", {}).get("ph_minimum"),
                    "growth_rate": plant_data.get("specifications", {}).get("growth_rate"),
                    "growth_form": plant_data.get("specifications", {}).get("growth_form"),
                    "growth_habit": plant_data.get("specifications", {}).get("growth_habit"),
                    "average_height": plant_data.get("specifications", {}).get("average_height"),
                    "maximum_height": plant_data.get("specifications", {}).get("maximum_height"),
                    "description": plant_data.get("description"),
                    "fruit_or_seed": plant_data.get("fruit_or_seed"),
                    # New fields for flower
                    "flower_color": plant_data.get("flower", {}).get("color"),
                    "flower_conspicuous": plant_data.get("flower", {}).get("conspicuous"),
                    # New fields for foliage
                    "foliage_texture": plant_data.get("foliage", {}).get("texture"),
                    "foliage_color": plant_data.get("foliage", {}).get("color"),
                    "leaf_retention": plant_data.get("foliage", {}).get("leaf_retention")
                }

                return care_details  # Return care details dictionary

            else:
                print("No care details found for the plant.")
                return None
        else:
            print("No plant details found for the given name.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching plant care details: {e}")
        return None




def fetch_plant_care_details_new_plant(plant_name_or_scientific=None, family_name=None):
    """
    Fetch plant care details using either the common name, scientific name, or family name.
    First, it will search using the provided input, and then fetch care details.
    """
    API_KEY = "-d9grLMzpYCFjJplOQLjR3rGjkEBLtBSPpY2WA55RiY"
    BASE_URL = "https://trefle.io/api/v1"
    HEADERS = {
        "Authorization": f"Bearer {API_KEY}"
    }

    # Step 1: Search for the plant using the provided input (common name, scientific name, or family)
    url = f"{BASE_URL}/species"
    params = {}

    if plant_name_or_scientific:
        # First try by common_name
        params["filter[common_name]"] = plant_name_or_scientific.lower()
        print(f"Searching by common name: {params['filter[common_name]']}")

        # If nothing is found, try by scientific_name
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()

        if "data" not in data or not data["data"]:
            # If no data returned, clear the params and try by scientific name
            params = {"filter[scientific_name]": plant_name_or_scientific.lower()}
            print(f"Searching by scientific name: {params['filter[scientific_name]']}")
            response = requests.get(url, headers=HEADERS, params=params)
            response.raise_for_status()
            data = response.json()

    elif family_name:
        params["filter[family]"] = family_name.lower()  # Try searching by family name
        print(f"Searching by family: {params['filter[family]']}")
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()

    try:
        # Check if there is any data in the response
        if "data" in data and data["data"]:
            plant = data["data"][0]  # Assuming the first result is the correct one

            # Basic plant information (for feedback to the user)
            basic_info = {
                "common_name": plant.get("common_name", "Unknown common name"),
                "scientific_name": plant.get("scientific_name", "Unknown scientific name"),
                "family": plant.get("family", "Unknown family"),
                "description": plant.get("description", "No description available")
            }

            # Step 2: Fetch the plant care details using the slug
            species_slug = plant.get("slug")
            if species_slug:
                species_url = f"{BASE_URL}/species/{species_slug}"
                species_response = requests.get(species_url, headers=HEADERS)
                species_response.raise_for_status()
                species_data = species_response.json()

                # Extract care information
                care_details = {}
                if "data" in species_data and species_data["data"]:
                    plant_data = species_data["data"]
                    print(plant_data['growth'])

                    # Extract relevant fields from the response
                    fields = {
                        "light": plant_data.get("growth", {}).get("light"),
                        "humidity": plant_data.get("growth", {}).get("atmospheric_humidity"),
                        "temperature": plant_data.get("growth", {}).get("temperature"),
                        "soil_type": plant_data.get("growth", {}).get("soil_type"),
                        "ph_maximum": plant_data.get("growth", {}).get("ph_maximum"),
                        "ph_minimum": plant_data.get("growth", {}).get("ph_minimum"),
                        "growth_rate": plant_data.get("specifications", {}).get("growth_rate"),
                        "growth_form": plant_data.get("specifications", {}).get("growth_form"),
                        "growth_habit": plant_data.get("specifications", {}).get("growth_habit"),
                        "average_height": plant_data.get("specifications", {}).get("average_height"),
                        "maximum_height": plant_data.get("specifications", {}).get("maximum_height"),
                        "description": plant_data.get("description"),
                        "fruit_or_seed": plant_data.get("fruit_or_seed"),
                        # New fields for flower
                        "flower_color": plant_data.get("flower", {}).get("color"),
                        "flower_conspicuous": plant_data.get("flower", {}).get("conspicuous"),
                        # New fields for foliage
                        "foliage_texture": plant_data.get("foliage", {}).get("texture"),
                        "foliage_color": plant_data.get("foliage", {}).get("color"),
                        "leaf_retention": plant_data.get("foliage", {}).get("leaf_retention")
                    }

                    # Add non-null fields to the care_details dictionary
                    for key, value in fields.items():
                        if value is not None and value != "":
                            care_details[key] = value

                return basic_info, care_details  # Return both basic information and care details
            else:
                print("No plant details found for the given name or slug.")
                return None
        else:
            print("No plants found matching the provided name or family.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching plant care details: {e}")
        return None
