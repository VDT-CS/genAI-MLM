import threading
import serial
import ast

class SerialListener:
    def __init__(self, callbacks, com_port='COM3', baud_rate=115200):
        self.callbacks = callbacks
        self.shutdown_event = threading.Event()
        self.thread = threading.Thread(target=self.read_serial_port)
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.ser = None  # Serial connection placeholder
        self.thread.start()

    def read_serial_port(self):
        try:
            self.ser = serial.Serial(self.com_port, self.baud_rate, timeout=1)
            while not self.shutdown_event.is_set():
                if self.ser.in_waiting > 0:
                    raw_data = self.ser.readline().decode('utf-8').rstrip()
                    print("Raw string: " + raw_data)
                    parsed_dict = ast.literal_eval(raw_data)
                    # Ensure parsed_dict is actually a dictionary
                    if not isinstance(parsed_dict, dict):
                        print("Error: Received data is not a dictionary.")
                        continue
                    if "INPUT" in parsed_dict:
                        input_type = parsed_dict["INPUT"]
                        if input_type in self.callbacks:
                            if isinstance(self.callbacks[input_type], dict):
                                input_value = parsed_dict.get("VALUE", None)  # Safely get VALUE
                                if input_value and input_value in self.callbacks[input_type]:
                                    self.callbacks[input_type][input_value]()
                            else:
                                self.callbacks[input_type]()
        finally:
            if self.ser:
                self.ser.close()
                print("Serial port closed.")

    def shutdown(self):
        print("Shutting down SerialListener...")
        self.shutdown_event.set()
        self.thread.join()
        print("SerialListener shutdown complete.")

# for debugging purposes
if __name__ == "__main__":
    
    # Predefined callback functions
    def callback1():
        print("Callback 1 executed.")

    def callback2():
        print("Callback 2 executed.")

    # Mapping specific string values to their respective callback functions
    callbacks = {
        "SCAN": callback1,
        "GENERATE": callback2,
    }

    # Initialize SerialListener with the defined callbacks
    serial_listener = SerialListener(callbacks)

    print("Press Enter to exit...")
    input()  # Wait for user input to exit