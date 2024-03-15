import win32print

def get_printer_names():
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
    for printer in printers:
        print(printer[2])

if __name__ == "__main__":
    get_printer_names()