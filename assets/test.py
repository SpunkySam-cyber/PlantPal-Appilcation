import tkinter as tk
from PIL import Image, ImageTk
import os

# Create the main tkinter window
root = tk.Tk()
root.title("Local Image Display")
root.geometry("600x400")  # Adjust size as needed

# Dynamically generate the absolute path to the image
relative_path = "plant-health.png"  # Replace with your relative path
absolute_path = os.path.abspath(relative_path)

try:
    # Load the image using PIL and resize it
    pil_image = Image.open(absolute_path)
    resized_image = pil_image.resize((600, 400))  # Adjust the size as needed
    tk_image = ImageTk.PhotoImage(resized_image)

    # Add the image as a background
    canvas = tk.Canvas(root, width=600, height=400)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=tk_image, anchor="nw")  # Anchor image to top-left

    # Create a frame with a semi-transparent effect
    overlay_frame = tk.Frame(root, bg="#FFFFFF", width=300, height=100)
    overlay_frame.place(relx=0.5, rely=0.1, anchor="center")  # Position the frame

    # Add text to the frame
    label = tk.Label(
        overlay_frame,
        text="Hello",

        fg="black",  # Text color
        font=("Arial", 16),
    )
    label.pack(pady=10)

except Exception as e:
    # Display error message if the image can't be loaded
    error_label = tk.Label(root, text=f"Error loading image: {e}", fg="red")
    error_label.pack(pady=20)

# Run the tkinter event loop
root.mainloop()
