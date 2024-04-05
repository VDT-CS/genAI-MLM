from gui import ImageGeneratorGUI
from printer_scanner_functions import ScannerPrinter
from replicate_communication import Replicate
from handleInput import InputHandler
from arduinoInput import SerialListener
import tkinter as tk

arduinoInput = None

####  These should be moved to keyboardInput.py ####
def toggle_fullscreen(root):
    root.attributes('-fullscreen', not root.attributes('-fullscreen'))
    return "break"

def end_fullscreen(root):
    root.attributes('-fullscreen', False)
    return "break"
####################################################

def initialize_serial_listener():
    global arduinoInput
    arduinoInput = SerialListener({
        "SCAN": lambda: onInput.perform_scan("scanned_image.jpg", scanner_printer, gui),
        "GENERATE": lambda: onInput.send_to_replicate("scanned_image.jpg", replicate, gui, scanner_printer),
        "POT1": lambda: print("Potentiometer 1 value received."), #Instead of this, we should call a function that appends a string to the prompt entry
        "POT2": lambda: print("Potentiometer 2 value received."),
        "POT3": lambda: print("Potentiometer 3 value received.")
    })

def on_closing():
    print("Application closing...")
    if arduinoInput is not None:
        arduinoInput.shutdown()
    else :
        print("arduinoInput is None")
    root.destroy()


if __name__ == "__main__":
    api_key = "REPLICATE_API_KEY"

    replicate = Replicate(api_key)
    scanner_printer = ScannerPrinter()
    onInput = InputHandler()

    root = tk.Tk()  # Create the root window
    gui = ImageGeneratorGUI(root,
                            lambda event: toggle_fullscreen(root), 
                            lambda event: end_fullscreen(root),
                            lambda: onInput.perform_scan("scanned_image.jpg", scanner_printer, gui),
                            lambda: onInput.send_to_replicate("scanned_image.jpg", replicate, gui, scanner_printer),
                            "GuiMode"
                            )

    # Schedule SerialListener initialization
    root.after(100, initialize_serial_listener)
    
    # Setup graceful shutdown
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()
