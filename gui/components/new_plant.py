import customtkinter as ctk
from tkinter import messagebox
from api.trefle_api import fetch_plant_care_details_new_plant  # Updated function name
from gui.components.homepage import Homepage

class NewPlantPage(ctk.CTkFrame):
    def __init__(self, master, switch_page_callback):
        super().__init__(master)

        # Main Content Frame
        self.content_frame = ctk.CTkFrame(self, fg_color="#90EE90")  # Lighter background color for clarity
        self.content_frame.pack(fill="both", expand=True)

        # Title
        self.title_label = ctk.CTkLabel(
            self.content_frame,
            text="🌱 Add a New Plant 🌱",
            font=("Arial", 32, "bold"),
            text_color="#0B3D26"
        )
        self.title_label.pack(pady=30)

        # Plant Name
        self.name_label = ctk.CTkLabel(self.content_frame, text="Plant Name:", font=("Arial", 20))
        self.name_label.pack(pady=10)
        self.name_entry = ctk.CTkEntry(
            self.content_frame,
            placeholder_text="Enter plant name",
            font=("Arial", 18),
            width=300,
            height=40
        )
        self.name_entry.pack(pady=15)

        # Species (optional)
        self.species_label = ctk.CTkLabel(self.content_frame, text="Plant Species (optional):", font=("Arial", 20))
        self.species_label.pack(pady=10)
        self.species_entry = ctk.CTkEntry(
            self.content_frame,
            placeholder_text="Enter plant species",
            font=("Arial", 18),
            width=300,
            height=40
        )
        self.species_entry.pack(pady=15)

        # Description (optional)
        self.description_label = ctk.CTkLabel(self.content_frame, text="Description (optional):", font=("Arial", 20))
        self.description_label.pack(pady=10)
        self.description_entry = ctk.CTkEntry(
            self.content_frame,
            placeholder_text="Enter plant description",
            font=("Arial", 18),
            width=300,
            height=40
        )
        self.description_entry.pack(pady=15)

        # Save Button
        self.save_button = ctk.CTkButton(
            self.content_frame,
            text="Save Plant",
            command=self.save_plant,
            font=("Arial", 22),
            width=300,
            height=35,
            border_width=2,
            border_color="white"
        )
        self.save_button.pack(pady=30)

        self.back_to_home_button = ctk.CTkButton(
            self.content_frame,
            text = "Back To Home",
            command = lambda : switch_page_callback(Homepage),
            font = ("Arial", 22),
            width = 300,
            height = 35,
            border_width=2,
            border_color="white"
        )
        self.back_to_home_button.pack(pady = 15)

    def save_plant(self):
        # Get the entered data
        plant_name = self.name_entry.get()
        species = self.species_entry.get()
        description = self.description_entry.get()

        # Check if the plant name is provided
        if not plant_name:
            messagebox.showwarning("Input Error", "Please enter the plant name.")
            return

        # Fetch plant care details using the new API function (fetch all plants and filter)
        care_details = fetch_plant_care_details_new_plant(plant_name, species, description)

        if not care_details:
            messagebox.showwarning("Plant Not Found", f"No care details found for {plant_name}.")
            return

        # Show a confirmation message with the fetched care details
        care_message = (
            f"Light: {care_details['light']}\n"
            f"Watering: {care_details['watering']}\n"
            f"Temperature: {care_details['temperature']}\n"
            f"Humidity: {care_details['humidity']}\n"
            f"Fertilization: {care_details['fertilization']}\n"
            f"Description: {care_details['description']}"
        )

        # Display the plant care details
        messagebox.showinfo("Plant Care Details", care_message)
