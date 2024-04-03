import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import threading
import os
import printer_scanner_functions as psf
# Make sure to have the above provided functions in the same file or imported here


class ImageGeneratorGUI:

    has_scanned = False

    def __init__(self, root):
        self.root = root
        root.title("Image Generator")
        root.attributes('-fullscreen', True) # Start in fullscreen mode
        
        # Bind the toggle_fullscreen and end_fullscreen methods to F11 and Esc keys, respectively
        root.bind('<F11>', self.toggle_fullscreen)
        root.bind('<Escape>', self.end_fullscreen)

        # Setup of the GUI
        self.scan_button = tk.Button(root, text="Scan Image", command=self.scan_and_display)
        self.scan_button.pack()

        self.prompt_entry = tk.Entry(root)
        self.prompt_entry.pack()

        self.send_button = tk.Button(root, text="Generate Image", command=self.send_to_replicate_thread)
        self.send_button.pack()

        self.image_label = tk.Label(root)
        self.image_label.pack()

    def toggle_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))
        return "break"

    def end_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)
        return "break"

    def scan_and_display(self):
        output_path = "scanned_image.jpg"
        #start a loading animation here
        psf.scan_image(output_path)
        #and end it here
        ImageGeneratorGUI.has_scanned = True	# Set the global variable to True
        self.display_image(output_path)

    def display_image(self, image_path):
        img = Image.open(image_path)
        img = img.resize((250, 354))  # Resize for display purposes
        img = img.rotate(90, expand=True)
        img_tk = ImageTk.PhotoImage(img)
        self.image_label.configure(image=img_tk)
        self.image_label.image = img_tk

    def send_to_replicate_thread(self):
        if not ImageGeneratorGUI.has_scanned:
            messagebox.showerror("Error", "Please scan an image first.")
            return
        else:
            prompt = self.prompt_entry.get()
            file_path = "scanned_image.jpg"
            threading.Thread(target=psf.send_to_replicate, args=(file_path, prompt)).start()
            # Implement a loading animation here