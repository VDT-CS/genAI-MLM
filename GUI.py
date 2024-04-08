import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
import printer_scanner_functions as psf # Import the printer_scanner_functions module
import glob

# This class is responsible for the GUI of the Image Generator
class ImageGeneratorGUI:

    has_scanned = False

    def __init__(self, root, 
                 scan_callback,
                 send_to_replicate_callback,
                 guiMode = None,):
        
        self.root = root
        root.title("Image Generator")
        root.attributes('-fullscreen', True)  # Start in fullscreen mode
        
        # Bind the toggle_fullscreen and end_fullscreen methods to F11 and Esc keys, respectively
        root.bind('<F11>', self.toggle_fullscreen)
        root.bind('<Escape>', self.end_fullscreen)

        # Image display label at the top
        self.image_label = tk.Label(root)
        self.image_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Prompt entry across the full width below the image
        self.prompt_entry = tk.Entry(root)
        self.prompt_entry.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)  # Padding for aesthetics

        if guiMode == "GuiMode":
        # Frame for buttons at the bottom
            self.button_frame = tk.Frame(root)
            self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

            # Buttons within the frame
            self.scan_button = tk.Button(self.button_frame, text="Scan Image", command=scan_callback)
            self.scan_button.pack(side=tk.LEFT, padx=5, pady=5)

            self.send_button = tk.Button(self.button_frame, text="Generate Image", command=send_to_replicate_callback)
            self.send_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.loading_frames_paths = sorted(glob.glob('gfx/loading/*.png'))
        self.loading_frames = [ImageTk.PhotoImage(Image.open(frame_path)) for frame_path in self.loading_frames_paths]
        self.loading_label = tk.Label(self.image_label)  # Assuming image_label is where you want the animation
        self.loading_index = 0
        self.loading = False
        
    def toggle_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))
        return "break"

    def end_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)
        return "break"
    
    def update_scanned_image(self, image_path):
        self.display_image(image_path)

    def OLD_scan_and_display(self):
        output_path = "scanned_image.jpg"
        self.start_loading_animation()  # Start loading animation
        threading.Thread(target=self.perform_scan, args=(output_path,)).start()
        #and end it here

    def start_loading_animation(self):
        self.loading = True
        self.loading_index = 0
        self.animate_loading()

    def stop_loading_animation(self):
        self.loading = False
        self.root.after(0, self.loading_label.place_forget)  # Hide the loading label when not in use

    def animate_loading(self):
        if self.loading:
            frame = self.loading_frames[self.loading_index]
            #print(self.loading_index) #for debugging
            self.loading_label.config(image=frame)
            self.loading_label.image = frame  # Keep a reference
            self.loading_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Adjust position as needed
            self.loading_index = (self.loading_index + 1) % len(self.loading_frames)
            self.root.after(66, self.animate_loading)  # Schedule next frame

    def display_image(self, image_path):
        # Make sure the GUI is updated to ensure label dimensions are accurate
        self.root.update_idletasks()

        # Load and rotate the image
        img = Image.open(image_path)
        img = img.rotate(90, expand=True)

        # Get the dimensions of the label
        label_width = self.image_label.winfo_width()
        label_height = self.image_label.winfo_height()

        # Calculate the new size while maintaining the aspect ratio
        img_width, img_height = img.size
        ratio = min(label_width / img_width, label_height / img_height)
        new_size = (int(img_width * ratio), int(img_height * ratio))

        # Resize the image using LANCZOS (high-quality downsampling)
        img = img.resize(new_size, Image.LANCZOS)

        # Display the image
        img_tk = ImageTk.PhotoImage(img)
        self.image_label.configure(image=img_tk)
        self.image_label.image = img_tk  # Keep a reference to prevent garbage-collection
        
    def show_error(self, title, message):
        messagebox.showerror(title, message)