import tkinter as  tk # for initiliazing the root window

from gui import ImageGeneratorGUI
from printer_scanner_functions import ScannerPrinter
from replicate_communication import Replicate
from handleInput import InputHandler
from arduinoInput import SerialListener

threadsToClose = []


def initialize_serial_listener(callbacks):
    arduinoInput = SerialListener(callbacks)
    threadsToClose.append(arduinoInput)
        
def set_shutdown_procedure(root, gui):
    print("Initiating shutdown...")
    
    for thread in threadsToClose:
        thread.shutdown()

    if any(thread.is_active() for thread in threadsToClose):
        gui.show_temporary_message("An external operation is in progress. The application will close automatically once the operation is complete.")
        check_and_finalize_shutdown(root, gui)
    else:
        root.destroy()

def check_and_finalize_shutdown(root, gui):
    all_threads_closed = all(not thread.is_active() for thread in threadsToClose)
    
    if all_threads_closed:
        print("All threads closed. Exiting.")
        root.destroy()
    else:
        root.after(100, lambda: check_and_finalize_shutdown(root, gui))


if __name__ == "__main__":
    api_key = "REPLICATE_API_KEY"

    replicate = Replicate(api_key)
    scanner_printer = ScannerPrinter()
    onInput = InputHandler()
    threadsToClose.append(onInput)

    root = tk.Tk()  # Create the root window
    
    gui = ImageGeneratorGUI(root,
                            lambda: onInput.perform_scan("scanned_image.jpg", scanner_printer, gui),
                            lambda: onInput.send_to_replicate("scanned_image.jpg", replicate, gui, scanner_printer),
                            )
    
    # Callbacks for arduino input
    arduino_callbacks = {
        "SCAN": lambda: onInput.perform_scan("scanned_image.jpg", scanner_printer, gui),
        "GENERATE": lambda: onInput.send_to_replicate("scanned_image.jpg", replicate, gui, scanner_printer),
        "STYLE": {
            "PHOTO": lambda: onInput.add_string_to_append_dict("STYLE", "Rendered as a high-resolution photo by a Canon 5D Mark IV"),
            "DIGITAL_ART": lambda: onInput.add_string_to_append_dict("STYLE","In the style of Deviant Art's digital 3D art"),
            "ANIME": lambda: onInput.add_string_to_append_dict("STYLE", "Anime-inspired, with detailed pencil and cross-hatching")
        },
        "TIME": {
            "CURRENT": lambda: onInput.add_string_to_append_dict("TIME", "Set in the present days"),
            "FUTURE": lambda: onInput.add_string_to_append_dict("TIME", "Imagined in a speculative, futuristic era"),
            "PAST": lambda: onInput.add_string_to_append_dict("TIME", "Rooted in historical times")
        },
        "TONE":{
            "NONE": lambda: onInput.add_string_to_append_dict("TONE", "Neutral tone, no thematic emphasis"),
            "CRITICAL": lambda: onInput.add_string_to_append_dict("TONE", "Serious, introspective themes"),
            "CARING": lambda: onInput.add_string_to_append_dict("TONE", "Infused with a caring and nurturing tone"),
            "WHIMSICAL": lambda: onInput.add_string_to_append_dict("TONE", "Whimsical, playful, and light-hearted")
        },
        "BACKGROUND":{
            "NONE": lambda: onInput.add_string_to_append_dict("BACKGROUND", "No background", "Exclude colors, shadows, and textures in the background"),
            "CITY": lambda: onInput.add_string_to_append_dict("BACKGROUND","Background overlooking a vibrant, lit-up cityscape"),
            "FOREST": lambda: onInput.add_string_to_append_dict("BACKGROUND","Background within a lively, verdant forest")
        }
    }

    root.after(100, lambda: initialize_serial_listener(arduino_callbacks))
    root.protocol("WM_DELETE_WINDOW", lambda: set_shutdown_procedure(root, gui))
    
    root.mainloop()
    print("Mainloop has exited")

