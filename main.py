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
            "PHOTO": lambda: onInput.add_string_to_append_dict("STYLE", "Rendered in a photo-realistic style akin to high-resolution imagery captured with a Canon 5D Mark IV camera"),
            "DIGITAL_ART": lambda: onInput.add_string_to_append_dict("STYLE","Crafted in a digital art format, with intricate 3D modeling elements, reminiscent of works found on Deviant Art"),
            "ANIME": lambda: onInput.add_string_to_append_dict("STYLE", "Illustrated in an anime style, featuring manga influences, detailed pencil strokes, and Japanese-style drawing techniques, including cross-hatching for texture")
        },
        "BACKGROUND":{
            "NONE": lambda: onInput.add_string_to_append_dict("BACKGROUND", "The scene is set against a white, monotone background, emphasizing simplicity and focus on the subject"),
            "CITY": lambda: onInput.add_string_to_append_dict("BACKGROUND","A sprawling cityscape serves as the backdrop, with an urban setting illuminated by city lights and towering skyscrapers"),
            "FOREST": lambda: onInput.add_string_to_append_dict("BACKGROUND","The setting is a living forest, teeming with lush greenery, diverse wildlife, and the untouched beauty of a natural environment")
        },
        "TIME": {
            "CURRENT": lambda: onInput.add_string_to_append_dict("TIME", "The depiction is grounded in the current time period, reflecting modern-day aesthetics and sensibilities"),
            "FUTURE": lambda: onInput.add_string_to_append_dict("TIME", "Envisioned in a futuristic time period, showcasing advanced technology, speculative design, and a forward-thinking ethos"),
            "PAST": lambda: onInput.add_string_to_append_dict("TIME", "Set against a historical backdrop, evoking the ambiance and characteristics of a bygone era")
        },
        "TONE":{
            "NONE": lambda: onInput.add_string_to_append_dict("TONE", "The piece carries a neutral tone, without a specific thematic emphasis"),
            "CRITICAL": lambda: onInput.add_string_to_append_dict("TONE", "Conveyed with a serious and critical tone, incorporating dark themes and a profound sense of introspection"),
            "CARING": lambda: onInput.add_string_to_append_dict("TONE", "Infused with a caring and nurturing tone, radiating positive themes and a comforting atmosphere"),
            "WHIMSICAL": lambda: onInput.add_string_to_append_dict("TONE", "Characterized by whimsical and playful elements, creating a light-hearted and joyous theme")
        }
    }

    root.after(100, lambda: initialize_serial_listener(arduino_callbacks))
    root.protocol("WM_DELETE_WINDOW", lambda: set_shutdown_procedure(root, gui))
    
    root.mainloop()
    print("Mainloop has exited")

