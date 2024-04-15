import threading
import pythoncom
from dotenv import load_dotenv
import os

load_dotenv()

class Input_Handler:
    def __init__(self):
        pass
        self.prompts_to_append = {}
        self.negative_prompt_to_append = {}
        self.shutdown_event = threading.Event()
        self.active_threads = set()
        self.lock = threading.Lock()

        self.printer_name = os.getenv('PRINTER_NAME')
    
    def perform_scan(self, output_path, scanner_printer, gui):
        if self.shutdown_event.is_set():
            return
        gui.start_loading_animation()
        t = threading.Thread(target=self.threadedScan, args=(output_path, scanner_printer, gui))
        t.start()
        self.thread_start(t)

    def threadedScan(self, output_path, scanner_printer, gui):
        thread_id = threading.get_ident()
        pythoncom.CoInitialize()
        try:
            scanner_printer.scan_image(output_path)
            # Schedule GUI updates to be executed on the main thread
            gui.root.after(0, lambda: setattr(gui, 'has_scanned', True))
            gui.root.after(0, gui.stop_loading_animation)
            gui.root.after(0, lambda: gui.update_scanned_image(output_path))
        finally:
            print("Scan complete.")
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
        pythoncom.CoInitialize()
        try:
            print("Sending image to replicate...")
            image_path = replicate.download_image(replicate.generate(file_path, prompt, negative_prompt), "generated_image.jpg")
            scanner_printer.print_image(image_path, self.printer_name)
            gui.root.after(0, gui.stop_loading_animation)
        finally:
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
        self.current_str_append = ""
        for input in append_from_dict:
            self.current_str_append = self.current_str_append + "; " + append_from_dict[input]
        print(self.current_str_append)
        return self.current_str_append
    
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
    