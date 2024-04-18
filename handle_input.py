import threading
from dotenv import load_dotenv
import shutil
import os
import sys

load_dotenv()

class Input_Handler:
    def __init__(self):
        self.prompts_to_append = {}
        self.negative_prompt_to_append = {}
        self.shutdown_event = threading.Event()
        self.active_threads = set()
        self.lock = threading.Lock()
        self.scanning = False

        self.printer_name = os.getenv('PRINTER_NAME')
    
    def perform_scan(self, output_path, scanner_printer, gui):
        if self.shutdown_event.is_set():
            return
        
        gui.start_loading_animation()

        temp_output_path = "new_scan.jpg"

        # Start the scanning process in a new thread
        t = threading.Thread(target=self.threadedScan, args=(temp_output_path, output_path, scanner_printer, gui))
        t.start()
        self.thread_start(t)


    def threadedScan(self,temp_output_path, final_output_path, scanner_printer, gui):
        thread_id = threading.get_ident()
        if sys.platform == 'win32':
            import pythoncom
            pythoncom.CoInitialize()
        try:
            scanner_printer.scan_image(temp_output_path)

            self.move_old_scan(final_output_path)
            shutil.move(temp_output_path, final_output_path)

            # Schedule GUI updates to be executed on the main thread
            gui.root.after(0, lambda: setattr(gui, 'has_scanned', True))
            gui.root.after(0, gui.stop_loading_animation)
            gui.root.after(0, lambda: gui.update_scanned_image(final_output_path))
        finally:
            print("Scan complete.")
            if sys.platform == 'win32':
                pythoncom.CoUninitialize()
            self.thread_end(thread_id)

    def send_to_replicate(self, input_path, replicate, gui, scanner_printer):
        if not gui.has_scanned or self.shutdown_event.is_set():
            gui.root.after(0, lambda: gui.show_error("Error", "Please scan an image first."))
            return
        prompt = gui.prompt_entry.get() + self.append_strings(self.prompts_to_append)
        negative_prompt = self.append_strings(self.negative_prompt_to_append)
        gui.start_loading_animation()
        t = threading.Thread(target=self.send_to_replicate_thread, args=(input_path, prompt, negative_prompt, replicate, gui, scanner_printer))
        t.start()
        self.thread_start(t)
        
    def send_to_replicate_thread(self, file_path, prompt, negative_prompt, replicate, gui, scanner_printer):
        thread_id = threading.get_ident()
        if sys.platform == 'win32':
            import pythoncom
            pythoncom.CoInitialize()
        try:
            print("Sending image to replicate...")
            image_path = replicate.download_image(replicate.generate(file_path, prompt, negative_prompt), "generated_image.jpg")
            scanner_printer.print_image(image_path, self.printer_name)
            gui.root.after(0, gui.stop_loading_animation)
        finally:
            if sys.platform == 'win32':
                pythoncom.CoUninitialize()
            self.thread_end(thread_id)
            
    def add_string_to_append_dict(self, input, strToAppend, negative_prompt = ""):
        self.prompts_to_append[input] = strToAppend
        if negative_prompt != "":
            self.negative_prompt_to_append[input] = negative_prompt
        else:
            # Remove the entry from the dictionary if negative_prompt is empty
            if input in self.negative_prompt_to_append:
                del self.negative_prompt_to_append[input]

    def append_strings(self, append_from_dict):
        current_str_append = ""
        for input in append_from_dict:
            current_str_append = current_str_append + "; " + append_from_dict[input]
        print(current_str_append)
        return current_str_append
    
    def shutdown(self):
        print("Shutting down Input_Handler...")
        if any(thread.is_alive() for thread in self.active_threads):
            self.shutdown_event.set()
        else:
            print("Input_Handler shutdown complete.")
        
    def thread_start(self, thread):
        with self.lock:
            self.active_threads.add(thread)

    def thread_end(self, thread_id):
        with self.lock:
            for thread in list(self.active_threads):
                if thread.ident == thread_id:
                    self.active_threads.remove(thread)
                    break
        
    def is_active(self):
        return any(thread.is_alive() for thread in self.active_threads)

    def move_old_scan(self, output_path):
        # Check if the output file already exists
        if os.path.exists(output_path):
            # Define the directory to move existing scans
            previous_scans_dir = 'previous_scans'
            
            # Create the directory if it does not exist
            if not os.path.exists(previous_scans_dir):
                os.makedirs(previous_scans_dir)
            
            # Create a new file name by incrementing numbers
            new_path = self.create_incremented_filepath(previous_scans_dir, output_path)
            
            # Move the file to the new location
            shutil.move(output_path, new_path)

    def create_incremented_filepath(self, directory, original_path):
        base_name = os.path.basename(original_path)
        name, ext = os.path.splitext(base_name)
        i = 1
        new_name = f"{name}_{i}{ext}"
        new_path = os.path.join(directory, new_name)
        
        # Increment the number in the filename until a new unique name is found
        while os.path.exists(new_path):
            i += 1
            new_name = f"{name}_{i}{ext}"
            new_path = os.path.join(directory, new_name)
        
        return new_path
    