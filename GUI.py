import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

class ClipDropApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ClipDrop Sketch-to-Image")
        self.geometry("800x600")

        self.canvas = tk.Canvas(self) # Create a canvas to display the sketch
        self.canvas.pack(fill=tk.BOTH, expand=True) # Fill the entire window

        self.upload_btn = tk.Button(self, text="Upload Sketch", command=self.upload_file) # Create a button to upload a sketch
        self.upload_btn.pack() # Pack the button into the window

        self.prompt_entry = tk.Entry(self, width=50) # Create an entry to enter a prompt
        self.prompt_entry.pack() # Pack the entry into the window
        self.prompt_entry.insert(0, "Enter prompt here") # Set the default text of the entry

        self.save_btn = tk.Button(self, text="Save Image", command=self.save_image, state=tk.DISABLED)
        self.save_btn.pack()

        self.send_btn = tk.Button(self, text="Send to ClipDrop", command=self.send_to_clipdrop) # Create a button to send the sketch to ClipDrop
        self.send_btn.pack() # Pack the button into the window

    def upload_file(self): # Called when the upload button is clicked
        self.file_path = filedialog.askopenfilename() # Open a file dialog to select a file
        if self.file_path: # Check if a file was selected
            self.sketch_image = Image.open(self.file_path) # Open the image
            self.sketch_photo = ImageTk.PhotoImage(self.sketch_image) # Convert the image to a PhotoImage
            self.canvas.create_image(400, 300, image=self.sketch_photo) # Display the image in the canvas

    def send_to_clipdrop(self): # Called when the send button is clicked
        prompt = self.prompt_entry.get() # Get the text from the entry
        if self.file_path and prompt: # Check if a file and prompt were entered
            with open(self.file_path, 'rb') as sketch_file_object: # Open the file
                r = requests.post( # Send the file to ClipDrop
                    'https://clipdrop-api.co/sketch-to-image/v1/sketch-to-image', # URL
                    files={'sketch_file': (self.file_path, sketch_file_object, 'image/jpeg')},# File
                    data={'prompt': prompt}, # Prompt
                    headers={'x-api-key': api_key} # API key
                )
                if r.ok:
                    self.generated_image = Image.open(BytesIO(r.content))  # Store the generated image
                    self.display_image(self.generated_image)  # Pass the image object to display_image
                else:
                    r.raise_for_status()

    def display_image(self, image):
        self.generated_photo = ImageTk.PhotoImage(image)
        self.canvas.delete("all")  # Clear the canvas
        if self.sketch_photo:  # Ensure a sketch was uploaded
            self.canvas.create_image(400, 400, image=self.sketch_photo)  # Display original sketch
        self.canvas.create_image(1200, 400, image=self.generated_photo)  # Display generated image
        self.save_btn.config(state=tk.NORMAL)  # Enable the Save button


    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            self.generated_image.save(file_path)

if __name__ == "__main__": # Check if the file was run directly
    app = ClipDropApp() # Create the app
    app.mainloop() # Run the app
