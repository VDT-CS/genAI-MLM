import cv2

from pathlib import Path

def processImage(path):
    image_path = Path(path)
    print("Image path:", image_path)
    image = cv2.imread(str(image_path))
    
    # Ensure the image loaded successfully
    if image is None:
        print(f'Failed to load image')
        exit()

    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Inverting the grayscale image
    invert = cv2.bitwise_not(grey_image)

    # Applying Gaussian Blur to the inverted image
    blur = cv2.GaussianBlur(invert, (21, 21), 0)

    # Inverting the blurred image
    inverted_blur = cv2.bitwise_not(blur)

    # Creating the sketch image
    sketch = cv2.divide(grey_image, inverted_blur, scale=256.0)

    # Applying thresholding to reduce noise and make the areas between edges solid black
    _, thresh_sketch = cv2.threshold(sketch, 240, 255, cv2.THRESH_BINARY)

    # Invert the thresholded sketch to have black as foreground
    invert_thresh_sketch = cv2.bitwise_not(thresh_sketch)

    # Define a kernel for the morphological operation
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))

    # Perform a closing operation to fill small holes and connect regions
    closed_sketch = cv2.morphologyEx(invert_thresh_sketch, cv2.MORPH_CLOSE, kernel)

    # Invert the closed sketch back to have white as foreground
    final_sketch = cv2.bitwise_not(closed_sketch)

    # Save the closed sketch image to disk
    resized_image = cv2.resize(final_sketch, (1024, 1024), interpolation=cv2.INTER_AREA)
    cv2.imwrite('gfx/currentImage.jpg', resized_image)
    return 'gfx/currentImage.jpg'