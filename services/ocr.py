import requests
import easyocr
from io import BytesIO
from PIL import Image

class OCRManager:
    """Manages OCR (Optical Character Recognition) operations"""
    
    def __init__(self):
        self.ocr_reader = None
    
    def load_image_from_url(self, image_url: str):
        """
        Load image from URL for OCR processing
        
        Args:
            image_url: URL of the image to process
            
        Returns:
            Image bytes
        """
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        
        # Convert the image to a format that easyocr can process
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
    
    def extract_text_from_image(self, img_byte_arr, languages=['en', 'ar']):
        """
        Extract text from image using OCR
        
        Args:
            img_byte_arr: Image data as bytes
            languages: List of languages for OCR recognition
            
        Returns:
            Extracted text as string
        """
        if not self.ocr_reader:
            self.ocr_reader = easyocr.Reader(languages)
        
        result = self.ocr_reader.readtext(img_byte_arr)
        return "\n".join([detection[1] for detection in result])
    
    def process_uploaded_image(self, uploaded_file, languages=['en', 'ar']):
        """
        Process an uploaded image file for text extraction
        
        Args:
            uploaded_file: Uploaded file object (from Streamlit file_uploader)
            languages: List of languages for OCR recognition
            
        Returns:
            Extracted text as string
        """
        img_byte_arr = uploaded_file.read()
        return self.extract_text_from_image(img_byte_arr, languages)