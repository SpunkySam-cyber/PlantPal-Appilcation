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
        pil_image = Image.open(file_path)  # Open the image using PIL
        pil_image = pil_image.resize((1200, 800))  # Resize to fit the window size
        background_photo = ctk.CTkImage(pil_image, size=(1600, 800))  # Create CTkImage object
        background_label = ctk.CTkLabel(frame, image=background_photo,
                                        text="")  # Create label with the background image
        background_label.place(relwidth=1, relheight=1)  # Place label to cover the frame
        return background_label

    except Exception as e:
        print(f"Error loading image: {e}")
        return None


# Update to make frame smaller and adjust its transparency
class Homepage(ctk.CTkFrame):
    def __init__(self, master, switch_page_callback):
        super().__init__(master)
        self.switch_page_callback = switch_page_callback

        # Add a full-page frame with a transparent background
        self.content_frame = ctk.CTkFrame(self, fg_color="#90EE90")
        self.content_frame.pack(fill="both", expand=True)

        # Load and set the background image for the homepage
        load_background_image(file_path="assets/bg.jpg", frame=self.content_frame)

        # Welcome Label
        self.welcome_label = ctk.CTkLabel(
            self.content_frame,
            text="🌱 Welcome to Plant Pal 🌱",
            font=("Arial", 32, "bold"),
            text_color="#0B3D26"  # Deep green
        )
        self.welcome_label.pack(pady=(30, 10))
        # Button Frame for consistent alignment (reduced height)
        self.button_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="#90EE90",
            corner_radius=20,
            width=600,
            height=350  # Reduced height for more visible background
        )
        self.button_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

        # Shared button styles
        button_style = {
            "font": ("Arial", 20, "bold"),
            "height": 50,
            "width": 300,
            "corner_radius": 15,
            "border_width": 2,
            "border_color": "#0B3D26",  # Dark green border
            "fg_color": "#FFFFFF",  # White
            "text_color": "#0B3D26",  # Dark green text
            "hover_color": "#52796F",  # Darker green on hover
        }

        # Buttons
        self.new_plant_button = ctk.CTkButton(
            self.button_frame,
            text="🌿 Add A New Plant",
            command=self.switch_to_new_plant,
            **button_style
        )
        self.new_plant_button.pack(pady=10)

        self.health_checkup_button = ctk.CTkButton(
            self.button_frame,
            text="🩺 Health Checkup",
            command=self.switch_to_health_checkup,
            **button_style
        )
        self.health_checkup_button.pack(pady=10)

        self.search_button = ctk.CTkButton(
            self.button_frame,
            text="🔍 Plant Lookup",
            command=self.switch_to_search_page,
            **button_style
        )
        self.search_button.pack(pady=10)

    def switch_to_health_checkup(self):
        from gui.components.health_checkup import HealthCheckupPage
        self.switch_page_callback(HealthCheckupPage)

    def switch_to_new_plant(self):
        from gui.components.new_plant import NewPlantPage
        self.switch_page_callback(NewPlantPage)

    def switch_to_search_page(self):
        from gui.components.search_page import SearchPage
        self.switch_page_callback(SearchPage)
