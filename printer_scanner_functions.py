# Currently, this file holds all the functions for interacting with the printer, the scanner, and the Replicate API. Should be broken up further.

import os
import win32ui
import win32com.client
from PIL import Image, ImageWin

class Scanner_Printer:
    
    def __init__(self):
        self.physical_width = 110
        self.physical_height = 111

    def print_image(self, image_path, printer_name): # For us, printer name is "HP ENVY 4520 series"
        printer_name = printer_name
        file_name = image_path

        hDC = win32ui.CreateDC ()
        hDC.CreatePrinterDC (printer_name)
        printer_size = hDC.GetDeviceCaps (self.physical_width), hDC.GetDeviceCaps (self.physical_height)

        bmp = Image.open (file_name)
        #if bmp.size[0] < bmp.size[1]:
        #   bmp = bmp.rotate (90)

        hDC.StartDoc (file_name)
        hDC.StartPage ()

        dib = ImageWin.Dib (bmp)
        dib.draw (hDC.GetHandleOutput (), (0,0,printer_size[0],printer_size[1]))

        hDC.EndPage ()
        hDC.EndDoc ()
        hDC.DeleteDC ()

    def scan_image(self, output_path):
        # Create a WIA object
        wia = win32com.client.Dispatch("WIA.DeviceManager")
        
        # Get the first scanner
        dev = None
        for info in wia.DeviceInfos:
            # Check if the device type is a scanner (Type 1)
            if info.Type == 1:  # 1 indicates a scanner
                dev = info.Connect()
                break  # Break after connecting to the first scanner

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
        
    if __name__ == "__main__":
        scan_image("test_image.jpg")