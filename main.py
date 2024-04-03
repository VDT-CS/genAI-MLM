import printer_scanner_functions as psf

if __name__ == "__main__":
    # Press button to scan -- should be replaced with a button press event from the arduino
    input("Press Enter to scan...")
    # Get file path and prompt from command line input
    output_path = "scanned_image.jpg"
    psf.scan_image(output_path)
    file_path = output_path
    # Press button to prompt -- should be replaced
    input("Press Enter to promt...")
    prompt = input("Enter your prompt: ")
    # Press button to generate -- should be replaced with an event from the arduino
    input("Press Enter to generate...")
    psf.send_to_replicate(file_path, prompt)
