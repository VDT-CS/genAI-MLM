import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os
from dotenv import load_dotenv
import replicate
import tempfile
from urllib.request import urlretrieve


load_dotenv()
api_key = os.getenv("REPLICATE_API_TOKEN")

class T2iLineartApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sketch-to-Image Machine")
        self.geometry("1100x1100")

        self.canvas = tk.Canvas(self)  # Create a canvas to display the sketch
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Fill the entire window

        self.upload_btn = tk.Button(self, text="Upload Sketch", command=self.upload_file) # Create a button to upload a sketch
        self.upload_btn.pack() # Pack the button into the window

        self.prompt_entry = tk.Entry(self, width=50) # Create an entry to enter a prompt
        self.prompt_entry.pack() # Pack the entry into the window
        self.prompt_entry.insert(0, "Enter prompt here") # Set the default text of the entry

        self.send_btn = tk.Button(self, text="Generate Image", command=self.send_to_replicate, state=tk.DISABLED)  # Disable the button initially
        self.send_btn.pack()  # Pack the button into the window

        self.bind('<Configure>', self.update_canvas)  # Bind the function to the window resize event

    def upload_file(self):  # Called when the upload button is clicked
        self.file_path = filedialog.askopenfilename()  # Open a file dialog to select a file
        if self.file_path:  # Check if a file was selected
            print("file path: ", self.file_path)  # Print the file path
            self.current_image = Image.open(self.file_path)  # Open the image
            self.update_canvas(None)  # Update the canvas
            self.send_btn.config(state=tk.NORMAL)  # Enable the Generate button

    def send_to_replicate(self):
        prompt = self.prompt_entry.get()  # Get the text from the entry
        if self.file_path and prompt:  # Check if a file and prompt were entered
            # Get the specific deployment
            deployment = replicate.deployments.get("magniswerfer/sketch-to-image-machine")

            # Send the image to Replicate and create a prediction
            with open(self.file_path, 'rb') as sketch_file_object:
                prediction = deployment.predictions.create(input={"image": sketch_file_object, "prompt": prompt})
            
            # Wait for the prediction to complete
            prediction.wait()

            # Download and display the image
            # Assuming the output is a list and the desired image is the second one
            if isinstance(prediction.output, list) and len(prediction.output) > 1:
                image_url = prediction.output[1]  # Get the URL of the second image
            else:
                print("Unexpected output format or insufficient outputs received.")
                return

            # Download and display the image
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                urlretrieve(image_url, tmp_file.name)
                self.display_image(tmp_file.name)

    def display_image(self, image_data):  # Display an image in the canvas
        self.current_image = Image.open(BytesIO(image_data))  # Open the image
        self.update_canvas(None)  # Update the canvas

    def display_image(self, image_data):
        if isinstance(image_data, str):
            # If image_data is a file path
            self.current_image = Image.open(image_data)
        else:
            # If image_data is bytes
            self.current_image = Image.open(BytesIO(image_data))

        self.update_canvas(None)
    
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
    app = T2iLineartApp() # Create the app
    app.mainloop() # Run the app
