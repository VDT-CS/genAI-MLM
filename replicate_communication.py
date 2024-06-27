import os
import random
import replicate
from dotenv import load_dotenv
from urllib.request import urlopen
import certifi
import ssl

class Replicate:
    def __init__(self, api_key):
        # Load API token
        load_dotenv()
        self.api_key = os.getenv(api_key)  # Now storing the actual API key value
        self.appended_negative_prompt = ""

    # Generate image from sketch
    def generate(self, file_path, user_prompt, negative_prompt):
        deployment = replicate.deployments.get("vdt-cs/sketch-to-image")
        standard_negative_prompt = "extra digit, fewer digits, cropped, worst quality, low quality, glitch, deformed, mutated, ugly, disfigured"
        
        print("Generating with prompt: " + user_prompt + ", and negative prompt: " + standard_negative_prompt + negative_prompt)

        with open(file_path, 'rb') as sketch_file_object:
            prediction = deployment.predictions.create(input={"image": sketch_file_object, 
                                                              "prompt": self.random_personality_prompt + " " + user_prompt,
                                                              "negative_prompt": standard_negative_prompt + negative_prompt
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

    # A function that randomly adds one of several strings to the user prompt
    def random_personality_prompt():
        personality_promts = [
                            "",
                            "No matter what, the following image should be contain sausages:", 
                            "Try to make the image look like a cat:", 
                            "Be sure to include a rainbow in the image:", 
                            "If in doubt, add a tree to the image:", 
                            "Everything is better with a smiley face:", 
                            "The image should be a little bit spooky:", 
                            "Everything is made of cheese:", 
                            "If there is a person, they should be an alien:", 
                            "the image should be a little bit glitchy:", 
                            "Add extra limbs to the image:",
                            "The image should be a little bit abstract:",
                            "Add extra eyes to the image:",
                            "Add a lot of eyes to the image:",
                            "All colours should be inverted:",
                            "Only use the color red:",
                            ]
        return personality_promts[random.randint(0, len(personality_promts) - 1)]
    
# For debugging purposes
if __name__ == "__main__":
    load_dotenv()
    api_key = 'REPLICATE_API_TOKEN'
    actual_api_key = os.getenv(api_key)
    print(f"API Key: {actual_api_key}")
    rep = Replicate(api_key)
    print(rep.generate("scanned_image.jpg", "A mean Shark", ""))