import cv2
import numpy as np

def remove_background_grabcut(input_path, output_path):
    # Load the image
    img = cv2.imread(input_path)

    # Convert to grayscale and apply Gaussian blur
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect edges using Canny
    edges = cv2.Canny(blurred, 50, 150)

    # Dilate the edge image to ensure all relevant edges are captured
    kernel = np.ones((5, 5), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)

    # Initialize an empty mask and then set probable foreground and background
    mask = np.zeros(img.shape[:2], np.uint8)  # mask initialized to PR_BG
    mask[dilated_edges != 0] = cv2.GC_PR_FGD
    mask[dilated_edges == 0] = cv2.GC_PR_BGD

    # Initialize background and foreground models for GrabCut
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    # Run GrabCut with the new mask as initialization
    cv2.grabCut(img, mask, None, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_MASK)

    # Set pixels to foreground or background based on refined mask
    mask = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype('uint8')

    # Use the mask to extract the object and set the background to white
    output = img.copy()
    output[mask == 0] = (255, 255, 255)

    # Save the result
    cv2.imwrite(output_path, output)

    return output_path

# Example usage:
# result_path = remove_background_grabcut('path_to_input_image.png', 'path_to_output_image.png')
