from gui import ImageGeneratorGUI
from printer_scanner_functions import ScannerPrinter
from replicate_communication import Replicate
from handleInput import InputHandler
from arduinoInput import SerialListener
import tkinter as tk


def initialize_serial_listener(callbacks, root):
    arduinoInput = SerialListener(callbacks)
    root.protocol("WM_DELETE_WINDOW", lambda: set_shutdown_procedure(arduinoInput, root))
    
def set_shutdown_procedure(arduino, root):
    root.destroy()
    arduino.shutdown()

if __name__ == "__main__":
    api_key = "REPLICATE_API_KEY"

    replicate = Replicate(api_key)
    scanner_printer = ScannerPrinter()
    onInput = InputHandler()

    root = tk.Tk()  # Create the root window
    gui = ImageGeneratorGUI(root,
                            lambda: onInput.perform_scan("scanned_image.jpg", scanner_printer, gui),
                            lambda: onInput.send_to_replicate("scanned_image.jpg", replicate, gui, scanner_printer),
                            "GuiMode"
                            )
    
    arduino_callbacks = {
        "SCAN": lambda: onInput.perform_scan("scanned_image.jpg", scanner_printer, gui),
        "GENERATE": lambda: onInput.send_to_replicate("scanned_image.jpg", replicate, gui, scanner_printer),
        "STYLE": {
            "PHOTO": lambda: onInput.append_to_prompt("Photo realistic, Canon 5D Mark IV"),
            "DIGITAL_ART": lambda: onInput.append_to_prompt("Digital Art, 3D modeling"),
            "ANIME": lambda: onInput.append_to_prompt("Anime, Manga")
        }
    }

    root.after(100, lambda: initialize_serial_listener(arduino_callbacks, root))
    
    root.mainloop()
    print("Mainloop has exited")

