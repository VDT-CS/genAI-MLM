import threading
import serial

class SerialListener:
    def __init__(self, callbacks):
        self.callbacks = callbacks
        self.shutdown_event = threading.Event()
        self.thread = threading.Thread(target=self.read_serial_port)
        self.thread.start()
    
    def read_serial_port(self):
        try:
            ser = serial.Serial('COM3', 115200, timeout=1)  # Using a timeout
            while not self.shutdown_event.is_set():
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').rstrip()
                    if line in self.callbacks:
                        self.callbacks[line]()
        finally:
            ser.close()

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