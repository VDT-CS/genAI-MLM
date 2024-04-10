# Sketch-to-image Machine

This is the code-base for a research collaboration between the Department of Computer Science at Aarhus University and Kolding Design School.

## The Project

The project investigates how AI-generated images might be used in creative processes (by professionals and students), in a tangible way.

## The Prototype
For the project, we are designing a tangible user interface, that allow users to scan a paper sketch, describe it in a prompt, and adjust parameters such as the background, the time period, the style of the generated image, etc. The device will then generate such an image and print it.

Physically, the prototype integrates a scanner-printer device, a tiny Windows PC (an Intel NUC), and an Arduino Uno. The scanner-printer, does the printing and scanning, the Arduino handles the physical inputs (dials and buttons), and the windows PC interfaces between the scanner-printer, the Arduino and a sketch-to-image model running on (Replicate)[replicate.com]. We specifically chose to run this project on Windows because of the excellent pywin32 package, that handles the scanner-printer integration.

## Future Work
This software is open-source, and we aim to maintain it over time. Further, as the project evolves, we will link to additional resources in this repository, such as how to construct the physical device, our studies on the prototype, etc.
