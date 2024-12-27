import customtkinter as ctk
from PIL import Image, ImageTk
import requests
from api.trefle_api import fetch_plants  # Import the API function to fetch plant data
from gui.components.homepage import Homepage



class SearchPage(ctk.CTkFrame):
    def __init__(self, parent,switch_page_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.switch_page_callback = switch_page_callback

        # Configure frame appearance
        self.configure(fg_color="#90EE90")  # Background color

        # Set up the search UI
        self.setup_search_ui()

    def setup_search_ui(self):
        """Set up the search UI components."""

        # Search Section: Frame for search input and button
        self.search_frame = ctk.CTkFrame(self, corner_radius=10, fg_color='white')
        self.search_frame.pack(pady=20, padx=20, fill="x")

        # Back to Home Button (Add it here)
        self.back_button = ctk.CTkButton(
            self.search_frame,
            text="Back to Home",
            command=lambda: self.switch_page_callback(Homepage),
            font=("Arial", 14)
        )
        self.back_button.pack(side="left", padx=10, pady=10)  # Positioning the button

        # Dropdown menu for filter selection
        self.filter_label = ctk.CTkLabel(self.search_frame, text="Search by:", font=("Arial", 14), height=60)
        self.filter_label.pack(side="left", padx=10)

        self.filter_var = ctk.StringVar(value="common_name")
        self.filter_menu = ctk.CTkOptionMenu(
            self.search_frame,
            variable=self.filter_var,
            values=["common_name", "scientific_name", "family"]
        )
        self.filter_menu.pack(side="left", padx=10)

        # Search input field
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Enter search term...", width=400)
        self.search_entry.pack(side="left", padx=10)

        # Search button
        self.search_button = ctk.CTkButton(self.search_frame, text="Search", command=self.search_plants)
        self.search_button.pack(side="left", padx=10)

        # Results Section: Scrollable frame for displaying plant results
        self.results_canvas = ctk.CTkCanvas(self, bg="#FFFFFF", highlightthickness=0)
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.results_canvas.yview)

        self.results_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.results_canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        self.scrollbar.pack(side="right", fill="y")

        self.results_frame = ctk.CTkFrame(self.results_canvas, corner_radius=10, fg_color="#FFFFFF")
        self.results_frame_id = self.results_canvas.create_window((0, 0), window=self.results_frame, anchor="nw")

        # Bind canvas for dynamic resizing
        self.results_frame.bind(
            "<Configure>", lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all"))
        )
        self.results_canvas.bind(
            "<Configure>", lambda e: self.results_canvas.itemconfig(self.results_frame_id, width=e.width)
        )

    def search_plants(self):
        """Handle search functionality to find and display plants."""
        query = self.search_entry.get().strip()
        filter_type = self.filter_var.get()

        if not query:
            self.display_message("Please enter a search term.")
            return

        # Show loading indicator
        self.show_loading()

        # Fetch and display plant data
        try:
            self.after(100, lambda: self.fetch_and_display_plants(filter_type, query))
        except Exception as e:
            self.hide_loading()
            self.display_message(f"Error: {e}")

    def fetch_and_display_plants(self, filter_type, query):
        """Fetch plants and display them in the results section."""
        try:
            plants_data = fetch_plants(filter_type, query)

            if plants_data and isinstance(plants_data, list):
                self.hide_loading()
                self.display_plants(plants_data)
            else:
                self.hide_loading()
                self.display_message("No plants found for your search.")
        except Exception as e:
            self.hide_loading()
            self.display_message(f"Error fetching plants: {e}")

    def display_plants(self, plants):
        """Display plant details in the results frame."""
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        for plant in plants:
            # Extract plant details
            common_name = plant.get("common_name", "Unknown Plant")
            scientific_name = plant.get("scientific_name", "Unknown Scientific Name")
            family = plant.get("family", "Unknown Family")
            genus = plant.get("genus", "Unknown Genus")
            year = plant.get("year", "Unknown Year")
            bibliography = plant.get("bibliography", "No Bibliography")
            image_url = plant.get("image_url")

            # Create a frame for each plant
            plant_frame = ctk.CTkFrame(self.results_frame, corner_radius=30,fg_color="#90EE90")
            plant_frame.pack(fill="x", padx=10, pady=5)

            # Display plant details
            plant_info = (f"Common Name: {common_name}\nScientific Name: {scientific_name}\n"
                          f"Family: {family}\nGenus: {genus}\nYear: {year}\nBibliography: {bibliography}")
            text_label = ctk.CTkLabel(plant_frame, text=plant_info, font=("Arial", 12), justify="left", anchor="w")
            text_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            # Display plant image
            if image_url:
                img_label = ctk.CTkLabel(plant_frame, text="")
                img_label.grid(row=0, column=1, padx=10, pady=10, sticky="e")

                img = self.fetch_and_convert_image(image_url)
                if img:
                    img_label.configure(image=img)
                    img_label.image = img
                else:
                    img_label.configure(text="Image not available")

    def fetch_and_convert_image(self, image_url):
        """Fetch and process an image from a URL."""
        try:
            image = Image.open(requests.get(image_url, stream=True).raw)
            image.thumbnail((300, 300))
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error fetching image: {e}")
            return None

    def display_message(self, message):
        """Display a message in the results frame."""
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        label = ctk.CTkLabel(self.results_frame, text=message, font=("Arial", 14))
        label.pack(pady=20)

    def show_loading(self):
        """Display a loading indicator."""
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        self.loading_label = ctk.CTkLabel(self.results_frame, text="Loading...", font=("Arial", 14))
        self.loading_label.pack(pady=20)

    def hide_loading(self):
        """Remove the loading indicator."""
        if hasattr(self, 'loading_label') and self.loading_label.winfo_exists():
            self.loading_label.destroy()
