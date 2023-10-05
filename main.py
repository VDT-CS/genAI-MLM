import requests
import os
import tkinter as tk
from tkinter import filedialog, simpledialog
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

load_dotenv()
api_key = os.getenv("API_KEY")

def select_file():
    root = tk.Tk()
    root.withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = filedialog.askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    return filename

def send_to_clipdrop(file_path, prompt='a car driving, cinematic'):
    with open(file_path, 'rb') as sketch_file_object:
        r = requests.post('https://clipdrop-api.co/sketch-to-image/v1/sketch-to-image',
            files={'sketch_file': (file_path, sketch_file_object, 'image/jpeg')},
            data={'prompt': prompt},
            headers={'x-api-key': api_key}
        )
        if r.ok:
            return r.content
        else:
            r.raise_for_status()

def display_image(image_data):
    image = Image.open(BytesIO(image_data))
    image.show()

def main():
    file_path = select_file()
    if file_path:  # check if a file was selected
        # Ask user for a prompt
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        prompt = simpledialog.askstring("Input", "Enter the prompt for ClipDrop:")
        root.destroy()  # Destroy the Tkinter root window

        if prompt:  # Check if a prompt was entered
            image_data = send_to_clipdrop(file_path, prompt)
            display_image(image_data)
        else:
            print("No prompt entered, exiting.")

if __name__ == "__main__":
    main()