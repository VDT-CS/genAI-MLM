import Cocoa

func printImage(imagePath: String, printerName: String) {
    guard let image = NSImage(contentsOfFile: imagePath) else {
        print("Failed to load the image")
        return
    }

    guard let printer = NSPrinter(name: printerName) else {
        print("Printer not found")
        return
    }

    let printInfo = NSPrintInfo.shared
    printInfo.printer = printer
    printInfo.orientation = .portrait
    printInfo.verticalPagination = .automatic
    printInfo.horizontalPagination = .fit

    // Create an NSImageView and properly size it
    let imageView = NSImageView(frame: NSRect(x: 0, y: 0, width: printInfo.paperSize.width, height: printInfo.paperSize.height))
    imageView.imageScaling = .scaleProportionallyUpOrDown
    imageView.image = image

    // Create the print operation with the image view
    let printOperation = NSPrintOperation(view: imageView, printInfo: printInfo)
    printOperation.showsPrintPanel = false  // Set to true to show print dialog
    printOperation.run()
}

if CommandLine.argc < 3 {
    print("Usage: \(CommandLine.arguments[0]) <imagePath> <printerName>")
} else {
    let imagePath = CommandLine.arguments[1]
    let printerName = CommandLine.arguments[2]
    printImage(imagePath: imagePath, printerName: printerName)
}