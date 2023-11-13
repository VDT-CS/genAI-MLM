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
        self.geometry("1100x1100")

        self.canvas = tk.Canvas(self)  # Create a canvas to display the sketch
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Fill the entire window

        self.upload_btn = tk.Button(self, text="Upload Sketch", command=self.upload_file) # Create a button to upload a sketch
        self.upload_btn.pack() # Pack the button into the window

        self.prompt_entry = tk.Entry(self, width=50) # Create an entry to enter a prompt
        self.prompt_entry.pack() # Pack the entry into the window
        self.prompt_entry.insert(0, "Enter prompt here") # Set the default text of the entry

        self.send_btn = tk.Button(self, text="Send to ClipDrop", command=self.send_to_clipdrop, state=tk.DISABLED)  # Disable the button initially
        self.send_btn.pack()  # Pack the button into the window

        self.bind('<Configure>', self.update_canvas)  # Bind the function to the window resize event

    def upload_file(self):  # Called when the upload button is clicked
        self.file_path = filedialog.askopenfilename()  # Open a file dialog to select a file
        if self.file_path:  # Check if a file was selected
            self.current_image = Image.open(self.file_path)  # Open the image
            self.update_canvas(None)  # Update the canvas
            self.send_btn.config(state=tk.NORMAL)  # Enable the Send to ClipDrop button

    def send_to_clipdrop(self):  # Called when the send button is clicked
        prompt = self.prompt_entry.get()  # Get the text from the entry
        if self.file_path and prompt:  # Check if a file and prompt were entered
            with open(self.file_path, 'rb') as sketch_file_object:  # Open the file
                r = requests.post( # Send the file to ClipDrop
                    'https://clipdrop-api.co/sketch-to-image/v1/sketch-to-image', # URL
                    files={'sketch_file': (self.file_path, sketch_file_object, 'image/jpeg')},# File
                    data={'prompt': prompt}, # Prompt
                    headers={'x-api-key': api_key} # API key
                )
                if r.ok: # Check if the request was successful
                    self.display_image(r.content) # Display the image
                else:
                    r.raise_for_status() # Raise an exception if the request failed

    def display_image(self, image_data):  # Display an image in the canvas
        self.current_image = Image.open(BytesIO(image_data))  # Open the image
        self.update_canvas(None)  # Update the canvas

    def display_image(self, image_data):  # Display an image in the canvas
        self.current_image = Image.open(BytesIO(image_data))  # Open the image
        self.update_canvas(None)  # Update the canvas
    
    def update_canvas(self, event):  # Update the canvas
        if hasattr(self, 'current_image'):
            # Get the dimensions of the canvas and the image
            canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()
            image_width, image_height = self.current_image.size

            # Calculate the scaling factor while maintaining the aspect ratio
            scale = min((canvas_width - 20) / image_width, (canvas_height - 20) / image_height)
            new_width, new_height = int(image_width * scale), int(image_height * scale)

            # Resize the image and create a PhotoImage object
            resized_image = self.current_image.resize((new_width, new_height), Image.LANCZOS)  # Corrected line
            photo = ImageTk.PhotoImage(resized_image)

            # Clear the canvas and display the image
            self.canvas.delete("all")
            self.canvas.create_image(canvas_width // 2, canvas_height // 2, image=photo)
            self.photo = photo  # Keep a reference to avoid garbage collection

if __name__ == "__main__": # Check if the file was run directly
    app = ClipDropApp() # Create the app
    app.mainloop() # Run the app
