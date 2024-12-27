import customtkinter as ctk
from tkinter import messagebox
from api.trefle_api import fetch_plant_care_details_new_plant  # Updated function name
from gui.components.homepage import Homepage
import json
import os

class NewPlantPage(ctk.CTkFrame):
    def __init__(self, master, switch_page_callback):
        super().__init__(master)

        # Main Content Frame
        self.content_frame = ctk.CTkFrame(self, fg_color="#90EE90")  # Lighter background color for clarity
        self.content_frame.pack(fill="both", expand=True)

        # Title
        self.title_label = ctk.CTkLabel(
            self.content_frame,
            text="🌱 Congrats on Getting Your New Plant 🌱",
            font=("Arial", 32, "bold"),
            text_color="#0B3D26"
        )
        self.title_label.pack(pady=30)

        # Plant Name
        self.name_label = ctk.CTkLabel(self.content_frame, text="Plant Name:", font=("Arial", 20, 'bold'))
        self.name_label.pack(pady=10)
        self.name_entry = ctk.CTkEntry(
            self.content_frame,
            placeholder_text="Enter the common or scientific name ",
            font=("Arial", 18),
            width=320,
            height=40
        )
        self.name_entry.pack(pady=15)

        # Family Name (optional)
        self.family_name_label = ctk.CTkLabel(self.content_frame, text="Family Name (Optional):", font=("Arial", 20, 'bold'))
        self.family_name_label.pack(pady=10)
        self.family_name_entry = ctk.CTkEntry(
            self.content_frame,
            placeholder_text="Enter the plant's family name if known ",
            font=("Arial", 18),
            width=320,
            height=40
        )
        self.family_name_entry.pack(pady=15)

        # Description (optional)
        self.description_label = ctk.CTkLabel(self.content_frame, text="Additional Notes (Optional):", font=("Arial", 20, 'bold'))
        self.description_label.pack(pady=10)
        self.description_entry = ctk.CTkEntry(
            self.content_frame,
            placeholder_text="Any details (e.g.purchase date, pot size)",
            font=("Arial", 18),
            width=320,
            height=40
        )
        self.description_entry.pack(pady=15)

        # Save Button
        self.save_button = ctk.CTkButton(
            self.content_frame,
            text="Save Plant Details",
            command=self.save_plant,
            font=("Arial", 22),
            width=300,
            height=40,
            border_width=2,
            border_color="white"
        )
        self.save_button.pack(pady=30)

        # Back to Home Button
        self.back_to_home_button = ctk.CTkButton(
            self.content_frame,
            text="Back to Home",
            command=lambda: switch_page_callback(Homepage),
            font=("Arial", 22),
            width=300,
            height=40,
            border_width=2,
            border_color="white"
        )
        self.back_to_home_button.pack(pady=15)

    def save_plant(self):
        # Get the entered data
        plant_name_or_scientific = self.name_entry.get().strip().lower()  # Common name or scientific name
        family_name = self.family_name_entry.get().strip() if self.family_name_entry.get() else None  # Optional family name field
        description = self.description_entry.get().strip() if self.description_entry.get() else None  # Optional description field

        # Save the plant details to a dictionary
        plant_data = {
            "name": plant_name_or_scientific,
            "family_name": family_name,
            "description": description,
        }

        # Check if the plant name (common or scientific) is provided
        if not plant_name_or_scientific:
            messagebox.showwarning("Input Error", "Please enter the plant name or scientific name.")
            return

        # Save to list/message demonstration
        success_message = f"Plant '{plant_name_or_scientific}' successfully added to your list!"
        if family_name:
            success_message += f"\nFamily: {family_name}"
        if description:
            success_message += f"\nNotes: {description}"

        # Show success message
        messagebox.showinfo("Plant Saved", success_message)
        # Save the plant details to a JSON file
        file_path = "assets/plants_data.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                existing_data = json.load(file)
        else:
            existing_data = []

        # Add the new plant data to the list
        existing_data.append(plant_data)

        # Write the updated data back to the JSON file
        with open(file_path, "w") as file:
            json.dump(existing_data, file, indent=4)

        # Fetch plant care details using the API function
        result = fetch_plant_care_details_new_plant(plant_name_or_scientific, family_name)

        # Check if the result is None
        if result is None:
            messagebox.showwarning("Plant Not Found", f"No care details found for '{plant_name_or_scientific}'.")
            return

        # Unpack the result into basic_info and care_details
        basic_info, care_details = result

        # Construct the Basic Info section
        basic_info_message = "Basic Information:\n\n"
        basic_info_message += "\n".join([
            f"Common Name: {basic_info.get('common_name', 'N/A')}",
            f"Scientific Name: {basic_info.get('scientific_name', 'N/A')}",
            f"Family: {basic_info.get('family', 'N/A')}",
            f"Description: {basic_info.get('description', 'No description available')}"
        ])

        # Construct the Care Details section
        care_message = "\n\nPlant Care Details:\n\n"
        if 'light' in care_details:
            light_level = care_details['light']
            light_description = (
                "very low light" if light_level <= 10 else
                "low light" if 10 < light_level <= 20 else
                "medium-low light" if 50 < light_level <= 200 else
                "medium light" if 200 < light_level <= 500 else
                "medium-bright light" if 500 < light_level <= 1000 else
                "bright light" )
            care_message += f"☀️ Sunlight: This plant needs {light_description}.\n"

        if 'humidity' in care_details:
            care_message += f"💧 Humidity: Around {care_details['humidity']}%.\n"

        if 'growth_rate' in care_details:
            care_message += f"📈 Growth rate: {care_details['growth_rate']} rate.\n"

        if 'minimum_temperature' in care_details and 'maximum_temperature' in care_details:
            care_message += f"🌡️ Temperature: {care_details['minimum_temperature']}°C to {care_details['maximum_temperature']}°C.\n"

        if 'soil_type' in care_details:
            care_message += f"🌿 Soil Type: {care_details['soil_type']} soil.\n"

        if 'ph_minimum' in care_details and 'ph_maximum' in care_details:
            care_message += f"🧑‍🌾 Soil pH: {care_details['ph_minimum']} to {care_details['ph_maximum']}.\n"

        care_message += "💦 Watering: Water regularly, ensuring soil doesn't become soggy.\n"

        # Construct the Extra Info section
        extra_info_message = "\n\nExtra Information:\n\n"
        if 'flower_color' in care_details or 'flower_conspicuous' in care_details:
            flower_message = "🌸 Flowers:"
            if 'flower_color' in care_details:
                flower_message += f" Color(s): {', '.join(care_details['flower_color'])}."
            if 'flower_conspicuous' in care_details:
                flower_message += f" Conspicuous: {'Yes' if care_details['flower_conspicuous'] else 'No'}."
            extra_info_message += flower_message + "\n"

        if 'foliage_texture' in care_details or 'foliage_color' in care_details or 'leaf_retention' in care_details:
            foliage_message = "🌿 Foliage:"
            if 'foliage_texture' in care_details:
                foliage_message += f" Texture: {care_details['foliage_texture']}."
            if 'foliage_color' in care_details:
                foliage_message += f" Color(s): {', '.join(care_details['foliage_color'])}."
            if 'leaf_retention' in care_details:
                foliage_message += f" Evergreen: {'Yes' if care_details['leaf_retention'] else 'No'}."
            extra_info_message += foliage_message + "\n"

        # General care instructions
        general_care_message = """
        🌟 General Plant Care Tips 🌟
        1. Watering: Always check the soil before watering. Overwatering can cause root rot, and underwatering can dry out the plant.
        2. Lighting: Place your plant in a location with the recommended light level, and rotate it occasionally to ensure even growth.
        3. Humidity: If your plant prefers higher humidity, group it with other plants or use a humidifier. Misting is also a good option.
        4. Temperature: Keep your plant away from extreme temperatures, such as drafty windows, heaters, or air conditioners.
        5. Feeding: Use a balanced fertilizer during the plant's active growing season, but avoid over-fertilizing.
        6. Pest Control: Check your plant regularly for pests like aphids, mealybugs, and spider mites. Use natural or chemical pest controls as needed.
        7. Pruning: Remove dead or yellowing leaves to keep the plant healthy and promote new growth.
        8. Repotting: Repot your plant every 1-2 years, or when it outgrows its current pot, to ensure proper root development.
        """

        # Combine all sections into one message
        full_message = f"{basic_info_message}{care_message}{extra_info_message}{general_care_message}"

        # Display the combined message
        messagebox.showinfo("Plant Information", full_message)
