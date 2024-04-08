import threading
import pythoncom

class InputHandler:
    def __init__(self):
        pass
        self.current_str_append = ""
    
    def perform_scan(self, outputPath, scannerPrinter, gui):
        gui.start_loading_animation()  # Start loading animation
        print("Scanning image...")
        threading.Thread(target=self.threadedScan, args=(outputPath, scannerPrinter, gui)).start()

    def threadedScan(self, outputPath, scannerPrinter, gui):
        pythoncom.CoInitialize()  # Initialize COM library in the current thread
        try:
            scannerPrinter.scan_image(outputPath)
            # Schedule all GUI updates to be executed on the main thread
            gui.root.after(0, lambda: setattr(gui, 'has_scanned', True))
            gui.root.after(0, gui.stop_loading_animation)
            gui.root.after(0, lambda: gui.update_scanned_image(outputPath))
        finally:
            pythoncom.CoUninitialize()  # Uninitialize COM library in the current thread

    def send_to_replicate(self, inputPath, replicate, gui, scannerPrinter):
        if not gui.has_scanned:
            # Ensure GUI updates from threads are scheduled on the main thread
            gui.root.after(0, lambda: gui.show_error("Error", "Please scan an image first."))
            return
        else:
            prompt = gui.prompt_entry.get()
            prompt = prompt + self.current_str_append
            gui.start_loading_animation()  # Start loading animation
            threading.Thread(target=self.send_to_replicate_thread, args=(inputPath, prompt, replicate, gui, scannerPrinter)).start()
        
    def send_to_replicate_thread(self, file_path, prompt, replicate, gui, scannerPrinter):
        pythoncom.CoInitialize()
        try:
            print("Sending image to replicate...")
            image_path = replicate.download_image(replicate.generate(file_path, prompt), "generated_image.jpg")
            # If 'print_image' updates the GUI or triggers feedback, ensure it's done in a thread-safe manner
            scannerPrinter.print_image(image_path, "HP ENVY 5530 series")
            # Schedule GUI update to stop loading animation
            gui.root.after(0, gui.stop_loading_animation)
        finally:
            pythoncom.CoUninitialize()
            
    def append_to_prompt(self, str_append):
        self.current_str_append = ", " + str_append