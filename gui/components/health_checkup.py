import customtkinter as ctk
from tkinter import messagebox  # For displaying feedback messages
from api.trefle_api import fetch_plant_care_details  # Assuming this fetches plant care details from an API
from gui.components.homepage import Homepage

class HealthCheckupPage(ctk.CTkFrame):
    def __init__(self, master, switch_page_callback):
        super().__init__(master)

        self.switch_page_callback = switch_page_callback  # Save callback reference

        # Main Content Frame
        self.content_frame = ctk.CTkFrame(self, fg_color="#90EE90")  # Light background color for the frame
        self.content_frame.pack(fill="both", expand=True)

        # Title
        self.title_label = ctk.CTkLabel(
            self.content_frame, text="🩺Health Checkup", font=("Arial", 32, "bold"),
            text_color="#0B3D26"
        )
        self.title_label.pack(pady=30)

        # Plant Name Input
        self.plant_label = ctk.CTkLabel(self.content_frame, text="Enter Plant Name:", font=("Arial", 20))
        self.plant_label.pack(pady=10)
        self.plant_name_entry = ctk.CTkEntry(
            self.content_frame, placeholder_text="Type plant name here...", font=("Arial", 18), width=300, height = 30
        )
        self.plant_name_entry.pack(pady=15)

        # Sunlight Options
        self.sunlight_label = ctk.CTkLabel(self.content_frame, text="Sunlight Exposure:", font=("Arial", 20))
        self.sunlight_label.pack(pady=10)
        self.sunlight_options = ctk.CTkOptionMenu(
            self.content_frame,
            values=[
                "Full Sun (6+ hours daily)",
                "Partial Sun (4-6 hours daily)",
                "Partial Shade (2-4 hours daily)",
                "Full Shade (Less than 2 hours daily)"
            ],
            font=("Arial", 18),
            height = 35
        )
        self.sunlight_options.pack(pady=15)

        # Watering Options
        self.water_label = ctk.CTkLabel(self.content_frame, text="Watering Status:", font=("Arial", 20))
        self.water_label.pack(pady=10)

        self.water_options = ctk.CTkOptionMenu(
            self.content_frame,
            values=[
                "Saturated (Too much water, soil is soggy)",
                "Optimal (Soil is moist but not soggy)",
                "Dry (Soil is dry, needs watering)",
                "Very Dry (Plant is wilting, urgent watering needed)"
            ],
            font=("Arial", 18),
            height = 35
        )
        self.water_options.pack(pady=15)

        # Check Health Button
        self.check_button = ctk.CTkButton(
            self.content_frame, text="Check Health", command=self.perform_checkup, font=("Arial", 22), width=300, height = 35, border_width=2, border_color="white"
        )
        self.check_button.pack(pady=30)

        # Back to Home Button
        self.back_button = ctk.CTkButton(
            self.content_frame, text="Back to Home", command=lambda: self.switch_page_callback(Homepage), font=("Arial", 22), width=300, height = 35, border_width=2, border_color="white"
        )
        self.back_button.pack(pady=15)

    def perform_checkup(self):
        """
        Perform health checkup based on user inputs (plant name, sunlight, watering)
        and fetch plant care details from the API for evaluation.
        """
        plant_name = self.plant_name_entry.get()
        sunlight = self.sunlight_options.get()
        watering = self.water_options.get()

        if not plant_name:
            messagebox.showwarning("Input Error", "Please enter a plant name.")
            return

        # Fetch plant care details from the API
        care_details = fetch_plant_care_details(plant_name)

        if not care_details:
            messagebox.showwarning("Plant Not Found", f"No care details found for {plant_name}.")
            return

        # Evaluate plant health based on care details
        health_message = self.evaluate_plant_health(care_details, sunlight, watering)

        # Show result in a messagebox
        messagebox.showinfo("Health Checkup Result", health_message)

    def evaluate_plant_health(self, care_details, sunlight, watering):
        """
        Evaluate plant health based on care details and user-provided conditions.

        Args:
            care_details (dict): Recommended care details from the API.
            sunlight (str): User-provided sunlight exposure.
            watering (str): User-provided watering status.

        Returns:
            str: Health status message with feedback on both sunlight and watering.
        """
        health_issues = []
        health_message = ""

        # Extract care details from API response
        recommended_light = care_details.get("light")  # Sunlight requirement as an integer (scale 0-10)
        recommended_humidity = care_details.get("soil_humidity")  # Soil moisture requirement as an integer (scale 0-10)

        # Care Message with relevant details
        care_message = "\n\nPlant Care Details:\n\n"
        if 'light' in care_details:
            light_level = care_details['light']
            light_description = (
                "very low light" if light_level <= 10 else
                "low light" if 10 < light_level <= 20 else
                "medium-low light" if 50 < light_level <= 200 else
                "medium light" if 200 < light_level <= 500 else
                "medium-bright light" if 500 < light_level <= 1000 else
                "bright light")
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

        # Sunlight evaluation
        sunlight_map = {
            "Full Sun (6+ hours daily)": 15,
            "Partial Sun (4-6 hours daily)": 13,
            "Partial Shade (2-4 hours daily)": 8,
            "Full Shade (Less than 2 hours daily)": 1,
        }

        sunlight_value = sunlight_map.get(sunlight, 0)
        if recommended_light:
            if sunlight_value < recommended_light:
                health_issues.append(
                    f"This plant needs more sunlight. It is currently receiving {sunlight.lower()}. Try increasing that by 1-2 hours.")
            elif sunlight_value > recommended_light:
                health_issues.append(
                    f"This plant is getting too much sunlight. It is currently receiving {sunlight.lower()}. Try reducing that by 1-2 hours.")
            else:
                health_message += f"The sunlight is appropriate for this plant. It is currently receiving {sunlight.lower()}. "

        # Watering evaluation
        watering_map = {
            "Saturated (Too much water, soil is soggy)": 9,
            "Optimal (Soil is moist but not soggy)": 6,
            "Dry (Soil is dry, needs watering)": 3,
            "Very Dry (Plant is wilting, urgent watering needed)": 1,
        }

        watering_value = watering_map.get(watering, 0)

        # Overwatering check (Saturated condition)
        if watering_value == 9:
            health_issues.append(
                f"Your plant is being overwatered; reduce watering. The soil is currently {watering.lower()}.")
        # Underwatering check (Very Dry or Dry condition)
        elif watering_value == 1 or watering_value == 3:
            health_issues.append(
                f"Your plant needs more water. The soil is currently {watering.lower()}.")
        # Appropriate watering check
        elif watering_value == 6:
            health_message += f"The watering is appropriate for this plant. It is currently being watered as {watering.lower()}. "

        # If the recommended humidity is available, perform additional checks
        if recommended_humidity is not None:
            if watering_value < recommended_humidity:
                health_issues.append(
                    f"Your plant needs more water. It is currently being watered as {watering.lower()}.")
            elif watering_value > recommended_humidity:
                health_issues.append(
                    f"Your plant is being overwatered; reduce watering. It is currently being watered as {watering.lower()}.")

        # Combine health issues and overall message
        if not health_issues:

            health_message += "The plant appears healthy based on the provided conditions."

        # Combine health message and issues into the final output
        if health_issues:
            return "\n".join(health_issues) + care_message
        else:
            return health_message + care_message
