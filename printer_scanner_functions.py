import os
import platform
import subprocess
from PIL import Image, ImageWin

# Conditional imports depending on the OS
if platform.system() == 'Windows':
    import win32ui
    import win32com.client

class Scanner_Printer:
    
    def __init__(self):
        self.physical_width = 110
        self.physical_height = 111

    def print_image(self, image_path, printer_name):
        if platform.system() == 'Windows':
            printer_name = printer_name
            file_name = image_path

            hDC = win32ui.CreateDC ()
            hDC.CreatePrinterDC (printer_name)
            printer_size = hDC.GetDeviceCaps (self.physical_width), hDC.GetDeviceCaps (self.physical_height)

            bmp = Image.open (file_name)

            hDC.StartDoc (file_name)
            hDC.StartPage ()

            dib = ImageWin.Dib (bmp)
            dib.draw (hDC.GetHandleOutput (), (0,0,printer_size[0],printer_size[1]))

            hDC.EndPage ()
            hDC.EndDoc ()
            hDC.DeleteDC ()
        if platform.system() == 'Darwin':  # Placeholder for macOS or other OS
            subprocess.run(["./printImageTool", image_path, printer_name])
        else:
            print("Unsupported OS for printing")

    def scan_image(self, output_path):
        if platform.system() == 'Windows':
            # Create a WIA object
            wia = win32com.client.Dispatch("WIA.DeviceManager")
            
            # Get the first scanner
            dev = None
            for info in wia.DeviceInfos:
                if info.Type == 1:  # Type 1 indicates a scanner
                    dev = info.Connect()
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
        if platform.system() == 'Darwin':  # Placeholder for macOS or other OS
            self.run_scanline()
        else:
            print("Unsupported OS for printing")


    def run_scanline(self):
        try:
            # Define the command with parameters
            command = [
                "scanline",
                "-flatbed",         # Specifies flatbed scanning
                "-dir", ".",        # Saves to the current directory
                "-name", "scanned_image",  # Base name of the file
                "-jpeg"             # Output format as JPEG
            ]

            # Execute the command
            subprocess.run(command, check=True)
            print("Scan completed successfully.")
        except subprocess.CalledProcessError as e:
            print("Failed to complete scan:", e)

if __name__ == "__main__":
    sp = Scanner_Printer()
    sp.scan_image("test_image.jpg")  # Modify to run desired method