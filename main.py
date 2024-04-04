from gui import ImageGeneratorGUI
import printer_scanner_functions as psf
import tkinter as tk

def toggle_fullscreen(root):
    root.attributes('-fullscreen', not root.attributes('-fullscreen'))
    return "break"

def end_fullscreen(root):
    root.attributes('-fullscreen', False)
    return "break"

root = tk.Tk() # Create the root window

# Adjusted to pass the root and functions properly
gui = ImageGeneratorGUI(root, lambda event: toggle_fullscreen(root), lambda event: end_fullscreen(root)) 

if __name__ == "__main__":
    root.mainloop()