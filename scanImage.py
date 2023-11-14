import pyinsane2
import PIL.Image

def scan_image():
    pyinsane2.init()

    try:
        devices = pyinsane2.get_devices()
        if not devices:
            raise Exception("No scanner detected")

        device = devices[0]
        print("Using scanner:", device.name)

        pyinsane2.set_scanner_opt(device, 'resolution', [300])

        scan_session = device.scan(multiple=False)
        try:
            while True:
                scan_session.scan.read()
        except EOFError:
            pass

        image = scan_session.images[0]
        file_path = "scanned_image.jpg"
        image.save(file_path)
        print(f"Scanned image saved to {file_path}")

    finally:
        pyinsane2.exit()

scan_image()