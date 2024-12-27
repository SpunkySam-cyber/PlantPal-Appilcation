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
            self.content_frame, text="Health Checkup", font=("Arial", 32, "bold"),
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
            str: Health status message.
        """
        health_issues = []

        # Evaluate sunlight exposure
        recommended_light = care_details.get("light")  # Assume API provides light as an integer scale
        if recommended_light:
            if "Full Sun" in sunlight and recommended_light < 7:
                health_issues.append("This plant may be getting too much sunlight.")
            elif "Shade" in sunlight and recommended_light > 3:
                health_issues.append("This plant may need more sunlight.")

        # Evaluate watering status
        recommended_water = care_details.get("precipitation_min")  # Example field
        if recommended_water:
            if "Saturated" in watering:
                health_issues.append("Soil is too wet; reduce watering.")
            elif "Dry" in watering or "Very Dry" in watering:
                health_issues.append("Plant may need more water.")

        # Determine overall health
        if not health_issues:
            return "The plant appears healthy based on the provided conditions."
        else:
            return "\n".join(health_issues)
