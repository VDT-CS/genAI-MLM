import os
from dotenv import load_dotenv
import replicate
import tempfile
from urllib.request import urlretrieve

def send_to_replicate(file_path, prompt):
    # Load API token
    load_dotenv()
    api_key = os.getenv("REPLICATE_API_TOKEN")

    # Get the specific deployment
    deployment = replicate.deployments.get("magniswerfer/sketch-to-image-machine")

    # Send the image to Replicate and create a prediction
    with open(file_path, 'rb') as sketch_file_object:
        prediction = deployment.predictions.create(input={"image": sketch_file_object, "prompt": prompt + "4k photo. photo realistic. Canon 5D MkIV"})
    
    # Wait for the prediction to complete
    prediction.wait()

    # Handle the output
    if isinstance(prediction.output, list) and len(prediction.output) > 1:
        image_url = prediction.output[1]  # Get the URL of the second image
        download_and_display_image(image_url)
    else:
        print("Unexpected output format or insufficient outputs received.")

def download_and_display_image(image_url):
    # Download and display the image
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        urlretrieve(image_url, 'generatedImage.jpg')
        print("Image downloaded and saved as 'generatedImage.jpg'")

if __name__ == "__main__":
    # Get file path and prompt from command line input
    file_path = input("Enter the path of your sketch file: ")
    prompt = input("Enter your prompt: ")
    send_to_replicate(file_path, prompt)
