# Dependencies Explained - requirements.txt

## Why We Use Each Python Package

This document explains the purpose, usage, and importance of every dependency in `requirements.txt`.

---

## 📦 Core Dependencies

### 1. streamlit >= 1.28.0

**Purpose:** Web application framework

**Why We Need It:**
- Creates the entire user interface
- Provides widgets (buttons, file uploaders, text areas)
- Handles user interactions
- Manages session state
- Auto-refreshes on changes

**Used For:**
```python
import streamlit as st

# Create UI components
st.title("AI Interviewer")
uploaded_file = st.file_uploader("Upload")
answer = st.text_area("Your answer")
```

**Where Used:** `app.py` (entire application)

**Without It:** No web interface - application wouldn't work!

**Version >= 1.28.0:** Needed for latest features like `st.audio_input()`

---

### 2. numpy >= 1.24.0

**Purpose:** Numerical computing library

**Why We Need It:**
- Image processing operations
- Array manipulations
- Mathematical computations
- Required by OpenCV

**Used For:**
```python
import numpy as np

# Image is stored as numpy array
image = np.ndarray  # Shape: (height, width, channels)
```

**Where Used:**
- `modules/screen_capture.py` - Image arrays
- `modules/ocr_text_extractor.py` - Image processing
- Required by OpenCV and Pillow

**Without It:** Can't process images!

**Version >= 1.24.0:** Modern features and bug fixes

---

### 3. opencv-python >= 4.8.0

**Purpose:** Computer vision and image processing

**Why We Need It:**
- Load and save images
- Convert image formats (BGR ↔ RGB ↔ Grayscale)
- Image preprocessing for OCR
- Contour detection for UI elements

**Used For:**
```python
import cv2

# Load image
image = cv2.imread('photo.jpg')

# Convert to grayscale for better OCR
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply threshold
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Detect UI elements
contours = cv2.findContours(edges, ...)
```

**Where Used:**
- `modules/screen_capture.py` - Image loading and preprocessing
- `modules/ocr_text_extractor.py` - Image enhancement, UI detection

**Without It:** Can't load or preprocess images for OCR!

**Version >= 4.8.0:** Latest computer vision algorithms

---

### 4. Pillow >= 10.0.0

**Purpose:** Python Imaging Library (PIL)

**Why We Need It:**
- Read uploaded images from Streamlit
- Handle various image formats (PNG, JPG, JPEG)
- Image format conversion
- Alternative to OpenCV for simple operations

**Used For:**
```python
from PIL import Image

# Open image from uploaded file
image = Image.open(uploaded_file)

# Convert PIL Image to numpy array
img_array = np.array(image)
```

**Where Used:**
- `modules/screen_capture.py` - Loading uploaded images
- Works with Streamlit file uploader

**Without It:** Can't read uploaded image files!

**Version >= 10.0.0:** Security fixes and format support

---

## 🔍 OCR Dependencies

### 5. pytesseract >= 0.3.10

**Purpose:** Python wrapper for Tesseract OCR

**Why We Need It:**
- Extract text from images
- Read text from screenshots
- Recognize text in PDFs (when converted to images)
- Get word-level details with confidence scores

**Used For:**
```python
import pytesseract

# Extract text from image
text = pytesseract.image_to_string(image)

# Get detailed word data
data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
```

**Where Used:**
- `modules/ocr_text_extractor.py` - All OCR operations

**Without It:** Can't extract text from images!

**Note:** Also requires Tesseract OCR system installation

**Version >= 0.3.10:** Python 3.x support, better API

---

## 🎤 Speech-to-Text Dependencies

### 6. openai-whisper >= 20231117

**Purpose:** OpenAI's Whisper speech recognition model

**Why We Need It:**
- Transcribe audio to text
- High accuracy speech recognition
- Supports multiple languages
- Offline processing (no API calls)

**Used For:**
```python
import whisper

# Load model
model = whisper.load_model("tiny")

# Transcribe audio file
result = model.transcribe("audio.wav")
text = result['text']
```

**Where Used:**
- `modules/speech_to_text.py` - Audio transcription

**Without It:** Can't transcribe audio!

**Requires:** FFmpeg (for audio processing)

**Version >= 20231117:** Latest model improvements

**Model Sizes:**
- tiny: 75MB (fast) ⭐ Default
- base: 150MB (better)
- small: 500MB (good)
- medium: 1.5GB (very good)

---

## 🤖 LLM & AI Dependencies

### 7. langchain >= 0.0.350

**Purpose:** Framework for LLM applications

**Why We Need It:**
- Interact with OpenAI API
- Chain multiple LLM calls
- Manage prompts and messages
- Structured output handling

**Used For:**
```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Initialize LLM
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Generate questions
messages = [
    SystemMessage(content="You are an interviewer..."),
    HumanMessage(content="Context: ...")
]
response = llm.invoke(messages)
```

**Where Used:**
- `modules/question_generator.py` - Intelligent question generation

**Without It:** Only rule-based questions (fallback works)

**Optional:** System works without it, but questions are better with it

**Version >= 0.0.350:** Compatible API changes

---

### 8. openai >= 1.3.0

**Purpose:** Official OpenAI Python library

**Why We Need It:**
- Access GPT models (GPT-3.5-turbo)
- API authentication
- Required by LangChain

**Used For:**
```python
import openai

# Set API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Used internally by LangChain
```

**Where Used:**
- `modules/question_generator.py` - Behind LangChain

**Without It:** LangChain can't connect to OpenAI

**Optional:** Only needed if using OpenAI features

**Version >= 1.3.0:** New API structure (v1.0+)

**Cost:** ~$0.001-0.002 per interview (GPT-3.5-turbo)

---

## 📄 PDF Processing Dependencies

### 9. PyPDF2 >= 3.0.0

**Purpose:** PDF reader and text extractor

**Why We Need It:**
- Read PDF files
- Extract text from PDFs
- Access PDF metadata
- Fallback PDF engine

**Used For:**
```python
from PyPDF2 import PdfReader

# Read PDF
pdf_reader = PdfReader(pdf_file)

# Extract text from each page
for page in pdf_reader.pages:
    text = page.extract_text()
```

**Where Used:**
- `app.py` - PDF text extraction (fallback method)
- `modules/` - PDF processing utilities

**Without It:** Can't read PDFs! (unless pdfplumber works)

**Version >= 3.0.0:** Major rewrite, better API

---

### 10. pdfplumber >= 0.10.0

**Purpose:** Advanced PDF analysis and extraction

**Why We Need It:**
- Better text extraction than PyPDF2
- Extract tables from PDFs
- Handle complex layouts
- Multi-column text support
- Layout preservation

**Used For:**
```python
import pdfplumber

# Open PDF with context manager
with pdfplumber.open(pdf_file) as pdf:
    for page in pdf.pages:
        # Extract text with layout
        text = page.extract_text(layout=True)
        
        # Extract tables
        tables = page.extract_tables()
```

**Where Used:**
- `app.py` - Primary PDF extraction engine

**Why Both PyPDF2 AND pdfplumber?**
- pdfplumber: Better quality (primary)
- PyPDF2: Faster, reliable fallback
- Try pdfplumber first, fallback to PyPDF2 if it fails

**Version >= 0.10.0:** Table extraction improvements

---

### 11. reportlab >= 4.0.7

**Purpose:** PDF generation library

**Why We Need It:**
- Create PDF reports
- Add text, tables, charts
- Professional formatting
- Styling and layout

**Used For:**
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import getSampleStyleSheet

# Create PDF
doc = SimpleDocTemplate("report.pdf", pagesize=letter)

# Add content
story = []
story.append(Paragraph("Interview Report", styles['Title']))
story.append(Table(data))

# Build PDF
doc.build(story)
```

**Where Used:**
- `modules/report_generator.py` - PDF report creation

**Without It:** Can't generate PDF reports! (Markdown still works)

**Version >= 4.0.7:** Security fixes, Python 3.11 support

---

### 12. markdown >= 3.5.1

**Purpose:** Markdown to HTML converter

**Why We Need It:**
- Format report text
- Convert markdown to displayable format
- Text styling

**Used For:**
```python
import markdown

# Convert markdown to HTML for display
html = markdown.markdown(md_text)

# Or just use markdown syntax in report
report = "# Title\n**Bold** text"
```

**Where Used:**
- `modules/report_generator.py` - Markdown report formatting
- `app.py` - Display formatted text

**Without It:** Reports would be plain text

**Version >= 3.5.1:** Extension support, bug fixes

---

## 🔧 Utilities

### 13. python-dotenv >= 1.0.0

**Purpose:** Load environment variables from .env file

**Why We Need It:**
- Manage API keys securely
- Store configuration
- Keep secrets out of code

**Used For:**
```python
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")
```

**Where Used:**
- `app.py` - Load environment configuration
- `modules/question_generator.py` - Get API keys

**Without It:** Have to set environment variables manually

**Version >= 1.0.0:** Modern API, better error handling

**Example .env file:**
```bash
OPENAI_API_KEY=sk-your-key-here
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

---

## 📊 Dependency Relationships

### Dependency Chain

```
streamlit (Web UI)
├── Uses PIL (Pillow) for image uploads
├── Displays numpy arrays
└── Manages session state

numpy (Arrays)
├── Used by OpenCV
├── Used by Pillow
└── Image data format

opencv-python (Image Processing)
├── Requires numpy
└── Used by OCR module

pytesseract (OCR)
├── Uses opencv-python
└── Uses numpy

openai-whisper (Speech Recognition)
└── Requires FFmpeg (system)

langchain (LLM Framework)
├── Requires openai
└── Optional for smart questions

pdfplumber (PDF Primary)
└── Table extraction

PyPDF2 (PDF Fallback)
└── Basic text extraction

reportlab (PDF Generation)
└── Create reports

markdown (Text Formatting)
└── Report formatting

python-dotenv (Config)
└── Environment management
```

---

## 💾 Total Size

### Download Sizes

```
streamlit:         ~20 MB
numpy:             ~25 MB
opencv-python:     ~90 MB
Pillow:            ~3 MB
pytesseract:       ~1 MB
openai-whisper:    ~5 MB (+ 75-3000MB models)
langchain:         ~15 MB
openai:            ~2 MB
PyPDF2:            ~2 MB
pdfplumber:        ~3 MB
reportlab:         ~5 MB
markdown:          ~1 MB
python-dotenv:     ~1 MB
--------------------------------
Total:             ~170 MB (+ Whisper models)
```

**With Whisper tiny:** ~250 MB  
**With Whisper base:** ~320 MB

---

## 🔄 Optional vs Required

### Required (Core Functionality)

```
✅ streamlit        - App won't run without it
✅ numpy            - Images won't process
✅ opencv-python    - Can't process images
✅ Pillow           - Can't upload images
✅ pytesseract      - Can't extract text from images
```

### Optional (Enhanced Features)

```
⚠️ openai-whisper   - Optional: Skip audio feature
⚠️ langchain        - Optional: Use fallback questions
⚠️ openai           - Optional: Use fallback questions
⚠️ PyPDF2           - Optional: Skip PDF upload
⚠️ pdfplumber       - Optional: Use PyPDF2 only
⚠️ reportlab        - Optional: Skip PDF reports
⚠️ markdown         - Optional: Plain text reports
⚠️ python-dotenv    - Optional: Set env vars manually
```

**Minimal Setup (Image + OCR only):**
```txt
streamlit
numpy
opencv-python
Pillow
pytesseract
```

**Full Setup (All Features):**
All 13 packages

---

## 🚀 Installation Options

### Standard (Recommended)

```bash
pip install -r requirements.txt
```

Installs all dependencies with minimum versions.

### Upgrade Existing

```bash
pip install -r requirements.txt --upgrade
```

Updates all packages to latest versions.

### Minimal (No Audio/LLM)

```bash
pip install streamlit numpy opencv-python Pillow pytesseract
```

Only image processing, no audio or AI features.

### With Specific Versions

```bash
pip install streamlit==1.28.0 numpy==1.24.0
```

Lock to exact versions for reproducibility.

---

## 🔍 Version Constraints

### Why >= (Greater Than or Equal)?

**Example:** `streamlit>=1.28.0`

**Means:**
- Version 1.28.0 or newer
- Allows bug fixes (1.28.1, 1.28.2)
- Allows new features (1.29.0, 1.30.0)

**Why Not Exact (==)?**
- Flexible for security updates
- Compatible with other packages
- Gets improvements automatically

**Why Not Latest (*)?**
- May break compatibility
- Untested versions
- Stability concerns

### Minimum Versions Explained

- `streamlit>=1.28.0`: Need `st.audio_input()` (added 1.28)
- `numpy>=1.24.0`: Python 3.11 support
- `opencv-python>=4.8.0`: Latest CV algorithms
- `PyPDF2>=3.0.0`: API changed in v3
- `openai>=1.3.0`: New API structure

---

## 🎯 Dependency Purpose Summary

| Package | Primary Use | Can Skip? | Size |
|---------|------------|-----------|------|
| streamlit | Web UI | ❌ No | 20MB |
| numpy | Array ops | ❌ No | 25MB |
| opencv-python | Image processing | ❌ No | 90MB |
| Pillow | Image loading | ❌ No | 3MB |
| pytesseract | OCR text extraction | ❌ No | 1MB |
| openai-whisper | Audio transcription | ✅ Yes | 5MB |
| langchain | LLM framework | ✅ Yes | 15MB |
| openai | OpenAI API | ✅ Yes | 2MB |
| PyPDF2 | PDF reading | ✅ Yes | 2MB |
| pdfplumber | Advanced PDF | ✅ Yes | 3MB |
| reportlab | PDF generation | ✅ Yes | 5MB |
| markdown | Text formatting | ✅ Yes | 1MB |
| python-dotenv | Config management | ✅ Yes | 1MB |

---

## 📝 Common Questions

### Why so many packages?

**Answer:** Each handles a specific task:
- Images → opencv, Pillow, numpy
- Text extraction → pytesseract
- Audio → whisper
- PDFs → PyPDF2, pdfplumber
- AI questions → langchain, openai
- Reports → reportlab, markdown
- UI → streamlit

### Can I reduce dependencies?

**Yes!** Minimal setup:
```txt
streamlit
numpy
opencv-python
Pillow
pytesseract
```
This gives you image + OCR only (no audio, no PDF, no AI).

### Are these packages safe?

**Yes!** All are:
- ✅ Popular & well-maintained
- ✅ Thousands of users
- ✅ Regular security updates
- ✅ Open source

### Why two PDF libraries?

**pdfplumber:** Better quality, tables, complex layouts  
**PyPDF2:** Faster, reliable fallback

Try pdfplumber first → fallback to PyPDF2 if it fails.

### Do I need OpenAI account?

**No!** OpenAI is optional:
- With API: Smart AI-generated questions
- Without API: Rule-based questions (works fine)

---

## 🔗 Official Documentation

- **streamlit:** https://docs.streamlit.io/
- **numpy:** https://numpy.org/doc/
- **opencv-python:** https://docs.opencv.org/
- **Pillow:** https://pillow.readthedocs.io/
- **pytesseract:** https://github.com/madmaze/pytesseract
- **openai-whisper:** https://github.com/openai/whisper
- **langchain:** https://python.langchain.com/
- **openai:** https://platform.openai.com/docs
- **PyPDF2:** https://pypdf2.readthedocs.io/
- **pdfplumber:** https://github.com/jsvine/pdfplumber
- **reportlab:** https://www.reportlab.com/docs/
- **markdown:** https://python-markdown.github.io/
- **python-dotenv:** https://github.com/thecdp/python-dotenv

---

**Each dependency serves a specific, important purpose in the AI Interview System!**

For installation help, see [DOCUMENTATION.md](DOCUMENTATION.md#installation)

