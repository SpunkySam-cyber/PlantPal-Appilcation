import customtkinter as ctk
from PIL import Image


def load_background_image(file_path, frame):
    """
    Load and set the background image for the given frame.

    Args:
        file_path (str): Path to the image file.
        frame (ctk.CTkFrame): The frame to set the background image.

    Returns:
        ctk.CTkLabel: The label containing the background image, or None if failed.
    """
    try:
        pil_image = Image.open(file_path)  # Ensure this path is correct
        pil_image = pil_image.resize((900, 600))  # Resize to match the window size
        background_photo = ctk.CTkImage(dark_image=pil_image, size=(900, 600))
        background_label = ctk.CTkLabel(frame, image=background_photo, text="")
        background_label.place(relwidth=1, relheight=1)
        return background_label
    except Exception as e:
        print(f"Error loading image: {e}")
        return None


class Homepage(ctk.CTkFrame):
    """
    Homepage for the PlantPal app.
    Provides options for Health Checkup, New Plant, and Search.
    """

    def __init__(self, master, switch_page_callback):
        """
        Initialize the homepage with buttons for navigation.

        Args:
            master: The parent widget.
            switch_page_callback (callable): Function to switch between pages.
        """
        super().__init__(master)
        self.switch_page_callback = switch_page_callback

        # Add a full-page frame with light background color
        self.content_frame = ctk.CTkFrame(self, fg_color="#90EE90")  # Light green
        self.content_frame.pack(fill="both", expand=True)

        # Load and set the background image for the homepage
        load_background_image(file_path="../gui/components/plant-health.png", frame=self.content_frame)

        # Welcome Label
        self.welcome_label = ctk.CTkLabel(
            self.content_frame,
            text="🌱 Welcome to Plant Pal 🌱",
            font=("Arial", 32, "bold"),
            text_color="#0B3D26"  # Deep green
        )
        self.welcome_label.pack(pady=(10, 30))

        # Button Frame for consistent alignment
        self.button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.button_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Shared button styles for consistency
        button_style = {
            "font": ("Arial", 25, "bold"),
            "height": 70,
            "width": 400,
            "corner_radius": 20,
            'border_width': 3,
            'border_color': '#0B3D26',
            "fg_color": "#FFFFFF",  # white
            "text_color": "#0B3D26",  # dark green text
            "hover_color": "#52796F",  # Darker green on hover
        }

        # Buttons
        self.new_plant_button = ctk.CTkButton(
            self.button_frame,
            text="🌿 Add New Plant",
            command=self.switch_to_new_plant,
            **button_style
        )
        self.new_plant_button.pack(pady=20)

        self.health_checkup_button = ctk.CTkButton(
            self.button_frame,
            text="🩺 Health Checkup",
            command=self.switch_to_health_checkup,
            **button_style
        )
        self.health_checkup_button.pack(pady=20)

        self.search_button = ctk.CTkButton(
            self.button_frame,
            text="🔍 Plant Lookup",
            command=self.switch_to_search_page,
            **button_style
        )
        self.search_button.pack(pady=20)

    def switch_to_health_checkup(self):
        from gui.components.health_checkup import HealthCheckupPage
        self.switch_page_callback(HealthCheckupPage)
    def switch_to_new_plant(self):
        from gui.components.new_plant import NewPlantPage
        self.switch_page_callback(NewPlantPage)
    def switch_to_search_page(self):
        from gui.components.search_page import SearchPage
        self.switch_page_callback(SearchPage)

