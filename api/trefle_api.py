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
