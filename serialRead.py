import serial
import time

def read_serial_port():
    # Open serial port with baud rate of 115200
    # Replace 'COM3' with your serial port name
    ser = serial.Serial('COM3', 115200)
    time.sleep(2)  # Wait for the connection to be established
    
    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(line)
    except KeyboardInterrupt:
        print("Serial reading terminated by user")
    finally:
        ser.close()  # Close the serial connection