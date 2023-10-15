from PIL import Image
from pytesseract import pytesseract
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract


class ImageProcess:
    def __init__(self, imagestr: str):
        self.extractTextFromImage(imagestr)

    def extractTextFromImage(self, imagestr: str):
        image_path = rf"output\{imagestr}"
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        self.handleExtractedText(text)

    def handleExtractedText(self, text: str):
        print(text)
        pass
