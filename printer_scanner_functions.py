# Currently, this file holds all the functions for interacting with the printer, the scanner, and the Replicate API. Should be broken up further.

import os
from dotenv import load_dotenv
import replicate
from urllib.request import urlopen
import certifi
import ssl
import win32ui
import win32com.client
from PIL import Image, ImageWin

PHYSICALWIDTH = 110
PHYSICALHEIGHT = 111

def send_to_replicate(file_path, prompt):
    # Load API token
    load_dotenv()
    api_key = os.getenv("REPLICATE_API_TOKEN")

    # Get the specific deployment
    deployment = replicate.deployments.get("vdt-cs/sketch-to-image")

    # Send the image to Replicate and create a prediction
    with open(file_path, 'rb') as sketch_file_object:
        prediction = deployment.predictions.create(input={"image": sketch_file_object, 
                                                          "prompt": prompt + "4k photo. photo realistic. Canon 5D MkIV"
                                                          })
    
    # Wait for the prediction to complete
    prediction.wait()

    # Handle the output
    if isinstance(prediction.output, list) and len(prediction.output) > 1:
        image_url = prediction.output[1]  # Get the URL of the second image
        download_and_display_image(image_url)
    else:
        print("Unexpected output format or insufficient outputs received.")

def download_and_display_image(image_url):
    # Create a SSL context using Certifi's set of trusted CAs
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    # Use this SSL context when opening the URL
    with urlopen(image_url, context=ssl_context) as response:
        with open('generatedImage.jpg', 'wb') as out_file:
            out_file.write(response.read())
        print("Image downloaded and saved as 'generatedImage.jpg'")

    # Print the image
    print_image('generatedImage.jpg', 'HP ENVY 4520 series')


def print_image(image_path, printer_name):
    printer_name = printer_name
    file_name = image_path

    hDC = win32ui.CreateDC ()
    hDC.CreatePrinterDC (printer_name)
    printer_size = hDC.GetDeviceCaps (PHYSICALWIDTH), hDC.GetDeviceCaps (PHYSICALHEIGHT)

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