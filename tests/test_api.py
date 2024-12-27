from api.trefle_api import fetch_plants, fetch_plant_details


#Test fetch_plants function
plants_data = fetch_plants(page=1)
if plants_data:
    print('Fetched Plants:')
    for plant in plants_data['data'][:5]:
        print(f"- {plant['common_name']} (ID:{plant['id']})")

if plants_data:
    first_plant_id = plants_data['data'][0]['id']
    plant_details = fetch_plant_details(first_plant_id)
    if plant_details:
        print("\nPlant Details: ")
        print(f"Name: {plant_details['data']['common_name']}")
        print(f"Scientific Name: {plant_details['data']['scientific_name']}")
        print(f"Family : {plant_details['data']['family']}")
