import subprocess

def hp_scan():
    try:
        # The number corresponding to the scanner in the hp-scan prompt
        scanner_number = "1"

        # Start hp-scan and send the scanner number to it
        process = subprocess.run(["hp-scan", "--output=" + "scannedImage.jpg", "-m" + "color"], input=scanner_number, text=True, check=True)
        print("Scan completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while scanning: {e}")

hp_scan()
