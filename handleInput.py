import threading
import pythoncom

class InputHandler:
    def __init__(self):
        pass
        self.stringsToAppend = {}
        self.shutdown_event = threading.Event()
        self.active_threads = set()
        self.lock = threading.Lock()
    
    def perform_scan(self, outputPath, scannerPrinter, gui):
        if self.shutdown_event.is_set():
            return
        t = threading.Thread(target=self.threadedScan, args=(outputPath, scannerPrinter, gui))
        t.start()
        self.thread_start(t)

    def threadedScan(self, outputPath, scannerPrinter, gui):
        thread_id = threading.get_ident()
        pythoncom.CoInitialize()
        try:
            scannerPrinter.scan_image(outputPath)
            # Schedule GUI updates to be executed on the main thread
            gui.root.after(0, lambda: setattr(gui, 'has_scanned', True))
            gui.root.after(0, gui.stop_loading_animation)
            gui.root.after(0, lambda: gui.update_scanned_image(outputPath))
        finally:
            print("Scan complete.")
            pythoncom.CoUninitialize()
            self.thread_end(thread_id)

    def send_to_replicate(self, inputPath, replicate, gui, scannerPrinter):
        if not gui.has_scanned or self.shutdown_event.is_set():
            gui.root.after(0, lambda: gui.show_error("Error", "Please scan an image first."))
            return
        prompt = gui.prompt_entry.get() + self.append_strings()
        gui.start_loading_animation()
        t = threading.Thread(target=self.send_to_replicate_thread, args=(inputPath, prompt, replicate, gui, scannerPrinter))
        t.start()
        self.thread_start(t)
        
    def send_to_replicate_thread(self, file_path, prompt, replicate, gui, scannerPrinter):
        thread_id = threading.get_ident()
        pythoncom.CoInitialize()
        try:
            print("Sending image to replicate...")
            image_path = replicate.download_image(replicate.generate(file_path, prompt), "generated_image.jpg")
            scannerPrinter.print_image(image_path, "HP ENVY 5530 series")
            gui.root.after(0, gui.stop_loading_animation)
        finally:
            pythoncom.CoUninitialize()
            self.thread_end(thread_id)
            
    def add_string_to_append_dict(self, input, strToAppend):
        self.stringsToAppend[input] = strToAppend

    def append_strings(self):
        self.current_str_append = ""
        for input in self.stringsToAppend:
            self.current_str_append = self.current_str_append + ", " + self.stringsToAppend[input]
        print(self.current_str_append)
        return self.current_str_append
    
    def shutdown(self):
        print("Shutting down InputHandler...")
        if any(thread.is_alive() for thread in self.active_threads):
            self.shutdown_event.set()
        else:
            print("InputHandler shutdown complete.")
        
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
    