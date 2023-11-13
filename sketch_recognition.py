import torch
from torch import nn
from pathlib import Path
import cv2

LABELS = Path('class_names.txt').read_text().splitlines()

model = nn.Sequential(
    nn.Conv2d(1, 32, 3, padding='same'),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Conv2d(32, 64, 3, padding='same'),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Conv2d(64, 128, 3, padding='same'),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Flatten(),
    nn.Linear(1152, 256),
    nn.ReLU(),
    nn.Linear(256, len(LABELS)),
)
state_dict = torch.load('pytorch_model.bin',    map_location='cpu')
model.load_state_dict(state_dict, strict=False)
model.eval()


def predict(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale
    x = torch.tensor(gray_img, dtype=torch.float32).unsqueeze(0).unsqueeze(0) / 255.  # Shape: [1, 1, height, width]
    with torch.no_grad():
        out = model(x)
    probabilities = torch.nn.functional.softmax(out[0], dim=0)
    values, indices = torch.topk(probabilities, 5)
    confidences = {LABELS[i]: v.item() for i, v in zip(indices, values)}
    return confidences

image = cv2.imread('/Users/au509365/Documents/Development/sketch-to-image-machine/gfx/binary.jpg')

resized_image = cv2.resize(image, (24, 24), interpolation=cv2.INTER_AREA)
cv2.imwrite('/Users/au509365/Documents/Development/sketch-to-image-machine/gfx/tiny_img.jpg', resized_image)


print(predict(resized_image))
