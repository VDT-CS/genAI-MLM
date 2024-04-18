import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import glob

# This class is responsible for the GUI of the Image Generator
class Image_Generator_GUI: 

    has_scanned = False

    def __init__(self, root,
                 gui_mode = None,
                 input_callbacks = None,
                 scan_callback = None,
                 send_to_replicate_callback = None,
                 ):
        
        large_font = ('Verdana', 20)
        
        self.root = root
        self.input_callbacks = input_callbacks

        root.title("Image Generator")
        
        self.window_size = "1024x600"
        root.geometry(self.window_size)
        
        root.attributes('-fullscreen', True)  # Start in fullscreen mode

        # Bind the toggle_fullscreen and end_fullscreen methods to F11 and Esc keys
        root.bind('<F11>', self.toggle_fullscreen)
        root.bind('<Escape>', self.end_fullscreen)

        # Create an empty frame at the top to reserve space
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Create the temporary message label within the top frame but don't display it yet
        self.temp_message_label = tk.Label(self.top_frame, bg="yellow", fg="black", text="")
        # No need to pack it now; it will be packed within the frame when needed

        # Image display label at the top
        self.image_label = tk.Label(root)
        self.image_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Prompt entry across the full width below the image
        self.image_label = tk.Label(root)
        self.image_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        root.bind('<Configure>', self.on_window_resize)  # Bind resize event
        self.current_image_path = None
        self.resize_event_id = None
        # Capture initial dimensions once the window is stable
        root.after(100, self.capture_initial_dimensions)

        if not gui_mode == "gui_mode":
            self.root.bind("<FocusOut>", self.force_focus)

        if gui_mode == "gui_mode":
            if not scan_callback or not send_to_replicate_callback or not self.input_callbacks:
                raise ValueError("scan_callback and send_to_replicate_callback must be provided when gui_mode is set")

            self.dropdown_frame = tk.Frame(root)
            self.dropdown_frame.pack(side=tk.TOP, fill=tk.X)

            self.setup_dropdown_menus()

        # Frame for buttons at the bottom
            self.button_frame = tk.Frame(root)
            self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

            # Buttons within the frame
            self.scan_button = tk.Button(self.button_frame, text="Scan Image", command=scan_callback, font=large_font)
            self.scan_button.pack(side=tk.LEFT, padx=5, pady=5)

            self.send_button = tk.Button(self.button_frame, text="Generate Image", command=send_to_replicate_callback, font=large_font)
            self.send_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.loading_frames_paths = sorted(glob.glob('gfx/loading/*.png'))
        self.loading_frames = [ImageTk.PhotoImage(Image.open(frame_path)) for frame_path in self.loading_frames_paths]
        self.loading_label = tk.Label(self.image_label)  # Assuming image_label is where you want the animation
        self.loading_index = 0
        self.loading = False

    def force_focus(self, event=None):
        """Force the focus to stay on the prompt entry."""
        self.prompt_entry.focus_set()

    def setup_dropdown_menus(self):
        for category, actions in self.input_callbacks.items():
            if isinstance(actions, dict):  # Check if the category has sub-options
                # Create a label for the dropdown
                label_text = f"{category.capitalize()}:"
                category_label = tk.Label(self.dropdown_frame, text=label_text, font=('Verdana', 12))
                category_label.pack(side=tk.LEFT, padx=(10, 0))

                # Create the dropdown menu
                var = tk.StringVar(self.root)
                var.set(f"Choose {category}")
                menu = tk.OptionMenu(self.dropdown_frame, var, *actions.keys(), command=self.get_option_command(actions, var))
                menu.pack(side=tk.LEFT, padx=(0, 20))  # Tighten spacing on left and add space on right


    def get_option_command(self, options, var):
        def command(selected_option):
            callback = options[selected_option]
            callback()
        return command
        
    def toggle_fullscreen(self, event=None):
        is_fullscreen = self.root.attributes('-fullscreen')
        if is_fullscreen:
            # If currently fullscreen, turn off fullscreen and set window to default size
            self.root.attributes('-fullscreen', False)
            self.root.geometry(self.window_size)  # Revert to default size when exiting fullscreen
        else:
            # Turn on fullscreen
            self.root.attributes('-fullscreen', True)
        return "break"

    def end_fullscreen(self, event=None):
        # Specifically for exiting fullscreen with the Esc key
        self.root.attributes('-fullscreen', False)
        self.root.geometry(self.window_size)  # Revert to default size when exiting fullscreen
        return "break"
    
    def update_scanned_image(self, image_path):
        self.display_image(image_path)

    def start_loading_animation(self):
        self.loading = True
        self.loading_index = 0
        self.animate_loading()
        self.place_loading_animation()  # Ensure it starts in the correct position

    def stop_loading_animation(self):
        self.loading = False
        self.loading_label.place_forget()  # Hide the loading label when not in use

    def animate_loading(self):
        if self.loading:
            frame = self.loading_frames[self.loading_index]
            self.loading_label.config(image=frame)
            self.loading_label.image = frame  # Keep a reference
            # Continuously update position to keep centered
            self.loading_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.loading_index = (self.loading_index + 1) % len(self.loading_frames)
            self.root.after(66, self.animate_loading)  # Schedule next frame

    def display_image(self, image_path):
        self.current_image_path = image_path  # Keep track of the current image
        img = Image.open(image_path)
        img = img.rotate(90, expand=True)  # Rotate image if needed

        # Fetch current window dimensions instead of widget dimensions
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height() - 100  # Adjust height for any other UI elements

        # Calculate the new size maintaining aspect ratio
        img_width, img_height = img.size
        ratio = min(window_width / img_width, window_height / img_height)
        new_size = (int(img_width * ratio), int(img_height * ratio))

        img = img.resize(new_size, Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        # Configure label to display image
        self.image_label.configure(image=img_tk)
        self.image_label.image = img_tk  # Store a reference to prevent garbage-collection

        print(f"Updated image size to: {new_size} based on window size: {window_width}x{window_height}")

    def capture_initial_dimensions(self):
        self.initial_width = self.root.winfo_width()
        self.initial_height = self.root.winfo_height()
        print(f"Initial window dimensions: {self.initial_width}x{self.initial_height}")
    
    def on_window_resize(self, event):
        if self.current_image_path:
            if self.resize_event_id:
                self.root.after_cancel(self.resize_event_id)
            self.resize_event_id = self.root.after(500, self.refresh_ui)
        
    def refresh_ui(self):
        self.display_image(self.current_image_path)
        if self.loading:
            self.place_loading_animation()  # Ensure the correct placement is maintained

    def place_loading_animation(self):
        # Adjust the loading label's position to always be at the center of the window
        self.loading_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    def show_error(self, title, message):
        messagebox.showerror(title, message)
        
    def show_temporary_message(self, message):
        # Now, pack the temporary message label within the top frame when needed
        self.temp_message_label.config(text=message)
        self.temp_message_label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    def hide_temporary_message(self):
        # Use pack_forget to remove the label from the top frame, hiding it
        self.temp_message_label.pack_forget()