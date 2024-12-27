# import requests
# import json
#
# API_KEY = '-d9grLMzpYCFjJplOQLjR3rGjkEBLtBSPpY2WA55RiY'
# BASE_URL = 'https://trefle.io/api/v1/plants'
# HEADERS = {
#     'Authorization' : f"Bearer {API_KEY}"
# }
# #Filtering
# params = {
#     'token': API_KEY,
#     # 'filter[common_name]' : 'cactus',
#     # 'filter[edible_part]' : 'roots,leaves',
#     # 'range[maximum_height_cm]': '5,20',
#     # 'filter[not_edible_part]': 'roots, stem, leaves, flower, fruits, seeds',
#     # 'order[year]': 'asc',
#     # 'q': 'coconut',
#     # 'filter[common_name]': 'bean',
#     # 'filter[common_name]' : 'coconut'
#     # 'page' : 5
# }
#
# response = requests.get(BASE_URL,headers=HEADERS, params=params)
#
# # Check if the response is successful
# if response.status_code == 200:
#     data = response.json()
#
#     # print(json.dumps(data, indent=4))
#
#     # Extract the list of plants from the response
#     plants = data.get('data', [])
#     print(plants[0])

#     # Open the file in write mode to store the plants data
#     # with open('data.json', 'w') as f:
#     #     # Iterate through each plant in the 'data' key
#     # json.dump(data['data'],  indent=4)  # Dump entire list as JSON with pretty formatting
#
#     # Check if any plants were returned
#     if plants:
#         for plant in plants:
#             print("\nPlant Information:")
#             print(f"Common Name: {plant.get('common_name', 'N/A')}")
#             print(f"Scientific Name: {plant.get('scientific_name', 'N/A')}")
#             print(f"Family: {plant.get('family', 'N/A')}")
#             print(f"Genus: {plant.get('genus', 'N/A')}")
#             # print(f"Synonyms: {', '.join(plant.get('synonyms', []))}")
#             print(f"Year: {plant.get('year', 'N/A')}")
#             # print(f"Image URL: {plant.get('image_url', 'N/A')}")
#     else:
#         print("No plants found.")
# else:
#     print(f"Error: {response.status_code}, {response.text}")
#
#
#
# # for plant in data['data']:
# #     print(plant['common_name'])
# #     print(plant['id'])
#
#
#

# from api.trefle_api import fetch_plant_care_details
#
#
# def test_fetch_plant_care_details():
#     # Example plant name to test
#     plant_name = "coconut"
#
#
#     # Call the function
#     care_details = fetch_plant_care_details(plant_name)
#
#     print(care_details)
#     # Print the results
#     if care_details:
#         print("Care details fetched successfully:")
#         print(care_details)
#     else:
#         print("No care details found for the given plant name.")
#
#
# if __name__ == "__main__":
#     test_fetch_plant_care_details()


import requests

# # Constants
# BASE_URL = "https://trefle.io/api/v1/species"
# API_KEY = "-d9grLMzpYCFjJplOQLjR3rGjkEBLtBSPpY2WA55RiY"  # Replace with your actual API key
# HEADERS = {
#     "Authorization": f"Bearer {API_KEY}"
# }
#
# def fetch_species_data(species_slug):
#     """
#     Fetch detailed information for a plant species by its slug.
#     """
#     url = f"{BASE_URL}/{species_slug}"
#
#     try:
#         response = requests.get(url, headers=HEADERS)
#         response.raise_for_status()
#
#         data = response.json()
#
#         if "data" in data:
#             return data["data"]
#             print(data['growth'])
#         else:
#             return "No data found for this species."
#
#     except requests.exceptions.RequestException as e:
#         return f"Error fetching species data: {e}"
#
#
# # Fetch data for Abies balsamea
# species_slug = "abies-balsamea"  # Slug for Abies balsamea
# species_data = fetch_species_data(species_slug)
#
# # Print out the response to inspect available fields
# print(species_data['growth'])

# import requests
# # Constants
# BASE_URL = "https://trefle.io/api/v1/species"
# API_KEY = "-d9grLMzpYCFjJplOQLjR3rGjkEBLtBSPpY2WA55RiY"  # Replace with your actual API key
# HEADERS = {
#     "Authorization": f"Bearer {API_KEY}"
# }
#
#
# # Make a GET request to the Trefle API to fetch all plant data (or adjust the query as necessary)
# species_slug = "abies-balsamea"
# params = {
#     "filter[species_slug['growth']]": species_slug
# }
#
# response = requests.get(BASE_URL, headers=HEADERS, params = params)

# import requests
#
# # Constants
# BASE_URL = "https://trefle.io/api/v1/species"
# API_KEY = "-d9grLMzpYCFjJplOQLjR3rGjkEBLtBSPpY2WA55RiY"  # Replace with your actual API key
# HEADERS = {
#     "Authorization": f"Bearer {API_KEY}"
# }
# species_slug = "abies-balsamea"
#
#
#
# def fetch_growth_data(species_slug):
#     # Complete URL for the specific species
#     url = f"{BASE_URL}/{species_slug}"
#
#     # Send GET request to fetch species data
#     response = requests.get(url, headers=HEADERS)
#
#     # Check if the request was successful
#     if response.status_code == 200:
#         # Get data from the response
#         info = response.json()
#         data = info['data']
#
#         if data:
#             # Use .get() to avoid key errors if the key is missing
#             growth_data = data.get('growth', 'Growth data not available.')
#             specifications_data = data.get('specifications', 'Specifications data not available.')
#             fruit_or_seed_data = data.get('fruit_or_seed', 'Fruit or seed data not available.')
#
#             # Print the data
#             print(growth_data)
#             print(specifications_data)
#             print(fruit_or_seed_data)
#         else:
#             print("No data available for this species.")
#     else:
#         print(f"Failed to fetch data. Status code: {response.status_code}")
#
# # Example usage
# fetch_growth_data("abies-balsamea")
#


import requests

# Constants
BASE_URL = "https://trefle.io/api/v1"
API_KEY = '-d9grLMzpYCFjJplOQLjR3rGjkEBLtBSPpY2WA55RiY'
HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def fetch_plant_slug(plant_name):
    """
    Search for a plant by its name (common name or scientific name) and fetch its slug.
    """
    url = f"{BASE_URL}/species"
    params = {"filter[common_name]": plant_name}

    try:
        # Make API request to search for the plant by its common name
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()

        # Check if there is any data in the response
        if "data" in data and data["data"]:
            plant = data["data"][0]  # Assuming the first result is the correct one
            species_slug = plant.get("slug")
            return species_slug
        else:
            print(f"No plant found with the name '{plant_name}'.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching plant slug: {e}")
        return None

def fetch_plant_care_details(species_slug):
    """
    Fetch complete plant care details for a given species slug from the Trefle API.
    """
    url = f"{BASE_URL}/species/{species_slug}"

    try:
        # Send GET request to fetch the species details
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()

        # Check if "data" is present
        if "data" in data and data["data"]:
            plant = data["data"]

            # Extract detailed care information from plant data
            care_details = {
                "plant_id": plant.get("id", "Unknown"),  # Include plant ID in the result

                # Fruit or Seed Related Fields
                "conspicuous_fruit": plant.get("fruit_or_seed", {}).get("conspicuous", "Unknown"),
                "fruit_color": plant.get("fruit_or_seed", {}).get("color", []),
                "fruit_shape": plant.get("fruit_or_seed", {}).get("shape", "Unknown"),
                "seed_persistence": plant.get("fruit_or_seed", {}).get("seed_persistence", "Unknown"),

                # Specifications Fields
                "ligneous_type": plant.get("specifications", {}).get("ligneous_type", "Unknown"),
                "growth_form": plant.get("specifications", {}).get("growth_form", "Unknown"),
                "growth_habit": plant.get("specifications", {}).get("growth_habit", "Unknown"),
                "growth_rate": plant.get("specifications", {}).get("growth_rate", "Unknown"),
                "average_height": plant.get("specifications", {}).get("average_height", {}),
                "maximum_height": plant.get("specifications", {}).get("maximum_height", {}),
                "nitrogen_fixation": plant.get("specifications", {}).get("nitrogen_fixation", "Unknown"),
                "shape_and_orientation": plant.get("specifications", {}).get("shape_and_orientation", "Unknown"),
                "toxicity": plant.get("specifications", {}).get("toxicity", "Unknown"),

                # Growth Fields
                "days_to_harvest": plant.get("growth", {}).get("days_to_harvest", "Unknown"),
                "growth_description": plant.get("growth", {}).get("description", "Unknown"),
                "sowing": plant.get("growth", {}).get("sowing", "Unknown"),
                "ph_maximum": plant.get("growth", {}).get("ph_maximum", "Unknown"),
                "ph_minimum": plant.get("growth", {}).get("ph_minimum", "Unknown"),
                "light": plant.get("growth", {}).get("light", "Unknown"),
                "atmospheric_humidity": plant.get("growth", {}).get("atmospheric_humidity", "Unknown"),
                "growth_months": plant.get("growth", {}).get("growth_months", []),
                "bloom_months": plant.get("growth", {}).get("bloom_months", []),
                "fruit_months": plant.get("growth", {}).get("fruit_months", []),
                "row_spacing": plant.get("growth", {}).get("row_spacing", {}),
                "spread": plant.get("growth", {}).get("spread", {}),
                "minimum_precipitation": plant.get("growth", {}).get("minimum_precipitation", {}),
                "maximum_precipitation": plant.get("growth", {}).get("maximum_precipitation", {}),
                "minimum_root_depth": plant.get("growth", {}).get("minimum_root_depth", {}),
                "minimum_temperature": plant.get("growth", {}).get("minimum_temperature", {}),
                "maximum_temperature": plant.get("growth", {}).get("maximum_temperature", {}),
                "soil_nutriments": plant.get("growth", {}).get("soil_nutriments", "Unknown"),
                "soil_salinity": plant.get("growth", {}).get("soil_salinity", "Unknown"),
                "soil_texture": plant.get("growth", {}).get("soil_texture", "Unknown"),
                "soil_humidity": plant.get("growth", {}).get("soil_humidity", "Unknown"),
            }

            return care_details

        else:
            print("No data found for the specified species slug.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching plant details: {e}")
        return None

def get_plant_details():
    """
    Get the plant name from the user, fetch the slug, and then fetch the detailed plant care info.
    """
    plant_name = input("Enter the plant name (common name or scientific name): ").strip()

    # Step 1: Fetch the slug for the given plant name
    species_slug = fetch_plant_slug(plant_name)

    if species_slug:
        # Step 2: Fetch the detailed care information using the slug
        care_details = fetch_plant_care_details(species_slug)

        if care_details:
            # Print out the fetched plant care details
            print(f"Plant care details for {plant_name}:")
            print(care_details)
        else:
            print("No care details found for this species.")
    else:
        print("Plant not found. Please check the name and try again.")

# Example usage
get_plant_details()
