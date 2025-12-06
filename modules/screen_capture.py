"""
Screen Capture Module
Handles image capture from screen or file upload
"""

import cv2
import numpy as np
from PIL import Image
import io
from typing import Optional, Union


class ScreenCapture:
    """Handles screen capture and image processing"""
    
    def __init__(self):
        self.current_image: Optional[np.ndarray] = None
    
    def load_image_from_file(self, uploaded_file) -> Optional[np.ndarray]:
        """
        Load image from uploaded file (Streamlit UploadedFile or file path)
        
        Args:
            uploaded_file: File object or path string
            
        Returns:
            numpy array of image (BGR format) or None if error
        """
        try:
            if hasattr(uploaded_file, 'read'):
                # Streamlit UploadedFile
                image_bytes = uploaded_file.read()
                image = Image.open(io.BytesIO(image_bytes))
            else:
                # File path
                image = Image.open(uploaded_file)
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert PIL to OpenCV format (BGR)
            self.current_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            return self.current_image
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
    
    def get_current_image(self) -> Optional[np.ndarray]:
        """Get the currently loaded image"""
        return self.current_image
    
    def preprocess_image(self, image: Optional[np.ndarray] = None) -> Optional[np.ndarray]:
        """
        Preprocess image for better OCR results
        
        Args:
            image: Image to preprocess (uses current_image if None)
            
        Returns:
            Preprocessed image
        """
        if image is None:
            image = self.current_image
        
        if image is None:
            return None
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
        
        return denoised

