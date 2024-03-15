import os
import win32com.client

def scan_image(output_path):
    # Create a WIA object
    wia = win32com.client.Dispatch("WIA.DeviceManager")
    
    # Get the first scanner
    dev = None
    for info in wia.DeviceInfos:
        for prop in info.Properties:
            if prop.Name == "Name":
                if "scanner" in prop.Value.lower():
                    dev = info.Connect()
                    break
        if dev is not None:
            break

    if dev is None:
        print("No scanner found")
        return

    # Scan an image
    img = dev.Items[1].Transfer()
    
    # Delete the existing file if it exists
    if os.path.exists(output_path):
        os.remove(output_path)
    
    # Save the image
    img.SaveFile(output_path)

# Specify the output file
output_path = "scanned_image.jpg"

# Scan the image
scan_image(output_path)