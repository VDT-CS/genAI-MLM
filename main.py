import tkinter as  tk # for initiliazing the root window
import argparse

from gui import Image_Generator_GUI
from printer_scanner_functions import Scanner_Printer
from replicate_communication import Replicate
from handle_input import Input_Handler
from arduino_input import Serial_Listener

threadsToClose = []

callbacks = {
        "SCAN": lambda: on_input.perform_scan("scanned_image.jpg", scanner_printer, gui),
        "GENERATE": lambda: on_input.send_to_replicate("scanned_image.jpg", replicate, gui, scanner_printer),
        "STYLE": {
            "NONE": lambda: on_input.add_string_to_append_dict("STYLE", ""),
            "PHOTO": lambda: on_input.add_string_to_append_dict("STYLE", "Rendered as a high-resolution photo by a Canon 5D Mark IV"),
            "DIGITAL_ART": lambda: on_input.add_string_to_append_dict("STYLE","In the style of Deviant Art's digital 3D art"),
            "ANIME": lambda: on_input.add_string_to_append_dict("STYLE", "Anime-inspired, with detailed pencil and cross-hatching")
        },
        "TIME": {
            "NONE": lambda: on_input.add_string_to_append_dict("TIME", ""),
            "CURRENT": lambda: on_input.add_string_to_append_dict("TIME", "Set in the present days"),
            "FUTURE": lambda: on_input.add_string_to_append_dict("TIME", "Imagined in a speculative, futuristic era"),
            "PAST": lambda: on_input.add_string_to_append_dict("TIME", "Rooted in historical times")
        },
        "TONE":{
            "NONE": lambda: on_input.add_string_to_append_dict("TONE", ""),
            "NEUTRAL": lambda: on_input.add_string_to_append_dict("TONE", "Neutral tone, no thematic emphasis"),
            "CRITICAL": lambda: on_input.add_string_to_append_dict("TONE", "Serious, introspective themes"),
            "CARING": lambda: on_input.add_string_to_append_dict("TONE", "Infused with a caring and nurturing tone"),
            "WHIMSICAL": lambda: on_input.add_string_to_append_dict("TONE", "Whimsical, playful, and light-hearted")
        },
        "BACKGROUND":{
            "NONE": lambda: on_input.add_string_to_append_dict("BACKGROUND",""),
            "WHITE": lambda: on_input.set_remove_background(lambda: on_input.add_string_to_append_dict("BACKGROUND", "Isolated on a white background!", "Exclude colors, shadows, and textures in the background")),
            "CITY": lambda: on_input.add_string_to_append_dict("BACKGROUND","Background overlooking a vibrant, lit-up cityscape"),
            "FOREST": lambda: on_input.add_string_to_append_dict("BACKGROUND","Background within a lively, verdant forest")
        }
}

def initialize_serial_listener(callbacks):
    arduinoInput = Serial_Listener(callbacks)
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
    api_key = 'REPLICATE_API_TOKEN'

    parser = argparse.ArgumentParser(description="Control the mode of the application")
    parser.add_argument("--mode", choices=["arduino", "gui"], required=True, help="Run the program in 'arduino-mode' or 'gui-mode'")
    args = parser.parse_args()

    replicate = Replicate(api_key)
    scanner_printer = Scanner_Printer()
    on_input = Input_Handler()
    threadsToClose.append(on_input)

    root = tk.Tk()  # Create the root window

    if args.mode == "arduino":
        gui = Image_Generator_GUI(root)

        # Initialize serial listener if Arduino mode is selected
        root.after(100, lambda: initialize_serial_listener(callbacks))
    if args.mode == "gui":
        gui = Image_Generator_GUI(root,
                            "gui_mode",
                            callbacks,
                            lambda: on_input.perform_scan("scanned_image.jpg", scanner_printer, gui),
                            lambda: on_input.send_to_replicate("scanned_image.jpg", replicate, gui, scanner_printer),
                            )

    root.protocol("WM_DELETE_WINDOW", lambda: set_shutdown_procedure(root, gui))
    
    root.mainloop()
    print("Mainloop has exited")

