import win32print
import win32com.client

def get_printer_names():
    print("Available printers:")
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
    for printer in printers:
        print(printer[2])
        
def get_scanner_names():
    print("Available scanners:")
    # Create a WIA object
    wia = win32com.client.Dispatch("WIA.DeviceManager")
    # Loop through all the devices in the WIA device manager
    for info in wia.DeviceInfos:
        # Check if the device type is a scanner
        # DeviceType 1 is a scanner
        if info.Type == 1:
            # Each DeviceInfo has a Properties collection
            for prop in info.Properties:
                # The Name property (property id 10) contains the device's name
                if prop.PropertyID == 10:
                    print(prop.Value)  # Use .Value to get the property's value

if __name__ == "__main__":
    get_printer_names()
    get_scanner_names()