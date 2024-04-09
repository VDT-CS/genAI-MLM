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
            "PHOTO": lambda: onInput.add_string_to_append_dict("STYLE", "Photo realistic, Canon 5D Mark IV"),
            "DIGITAL_ART": lambda: onInput.add_string_to_append_dict("STYLE","Digital Art, 3D modeling"),
            "ANIME": lambda: onInput.add_string_to_append_dict("STYLE", "Anime, Manga")
        },
        "BACKGROUND":{
            "WHITE": lambda: onInput.add_string_to_append_dict("BACKGROUND", "White, monotone background"),
            "CITY": lambda: onInput.add_string_to_append_dict("BACKGROUND","Sprawling cityscape, urban setting, city lights, skyscrapers"),
            "FOREST": lambda: onInput.add_string_to_append_dict("BACKGROUND","Living forest, lush greenery, wildlife, natural setting")
        },
        "TIME": {
            "CURRENT": lambda: onInput.add_string_to_append_dict("TIME", "Current time period"),
            "FUTURE": lambda: onInput.add_string_to_append_dict("TIME", "Futuristic time period"),
            "PAST": lambda: onInput.add_string_to_append_dict("TIME", "Historical time period")
        }
    }

    root.after(100, lambda: initialize_serial_listener(arduino_callbacks, root))
    
    root.mainloop()
    print("Mainloop has exited")

