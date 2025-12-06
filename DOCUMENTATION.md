# AI-Driven Automated Interviewer - Complete Documentation

## 📚 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [User Guide](#user-guide)
6. [System Architecture](#system-architecture)
7. [Module Documentation](#module-documentation)
8. [Configuration](#configuration)
9. [Troubleshooting](#troubleshooting)
10. [Recent Updates](#recent-updates)
11. [FAQ](#faq)
12. [Contributing](#contributing)

---

## Overview

### What is AI-Driven Automated Interviewer?

An intelligent system that conducts automated technical interviews for project presentations. It combines OCR, speech recognition, and AI to:
- Extract content from screenshots and PDFs
- Transcribe audio explanations
- Generate context-aware interview questions
- Validate student answers against expected points
- Provide comprehensive scoring and feedback

### Key Capabilities

- **Multi-Modal Input**: Images, PDFs, and audio
- **Intelligent Questioning**: AI-generated or rule-based questions
- **Answer Validation**: Automatic correctness checking
- **Comprehensive Evaluation**: 4-criterion scoring system
- **Detailed Feedback**: Strengths, weaknesses, and suggestions
- **Report Generation**: Markdown and PDF reports

---

## Features

### 1. Content Extraction

#### Image/Screenshot Processing
- **OCR Text Extraction**: Extracts text using Tesseract
- **Keyword Detection**: Identifies key technical terms
- **Code Snippet Detection**: Recognizes code patterns
- **UI Element Detection**: Identifies buttons, fields, etc.
- **Supported Formats**: PNG, JPG, JPEG

#### PDF Processing
- **Full Text Extraction**: Extracts all text from all pages
- **Table Detection**: Automatically extracts tables
- **Multi-Column Support**: Handles complex layouts
- **Page-by-Page Processing**: Labels content by page
- **Supported Features**: pdfplumber + PyPDF2 dual engine

#### Audio Transcription
- **Speech-to-Text**: OpenAI Whisper integration
- **Multiple Formats**: WAV, MP3, M4A
- **Auto-Detection**: FFmpeg auto-configuration
- **Fallback Models**: Tiny model for fast performance

### 2. Interview System

#### Question Generation
- **Context-Aware**: Based on extracted content
- **Expected Answers**: 3-5 key points per question
- **OpenAI Integration**: GPT-3.5 for intelligent questions
- **Fallback System**: Rule-based generation
- **Follow-up Questions**: Adaptive based on answers

#### Answer Validation
- **Automatic Checking**: Validates against expected points
- **Correctness Percentage**: 0-100% match score
- **Detailed Feedback**: Shows found/missing points
- **Fuzzy Matching**: Handles typos and variations
- **Visual Indicators**: ✅ Correct, ⚠️ Partial, ❌ Missing

### 3. Evaluation & Scoring

#### Scoring Criteria (Weighted)
1. **Technical Depth** (30%): Implementation details
2. **Clarity** (25%): Communication quality
3. **Originality** (25%): Unique approach
4. **Understanding** (20%): Conceptual grasp

#### Feedback System
- **Strengths Identification**: Top performing areas
- **Weakness Analysis**: Areas needing improvement
- **Actionable Suggestions**: Specific recommendations
- **Score Breakdown**: Detailed criterion analysis

### 4. Report Generation

#### Markdown Reports
- Executive summary
- Extracted content
- Full Q&A transcript
- Score breakdown
- Detailed feedback
- Downloadable as .md file

#### PDF Reports
- Professional formatting
- Charts and tables
- Color-coded sections
- Print-ready layout
- Downloadable as .pdf file

---

## Installation

### Prerequisites

#### Required Software
- **Python 3.8+**: Programming language runtime
- **Tesseract OCR**: For image text extraction
- **FFmpeg**: For audio processing

#### Python Packages
All managed via `requirements.txt`

### Step-by-Step Installation

#### 1. Clone/Download Project

```bash
cd AI
```

#### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Packages installed:**
- streamlit (Web UI)
- opencv-python (Image processing)
- pytesseract (OCR wrapper)
- openai-whisper (Speech recognition)
- pdfplumber, PyPDF2 (PDF processing)
- langchain, openai (LLM integration)
- reportlab (PDF generation)

#### 3. Install Tesseract OCR

**Windows:**
```powershell
winget install UB-Mannheim.TesseractOCR
```

**Manual:** Download from https://github.com/UB-Mannheim/tesseract/wiki

**Verification:**
```bash
tesseract --version
```

#### 4. Install FFmpeg

**Windows:**
```powershell
winget install Gyan.FFmpeg
```

**Automatic:**
```bash
python install_ffmpeg_auto.py
```

**Verification:**
```bash
ffmpeg -version
```

#### 5. (Optional) Configure OpenAI API

For enhanced question generation:

```powershell
# Windows PowerShell
$env:OPENAI_API_KEY="your-api-key-here"

# Or enter in app sidebar
```

### Automated Installation

Run the complete installer:

```bash
python install_all_dependencies.bat
```

This will:
1. Install Python packages
2. Install Tesseract OCR
3. Install FFmpeg
4. Verify all dependencies

---

## Quick Start

### Starting the Application

```bash
python -m streamlit run app.py
```

The app will open at `http://localhost:8501`

### Basic Workflow

1. **Upload Content** (Tab 1)
   - Upload screenshot or PDF
   - Upload/record audio
   - Click "Start Interview"

2. **Answer Questions** (Tab 2)
   - Read each question
   - Type your answer
   - Click "Submit Answer"
   - Repeat for all 5 questions

3. **View Results** (Tab 3)
   - See overall score
   - Review answer correctness
   - Read detailed feedback

4. **Generate Report** (Tab 4)
   - View/download Markdown report
   - Generate PDF report

---

## User Guide

### Tab 1: Upload Content

#### Uploading Images/PDFs

**Supported Files:**
- Images: PNG, JPG, JPEG
- Documents: PDF (text-based or scanned)

**What Happens:**
1. File is uploaded
2. Text is automatically extracted
3. Keywords are detected
4. Code snippets are identified
5. Statistics are shown
6. Full text is available in expander

**Tips:**
- Use high-resolution images
- Ensure text is clear
- PDF text-based works best
- Multi-page PDFs supported

#### Recording/Uploading Audio

**Audio Sources:**
- **Record**: Use browser microphone
- **Upload**: WAV, MP3, M4A files

**Process:**
1. Select audio source
2. Record or upload file
3. Click "Transcribe Audio"
4. Wait for processing (~5-10 seconds)
5. View transcription

**Tips:**
- Record 30+ seconds minimum
- Speak clearly, minimal background noise
- WAV format recommended
- First transcription takes longer (model loading)

#### Starting Interview

**Requirements:**
- At least one of: image/PDF OR audio
- Click "Start Interview" button

**What Happens:**
1. Context is analyzed
2. First question is generated
3. Interview session begins
4. Switch to Interview tab

### Tab 2: Interview

#### Answering Questions

**Display:**
- Question number (e.g., "Question 2 of 5")
- Question text
- Answer text area (unique per question)
- Submit button

**Process:**
1. Read question carefully
2. Type detailed answer
3. Click "Submit Answer"
4. Page refreshes with next question

**Tips:**
- Be specific and detailed
- Mention technical terms
- Explain implementation
- Use examples
- Answer is evaluated against expected points

#### Progress Tracking

**Indicators:**
- Progress bar (0-100%)
- Question count (e.g., "2/5 questions answered")
- Conversation history below

**History Display:**
- Q1, A1, Q2, A2 format
- Answers truncated to 200 chars
- Full history maintained

### Tab 3: Results

#### Overall Score

**Display:**
- Large score metric (0-100)
- Visual prominence

**Interpretation:**
- 90-100: Excellent
- 80-89: Very Good
- 70-79: Good
- 60-69: Satisfactory
- Below 60: Needs Improvement

#### Answer Correctness

**For Each Question:**
```
▼ Question X: Review
Question: [question text]
Your Answer: [answer preview]

Status:
✅ Correct (80% match)
⚠️ Partially Correct (60% match)
❌ Needs Improvement (40% match)

✅ Key points mentioned:
- ✓ point 1
- ✓ point 2

⚠️ Partially mentioned:
- ~ point 3

❌ Missing key points:
- ✗ point 4
```

**Correctness Levels:**
- ≥70%: Correct ✅
- 50-69%: Partial ⚠️
- <50%: Needs work ❌

#### Score Breakdown

**Four Criteria:**

1. **Technical Depth (30% weight)**
   - Implementation details
   - Technical terminology
   - Code references

2. **Clarity (25% weight)**
   - Answer structure
   - Vocabulary
   - Conciseness

3. **Originality (25% weight)**
   - Unique approach
   - Creative solutions
   - Personal insights

4. **Understanding (20% weight)**
   - Conceptual grasp
   - Relevance to question
   - Explanation quality

**Display:**
- Progress bar for each
- Score out of 100
- Weight percentage
- Description

#### Overall Feedback

**Strengths:**
- Top 2-3 performing criteria
- Scores and descriptions
- What you did well

**Areas for Improvement:**
- Bottom 2-3 criteria
- Specific weaknesses
- What to focus on

**Suggestions:**
- Actionable recommendations
- Improvement strategies
- Learning resources

### Tab 4: Report

#### Markdown Report

**Contents:**
- Executive summary
- Overall score
- Extracted content
- Full Q&A transcript
- Score breakdown table
- Detailed feedback

**Actions:**
- View in app
- Copy to clipboard
- Download as .md file

#### PDF Report

**Features:**
- Professional layout
- Tables and charts
- Color-coded sections
- All information from Markdown

**Actions:**
- Click "Generate PDF Report"
- Processing message shown
- Download automatically

**Use Cases:**
- Sharing with instructors
- Portfolio documentation
- Archival purposes
- Printing

---

## System Architecture

### Overview

```
┌─────────────────────────────────────┐
│      Streamlit Web Interface        │
└─────────────────┬───────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
┌───────▼─────┐   ┌─────────▼──────┐
│   Content   │   │   Interview    │
│  Extraction │   │   Management   │
└───────┬─────┘   └─────────┬──────┘
        │                   │
    ┌───┴────┐         ┌────┴────┐
    │        │         │         │
┌───▼──┐ ┌──▼───┐ ┌───▼───┐ ┌──▼────┐
│ OCR  │ │ STT  │ │ Q-Gen │ │ Score │
└──────┘ └──────┘ └───────┘ └───────┘
```

### Core Modules

#### 1. screen_capture.py
- Image loading
- Format conversion
- Preprocessing
- Validation

#### 2. ocr_text_extractor.py
- Tesseract integration
- Text extraction
- Keyword detection
- Code snippet identification
- UI element detection

#### 3. speech_to_text.py
- Whisper model loading
- FFmpeg detection/configuration
- Audio transcription
- Error handling

#### 4. question_generator.py
- LLM integration (OpenAI)
- Expected answer generation
- Fallback question generation
- Context analysis

#### 5. interview_manager.py
- Session state management
- Conversation history
- Question flow control
- Answer collection

#### 6. scoring.py
- Criterion evaluation
- Answer validation
- Correctness checking
- Feedback generation

#### 7. report_generator.py
- Markdown formatting
- PDF generation
- Content organization
- File export

### Data Flow

```
1. Upload → Extract → Store Context
2. Start Interview → Generate Q1 + Expected Points
3. Answer Q1 → Validate → Generate Q2
4. Repeat 5 times
5. Calculate Scores → Check Correctness
6. Generate Feedback → Create Report
```

### Session State Management

**Key State Variables:**
- `interview_manager`: Interview session
- `context`: Extracted content
- `scoring_system`: Evaluator instance
- `stt_model`: Whisper model
- `image_processed`: Cache flag
- `audio_processed`: Cache flag

---

## Module Documentation

### screen_capture.py

#### Class: ScreenCapture

**Methods:**

```python
load_image_from_file(file_obj) -> np.ndarray
```
- Loads image from uploaded file
- Returns: NumPy array or None

```python
preprocess_image(image) -> np.ndarray
```
- Converts to grayscale
- Applies threshold
- Enhances for OCR
- Returns: Processed image

### ocr_text_extractor.py

#### Class: OCRTextExtractor

**Methods:**

```python
extract_text(image) -> str
```
- Extracts text from image
- Returns: Text string

```python
extract_detailed(image) -> Dict
```
- Extracts text with bounding boxes
- Returns: Dict with words and positions

```python
extract_keywords(text, min_length=4) -> List[str]
```
- Identifies technical keywords
- Returns: List of keywords

```python
detect_code_snippets(text) -> List[str]
```
- Finds code-like patterns
- Returns: List of code snippets

### speech_to_text.py

#### Class: SpeechToText

**Methods:**

```python
__init__(model_size="tiny")
```
- Initializes Whisper model
- Checks FFmpeg availability

```python
transcribe_file(file_path, language=None) -> Dict
```
- Transcribes audio file
- Returns: Dict with text, language, error

```python
transcribe_audio(audio_data, language=None) -> Dict
```
- Transcribes audio bytes
- Returns: Dict with text, language, error

### question_generator.py

#### Class: QuestionGenerator

**Methods:**

```python
generate_initial_question(context) -> Dict
```
- Generates first question with expected points
- Returns: {question, expected_points}

```python
generate_followup_question(prev_q, answer, context) -> Dict
```
- Generates follow-up with expected points
- Returns: {question, expected_points}

### interview_manager.py

#### Class: InterviewManager

**Methods:**

```python
start_interview(context)
```
- Initializes interview session
- Generates first question

```python
submit_answer(answer) -> Optional[str]
```
- Processes answer
- Generates next question
- Returns: Next question or None

```python
get_current_question() -> Optional[str]
```
- Returns: Current question text

```python
get_conversation_history() -> List[Dict]
```
- Returns: Full conversation

```python
get_qa_pairs() -> List[Dict]
```
- Returns: Question-answer pairs

### scoring.py

#### Class: ScoringSystem

**Methods:**

```python
evaluate_qa_pair(question, answer, context, expected_points) -> Dict
```
- Evaluates single Q&A
- Checks correctness
- Returns: Score dict with correctness

```python
calculate_final_score(qa_scores) -> Dict
```
- Calculates weighted final score
- Returns: Overall score and breakdown

```python
generate_feedback(scores, qa_pairs) -> Dict
```
- Generates strengths/weaknesses
- Returns: Feedback dict

### report_generator.py

#### Class: ReportGenerator

**Methods:**

```python
generate_markdown_report(interview_data, scores, feedback) -> str
```
- Creates markdown report
- Returns: Markdown string

```python
generate_pdf_report(interview_data, scores, feedback, filename) -> bool
```
- Creates PDF report
- Returns: Success boolean

---

## Configuration

### Environment Variables

```bash
# OpenAI API (optional)
OPENAI_API_KEY="sk-..."

# Tesseract Path (if not in PATH)
TESSERACT_CMD="C:\Program Files\Tesseract-OCR\tesseract.exe"

# FFmpeg Path (if not in PATH)
FFMPEG_PATH="C:\ffmpeg\bin"
```

### Application Settings

**In app.py:**

```python
# Whisper Model Size
model_size = "tiny"  # Options: tiny, base, small, medium, large

# Max Interview Questions
max_questions = 5

# Scoring Weights
rubric = {
    'technical_depth': {'weight': 0.30},
    'clarity': {'weight': 0.25},
    'originality': {'weight': 0.25},
    'understanding': {'weight': 0.20}
}
```

### Customization

#### Changing Number of Questions

In `modules/interview_manager.py`:

```python
self.max_questions = 5  # Change to desired number
```

#### Adjusting Scoring Weights

In `modules/scoring.py`:

```python
self.rubric = {
    'technical_depth': {'weight': 0.35},  # Adjust weights
    'clarity': {'weight': 0.20},
    # ... must sum to 1.0
}
```

#### Modifying Question Templates

In `modules/question_generator.py`:

```python
def _generate_fallback_question(self, context: Dict) -> Dict:
    # Customize question templates here
```

---

## Troubleshooting

### Common Issues

#### 1. "Tesseract not found"

**Symptoms:**
- Error in OCR extraction
- No text extracted from images

**Solutions:**
```bash
# Install Tesseract
winget install UB-Mannheim.TesseractOCR

# Restart terminal and app
python -m streamlit run app.py
```

#### 2. "FFmpeg not found"

**Symptoms:**
- Audio transcription fails
- Error when clicking "Transcribe"

**Solutions:**
```bash
# Method 1: Auto-installer
python install_ffmpeg_auto.py

# Method 2: Package manager
winget install Gyan.FFmpeg

# Then restart terminal and app
```

#### 3. Page Hanging/Slow

**Causes:**
- Large files being processed
- Model loading for first time

**Solutions:**
- Use smaller images (<2MB)
- First Whisper run takes time (model download)
- Clear cache: `streamlit cache clear`
- Use "Reset All" button

#### 4. Answer Box Not Showing

**Cause:**
- Old session state

**Solution:**
- Restart application
- Use "Reset All" button
- Clear browser cache

#### 5. PDF Text Not Extracting

**Causes:**
- Image-based PDF (scanned)
- Unusual encoding

**Solutions:**
- Convert PDF pages to images
- Use text-based PDFs
- Check `pdfplumber` installation

#### 6. Questions Not Generating

**Cause:**
- No content extracted

**Solution:**
- Ensure image/PDF has text
- Check audio transcription worked
- Verify content in Tab 1

### Error Messages

#### "PyPDF2 not found"

```bash
pip install PyPDF2 pdfplumber
streamlit cache clear
python -m streamlit run app.py
```

#### "Progress bar invalid value"

Already fixed. If you see this, restart app.

#### "streamlit command not found"

```bash
# Use:
python -m streamlit run app.py
# Instead of:
streamlit run app.py
```

### Performance Tips

1. **Use Tiny Whisper Model** (default) - Faster
2. **Compress Images** - Before uploading
3. **Shorter Audio** - <2 minutes optimal
4. **Text-Based PDFs** - Better extraction
5. **Clear Cache** - Periodically
6. **Close Other Apps** - Free up RAM

---

## Recent Updates

### Version 2.0 Features

#### Answer Validation System ✨ NEW
- Automatic correctness checking
- Expected answer points
- Detailed feedback on matches
- Visual indicators (✅⚠️❌)

#### Enhanced PDF Support ✨ NEW
- Dual extraction engine (pdfplumber + PyPDF2)
- Table detection and extraction
- Multi-column layout support
- Page-by-page labeling
- Statistics display
- Download extracted text

#### Performance Improvements
- Smart caching system
- No re-processing on page reload
- Faster tiny Whisper model
- Dynamic widget keys
- Reset functionality

#### Auto-Detection Features
- FFmpeg auto-location (8+ paths)
- Tesseract auto-configuration
- Session PATH updates
- Project-bundled support

#### UI Enhancements
- Expandable full text view
- Correctness section
- Download buttons
- Better progress indicators
- Status messages

---

## FAQ

### General

**Q: Do I need OpenAI API?**
A: No. System works with fallback question generation.

**Q: What's the cost?**
A: Free! Optional OpenAI API has usage costs.

**Q: Can I use offline?**
A: Yes, except OpenAI features require internet.

### Installation

**Q: Installation taking long?**
A: First Whisper run downloads model (~75MB). Normal.

**Q: Which Python version?**
A: Python 3.8 or higher required.

**Q: Do I need GPU?**
A: No. CPU is sufficient (tiny model is fast).

### Usage

**Q: How many questions?**
A: Default is 5. Configurable in code.

**Q: Can I skip audio?**
A: Yes. Image/PDF alone works.

**Q: Can I retry interview?**
A: Yes. Use "Reset All" button.

**Q: Answer validation language?**
A: English primary. Other languages may work.

### Technical

**Q: How accurate is validation?**
A: 70%+ threshold. Fuzzy matching handles variations.

**Q: Can I customize scoring?**
A: Yes. Modify weights in `scoring.py`.

**Q: Export format options?**
A: Markdown (.md) and PDF (.pdf).

**Q: Maximum file sizes?**
A: Images: <10MB, Audio: <10 minutes, PDF: <50 pages.

---

## Contributing

### Extending the System

#### Adding New Scoring Criteria

1. Update `scoring.py`:
```python
self.rubric = {
    'technical_depth': {'weight': 0.25},
    'clarity': {'weight': 0.20},
    'originality': {'weight': 0.20},
    'understanding': {'weight': 0.15},
    'new_criterion': {'weight': 0.20}  # Add new
}
```

2. Implement scoring method:
```python
def _score_new_criterion(self, answer, context):
    # Your logic here
    return score
```

#### Customizing Question Generation

Edit `modules/question_generator.py`:
```python
def _generate_fallback_question(self, context):
    # Your custom logic
    return {'question': q, 'expected_points': points}
```

#### Adding New Report Formats

Extend `modules/report_generator.py`:
```python
def generate_html_report(self, data):
    # Generate HTML report
    return html_string
```

### Code Style

- Follow PEP 8
- Document all functions
- Add type hints
- Include error handling
- Write unit tests

### Testing

```bash
# Run tests
python -m pytest tests/

# Test specific module
python -m pytest tests/test_ocr.py
```

---

## License

This project is provided for educational and demonstration purposes.

---

## Support

### Documentation Files

- `README.md` - Quick start guide
- `DOCUMENTATION.md` - This file (complete docs)
- `QUICKSTART.md` - Fast setup guide
- `FFMPEG_INSTALL_GUIDE.md` - FFmpeg help
- `ENHANCED_PDF_EXTRACTION.md` - PDF features
- `ANSWER_VALIDATION_FEATURE.md` - Validation docs
- `INTERVIEW_FIX.md` - Interview fixes
- `PERFORMANCE_FIXES.md` - Speed improvements

### Getting Help

1. Check relevant documentation file
2. Check Troubleshooting section
3. Review error messages carefully
4. Check GitHub issues (if applicable)
5. Review code comments

---

## Appendix

### File Structure

```
AI/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # Quick start guide
├── DOCUMENTATION.md                # Complete documentation (this file)
│
├── modules/                        # Core modules
│   ├── screen_capture.py          # Image processing
│   ├── ocr_text_extractor.py      # OCR functionality
│   ├── speech_to_text.py          # Audio transcription
│   ├── question_generator.py      # Question generation
│   ├── interview_manager.py       # Interview flow
│   ├── scoring.py                 # Evaluation system
│   └── report_generator.py        # Report creation
│
├── tests/                          # Unit tests
│   ├── test_ocr.py
│   ├── test_stt.py
│   └── test_scoring.py
│
├── docs/                           # Additional documentation
│   └── architecture.md
│
├── examples/                       # Example files
│   ├── sample_screenshot.png
│   ├── sample_audio.wav
│   └── sample_report.md
│
└── [utility scripts]              # Installation & setup tools
    ├── install_ffmpeg_auto.py
    ├── check_dependencies.py
    ├── test_pdf_extraction.py
    └── setup_ffmpeg.py
```

### Keyboard Shortcuts

**In Streamlit App:**
- `R` - Rerun app
- `C` - Clear cache
- `?` - Show shortcuts

**In Terminal:**
- `Ctrl+C` - Stop app
- `Ctrl+Z` - Suspend (Windows)

### System Requirements

**Minimum:**
- CPU: Dual-core 2GHz
- RAM: 4GB
- Storage: 2GB free
- OS: Windows 10/11, macOS, Linux

**Recommended:**
- CPU: Quad-core 2.5GHz+
- RAM: 8GB+
- Storage: 5GB free
- SSD for faster loading

---

**Last Updated:** December 2024  
**Version:** 2.0  
**Author:** AI Interview System Team

---

For questions or issues, refer to the troubleshooting section or check individual documentation files for specific features.

