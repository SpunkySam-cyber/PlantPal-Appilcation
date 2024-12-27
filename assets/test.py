import customtkinter as ctk
from PIL import Image

# Create the customtkinter window
root = ctk.CTk()
root.title("Local Image Display")

# Path to the local image
file_path = "../gui/components/plant-health.png"  # Replace with your image file path

try:
    # Load the image using PIL and resize it
    pil_image = Image.open(file_path)
    resized_image = pil_image.resize((300, 300))  # Adjust the size as needed

    # Convert the PIL image to a CTkImage
    tk_image = ctk.CTkImage(dark_image=resized_image, size=(400, 300))

    # Label to display the image
    image_label = ctk.CTkLabel(root, image=tk_image, text="")
    image_label.pack(pady=20)

except Exception as e:
    # Display error message if the image can't be loaded
    error_label = ctk.CTkLabel(root, text=f"Error loading image: {e}", text_color="red")
    error_label.pack(pady=20)

# Run the customtkinter event loop
root.mainloop()
