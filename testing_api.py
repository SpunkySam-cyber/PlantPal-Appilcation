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
#
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

from api.trefle_api import fetch_plant_care_details


def test_fetch_plant_care_details():
    # Example plant name to test
    plant_name = "coconut"


    # Call the function
    care_details = fetch_plant_care_details(plant_name)

    print(care_details)
    # Print the results
    if care_details:
        print("Care details fetched successfully:")
        print(care_details)
    else:
        print("No care details found for the given plant name.")


if __name__ == "__main__":
    test_fetch_plant_care_details()

