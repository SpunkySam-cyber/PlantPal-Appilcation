import customtkinter as ctk
from PIL import Image
from gui.components.health_checkup import HealthCheckupPage
from gui.components.homepage import Homepage
from gui.components.new_plant import NewPlantPage
from gui.components.search_page import SearchPage



class PlantPalApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set main window properties
        self.title("Plant Pal")
        self.geometry("1000x650")
        self.iconbitmap("assets/logo-1.ico")

        # Set appearance and color theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")


        # Initialize container for all pages
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        # Show homepage by default
        self.show_page(Homepage)

    def show_page(self, page_class, *args, **kwargs):
        """
        A generic method to display a page.

        Args:
            page_class: The class of the page to display.
            *args, **kwargs: Additional arguments to pass to the page.
        """
        # Clear the current page
        for widget in self.container.winfo_children():
            widget.destroy()

        # Pass the show_page method itself as the switch_page_callback
        kwargs["switch_page_callback"] = self.show_page

        # Create the new page and display it
        page = page_class(self.container, *args, **kwargs)
        page.pack(fill="both", expand=True)


# Run the app
if __name__ == "__main__":
    app = PlantPalApp()
    app.mainloop()
