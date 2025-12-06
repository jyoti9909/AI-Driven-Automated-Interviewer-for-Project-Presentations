"""
OCR Text Extractor Module
Extracts text from images using Tesseract OCR
"""

import pytesseract
import cv2
import numpy as np
from typing import List, Dict, Optional
import re
import os
import platform


class OCRTextExtractor:
    """Extracts text and detects elements from images using OCR"""
    
    def __init__(self):
        # Auto-configure Tesseract path for Windows
        if platform.system() == 'Windows':
            possible_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                r'C:\Users\Public\Tesseract-OCR\tesseract.exe',
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    break
    
    def extract_text(self, image: np.ndarray) -> str:
        """
        Extract all text from image
        
        Args:
            image: Image array (grayscale or BGR)
            
        Returns:
            Extracted text string
        """
        try:
            # Convert to RGB if needed
            if len(image.shape) == 3:
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                image_rgb = image
            
            # Extract text with custom config for better results
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(image_rgb, config=custom_config)
            return text.strip()
        except pytesseract.TesseractNotFoundError:
            error_msg = """
            Tesseract OCR not found!
            
            Install using: winget install UB-Mannheim.TesseractOCR
            Or download from: https://github.com/UB-Mannheim/tesseract/wiki
            """
            print(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            print(f"Error in OCR extraction: {e}")
            return ""
    
    def extract_detailed(self, image: np.ndarray) -> Dict:
        """
        Extract detailed information including bounding boxes
        
        Args:
            image: Image array
            
        Returns:
            Dictionary with text, words, and metadata
        """
        try:
            if len(image.shape) == 3:
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                image_rgb = image
            
            # Get detailed data
            data = pytesseract.image_to_data(image_rgb, output_type=pytesseract.Output.DICT)
            
            # Extract words with confidence
            words = []
            text_parts = []
            
            for i, word in enumerate(data['text']):
                if word.strip():
                    words.append({
                        'text': word,
                        'confidence': int(data['conf'][i]) if data['conf'][i] != -1 else 0,
                        'x': data['left'][i],
                        'y': data['top'][i],
                        'width': data['width'][i],
                        'height': data['height'][i]
                    })
                    text_parts.append(word)
            
            full_text = ' '.join(text_parts)
            
            return {
                'full_text': full_text,
                'words': words,
                'word_count': len(words)
            }
        except Exception as e:
            print(f"Error in detailed OCR extraction: {e}")
            return {'full_text': '', 'words': [], 'word_count': 0}
    
    def extract_keywords(self, text: str, min_length: int = 4) -> List[str]:
        """
        Extract keywords from text (technical terms, code-like patterns)
        
        Args:
            text: Input text
            min_length: Minimum keyword length
            
        Returns:
            List of keywords
        """
        # Extract technical keywords (words with capitals, numbers, or common tech terms)
        words = re.findall(r'\b[A-Z][a-zA-Z0-9]*\b|\b[a-z]+[A-Z][a-zA-Z0-9]*\b', text)
        
        # Filter by length and common tech patterns
        keywords = [w for w in words if len(w) >= min_length]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_keywords = []
        for kw in keywords:
            if kw.lower() not in seen:
                seen.add(kw.lower())
                unique_keywords.append(kw)
        
        return unique_keywords[:20]  # Limit to top 20
    
    def detect_code_snippets(self, text: str) -> List[str]:
        """
        Detect potential code snippets in text
        
        Args:
            text: Input text
            
        Returns:
            List of detected code-like patterns
        """
        # Look for code-like patterns
        code_patterns = [
            r'def\s+\w+\([^)]*\)',  # Function definitions
            r'class\s+\w+',  # Class definitions
            r'import\s+\w+',  # Imports
            r'\w+\([^)]*\)',  # Function calls
            r'[a-zA-Z_]\w*\s*=\s*[^=]+',  # Variable assignments
        ]
        
        code_snippets = []
        for pattern in code_patterns:
            matches = re.findall(pattern, text)
            code_snippets.extend(matches)
        
        return list(set(code_snippets))[:10]  # Limit to top 10
    
    def detect_ui_elements(self, image: np.ndarray) -> Dict:
        """
        Detect UI elements (buttons, text boxes, etc.) using contour detection
        
        Args:
            image: Image array
            
        Returns:
            Dictionary with detected UI elements
        """
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filter contours by area
            min_area = 100
            ui_elements = []
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > min_area:
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h if h > 0 else 0
                    
                    # Classify based on aspect ratio
                    element_type = "unknown"
                    if 0.8 < aspect_ratio < 1.2:
                        element_type = "button"
                    elif aspect_ratio > 3:
                        element_type = "text_field"
                    elif aspect_ratio < 0.3:
                        element_type = "sidebar"
                    
                    ui_elements.append({
                        'type': element_type,
                        'x': x,
                        'y': y,
                        'width': w,
                        'height': h,
                        'area': area
                    })
            
            return {
                'elements': ui_elements,
                'count': len(ui_elements)
            }
        except Exception as e:
            print(f"Error detecting UI elements: {e}")
            return {'elements': [], 'count': 0}

