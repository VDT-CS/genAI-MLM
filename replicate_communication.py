import os
import replicate
from dotenv import load_dotenv
from urllib.request import urlopen
import certifi
import ssl

class Replicate:
    def __init__(self, api_key):
        # Load API token
        load_dotenv()
        self.api_key = api_key
        self.appended_prompt = ""
    
    #Generate image from sketch
    def generate(self, file_path, userPrompt):
        api_key = os.getenv(self.api_key)
        deployment = replicate.deployments.get("vdt-cs/sketch-to-image")
        
        with open(file_path, 'rb') as sketch_file_object:
            prediction = deployment.predictions.create(input={"image": sketch_file_object, 
                                                              "prompt": userPrompt + self.appended_prompt
                                                              })
        prediction.wait()
        if isinstance(prediction.output, list) and len(prediction.output) > 1:
            image_url = prediction.output[1]
            return image_url #returns the URL of the generated image
        else: # This should probably throw an exception instead of printing
            print("Unexpected output format or insufficient outputs received.")
            pass

    #Download image from URL
    def download_image(self, image_url, file_path):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        with urlopen(image_url, context=ssl_context) as response:
            with open(file_path, 'wb') as out_file:
                out_file.write(response.read())
            print("Image downloaded and saved as 'generated_image.jpg'")
        return file_path #returns the path of the downloaded image
    
    def append_to_prompt(self, prompt):
        self.appended_prompt += prompt
    
# For debugging purposes
if __name__ == "__main__":
    rep = Replicate("REPLICATE_API_KEY")
    print(rep.generate("scanned_image.jpg", "A mean Shark"))