import customtkinter as ctk
import requests
from api.trefle_api import fetch_plants  # Custom API function to fetch plant data
from PIL import Image, ImageTk

# Configure app appearance and theme
ctk.set_appearance_mode("light")  # Modes: "system", "light", "dark"
ctk.set_default_color_theme("green")  # Themes: "blue", "dark-blue", "green"


class PlantPalApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set up the main application window
        self.title("Plant Pal")  # Window title
        self.geometry("800x500")  # Window size
        self.configure(bg="#F0F4F8")  # Background color

        # Search Section: Frame for search input and button
        self.search_frame = ctk.CTkFrame(self, corner_radius=10)  # Frame for search bar
        self.search_frame.pack(pady=20, padx=20, fill="x")  # Position frame at the top

        # Dropdown menu for filter selection
        self.filter_label = ctk.CTkLabel(self.search_frame, text="Search by:", font=("Arial", 14))
        self.filter_label.pack(side="left", padx=10)  # Label for filter selection

        self.filter_var = ctk.StringVar(value="common_name")  # Default filter
        self.filter_menu = ctk.CTkOptionMenu(
            self.search_frame,
            variable=self.filter_var,
            values=["common_name", "scientific_name", "family"]
        )
        self.filter_menu.pack(side="left", padx=10)  # Dropdown for filter selection

        # Search label and input field
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Enter search term...", width=400)
        self.search_entry.pack(side="left", padx=10)  # Input field for search query

        # Search button
        self.search_button = ctk.CTkButton(self.search_frame, text="Search", command=self.search_plants)
        self.search_button.pack(side="left", padx=10)  # Button to trigger search

        # Results Section: Frame for displaying plant results with scrollbar
        self.results_canvas = ctk.CTkCanvas(self, bg="#FFFFFF", highlightthickness=0)  # Canvas for scrollable content
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.results_canvas.yview)  # Scrollbar

        # Configure the scrollbar with the canvas
        self.results_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack the canvas and scrollbar
        self.results_canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        self.scrollbar.pack(side="right", fill="y")

        # Create an internal frame inside the canvas for the results
        self.results_frame = ctk.CTkFrame(self.results_canvas, corner_radius=10, fg_color="#FFFFFF")
        self.results_frame_id = self.results_canvas.create_window((0, 0), window=self.results_frame, anchor="nw")

        # Bind the canvas to adjust the scroll region dynamically
        self.results_frame.bind("<Configure>",
                                lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all")))
        self.results_canvas.bind("<Configure>",
                                 lambda e: self.results_canvas.itemconfig(self.results_frame_id, width=e.width))

    def show_loading(self):
        """Display a loading indicator in the results frame."""
        # Clear existing results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        # Display loading message
        self.loading_label = ctk.CTkLabel(self.results_frame, text="Loading...", font=("Arial", 14))
        self.loading_label.pack(pady=20)

    def hide_loading(self):
        """Remove the loading indicator."""
        if hasattr(self, 'loading_label') and self.loading_label.winfo_exists():
            self.loading_label.destroy()

    def search_plants(self):
        """Handle search functionality to find and display plants."""
        query = self.search_entry.get().strip()  # Get search term from input
        filter_type = self.filter_var.get()  # Get selected filter type

        if not query:  # Check if the input is empty
            self.display_message("Please enter a search term.")  # Show error if no input
            return

        # Display the loading indicator
        self.show_loading()

        # Fetch plant data from the API
        try:
            self.after(100, lambda: self.fetch_and_display_plants(filter_type, query))
        except Exception as e:
            self.hide_loading()
            self.display_message(f"Error fetching plants: {e}")

    def fetch_and_display_plants(self, filter_type, query):
        """Fetch plants and display them after loading."""
        try:
            plants_data = fetch_plants(filter_type, query)  # Call the custom API function

            # Check if valid results are returned and display them
            if plants_data and isinstance(plants_data, list) and len(plants_data) > 0:
                self.hide_loading()
                self.display_plants(plants_data)
            else:
                self.hide_loading()
                self.display_message("No plants found for your search.")  # No results case
        except Exception as e:
            self.hide_loading()
            self.display_message(f"Error fetching plants: {e}")  # Handle API errors

    def display_message(self, message):
        """Display a simple message in the results frame."""
        # Clear existing results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        # Show the message
        label = ctk.CTkLabel(self.results_frame, text=message, font=("Arial", 14))
        label.pack(pady=20)

    def fetch_and_convert_image(self, image_url):
        """Fetch and process an image from a URL."""
        try:
            # Fetch the image from the URL
            image = Image.open(requests.get(image_url, stream=True).raw)
            image.thumbnail((300, 300))  # Resize for layout
            return ImageTk.PhotoImage(image)  # Convert to Tkinter-compatible format
        except Exception as e:
            print(f"Error fetching image: {e}")  # Handle errors
            return None

    def display_plants(self, plants):
        """Display plant details and images in the results frame."""
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Loop through the list of plants and display each
        for idx, plant in enumerate(plants):
            # Extract plant details
            common_name = plant.get("common_name", "Unknown Plant")
            scientific_name = plant.get("scientific_name", "Unknown Scientific Name")
            family = plant.get("family", "Unknown Family")
            genus = plant.get("genus", "Unknown Genus")
            year = plant.get("year", "Unknown Year")
            bibliography = plant.get("bibliography", "No Bibliography")
            image_url = plant.get("image_url")

            # Create a frame for each plant entry
            plant_frame = ctk.CTkFrame(self.results_frame, corner_radius=8)
            plant_frame.pack(fill="x", padx=10, pady=5)  # Layout for the plant frame

            # Text label for plant details
            plant_info = (f"Common Name: {common_name}\nScientific Name: {scientific_name}\n"
                          f"Family: {family}\nGenus: {genus}\nYear: {year}\nBibliography: {bibliography}")
            text_label = ctk.CTkLabel(plant_frame, text=plant_info, justify="left", anchor="w", font=("Arial", 12))
            text_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            # Image label for plant photo
            if image_url:
                img_label = ctk.CTkLabel(plant_frame, text="")
                img_label.grid(row=0, column=1, padx=10, pady=10, sticky="e")

                img = self.fetch_and_convert_image(image_url)  # Fetch and prepare the image
                if img:
                    img_label.configure(image=img)  # Set the image in the label
                    img_label.image = img  # Prevent garbage collection of the image
                else:
                    img_label.configure(text="Image not available")  # Fallback if image fetch fails


# Run the app
if __name__ == "__main__":
    app = PlantPalApp()  # Initialize the app
    app.mainloop()  # Start the app's main loop
