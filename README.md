# 🎤 AI-Driven Automated Interviewer for Project Presentations

A complete end-to-end system that listens to student project presentations, understands content from screens and speech, asks adaptive interview questions, and generates comprehensive score reports with feedback.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Demo Flow](#demo-flow)
- [Scoring System](#scoring-system)
- [Requirements](#requirements)
- [Troubleshooting](#troubleshooting)

## ✨ Features

### 1. Presentation Understanding
- **Screen Capture**: Upload screenshots or process static images
- **OCR Text Extraction**: Extracts text from slides, code, and UI using Tesseract OCR
- **Speech-to-Text**: Transcribes audio explanations using OpenAI Whisper
- **Content Detection**: Identifies UI elements, code snippets, keywords, and diagrams

### 2. Dynamic Interviewing
- **Context-Aware Questions**: Generates intelligent questions based on extracted content
- **Follow-up Questions**: Asks adaptive follow-ups based on student responses
- **Conversation Management**: Maintains interview flow and conversation history
- **LLM Integration**: Uses OpenAI GPT or fallback rule-based generation

### 3. Evaluation & Feedback
- **Comprehensive Scoring**: Evaluates on 4 criteria with weighted scoring
- **Detailed Feedback**: Provides strengths, weaknesses, and actionable suggestions
- **Report Generation**: Creates markdown and PDF reports

## 🏗️ Architecture

The system is built with a modular architecture:

```
┌─────────────────────────────────────────────────────────┐
│                   Streamlit Web UI                        │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
│ Screen       │  │ Speech-to-   │  │ OCR Text     │
│ Capture      │  │ Text         │  │ Extractor    │
└───────┬──────┘  └──────┬───────┘  └──────┬───────┘
        │                │                 │
        └────────────────┼─────────────────┘
                         │
              ┌──────────▼──────────┐
              │  Interview Manager   │
              └──────────┬───────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼──────┐  ┌──────▼──────┐  ┌─────▼──────┐
│ Question     │  │ Scoring      │  │ Report     │
│ Generator    │  │ System       │  │ Generator  │
└──────────────┘  └──────────────┘  └────────────┘
```

### Core Modules

- **`screen_capture.py`**: Handles image loading and preprocessing
- **`ocr_text_extractor.py`**: Extracts text, keywords, and detects code snippets
- **`speech_to_text.py`**: Converts audio to text using Whisper
- **`question_generator.py`**: Generates questions using LLM or fallback rules
- **`interview_manager.py`**: Manages interview flow and conversation state
- **`scoring.py`**: Evaluates responses based on rubric
- **`report_generator.py`**: Generates markdown and PDF reports

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Tesseract OCR installed on your system
  - **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
  - **macOS**: `brew install tesseract`
  - **Linux**: `sudo apt-get install tesseract-ocr`

### Step 1: Clone or Download

```bash
cd AI
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Tesseract (Windows)

If Tesseract is not in your PATH, uncomment and update the path in `modules/ocr_text_extractor.py`:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### Step 4: (Optional) Set OpenAI API Key

For enhanced question generation, set your OpenAI API key:

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your-api-key-here"

# Linux/Mac
export OPENAI_API_KEY="your-api-key-here"
```

Or enter it in the Streamlit app sidebar.

## 💻 Usage

### Starting the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

### Demo Flow

1. **Upload Content** (Tab 1)
   - Upload a screenshot of your project (PNG, JPG, JPEG)
   - Record or upload audio explaining your project (30+ seconds recommended)
   - Click "Start Interview"

2. **Answer Questions** (Tab 2)
   - Read the AI-generated question
   - Type your answer in the text area
   - Click "Submit Answer"
   - Answer 3-5 questions total

3. **View Results** (Tab 3)
   - See your overall score (0-100)
   - Review score breakdown by criterion
   - Read strengths, weaknesses, and suggestions

4. **Generate Report** (Tab 4)
   - View markdown report
   - Download markdown file
   - Generate and download PDF report

## 📁 Project Structure

```
AI/
├── app.py                      # Streamlit main application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── modules/                    # Core modules
│   ├── __init__.py
│   ├── screen_capture.py      # Image capture and preprocessing
│   ├── ocr_text_extractor.py  # OCR text extraction
│   ├── speech_to_text.py      # Whisper STT wrapper
│   ├── question_generator.py   # LLM question generation
│   ├── interview_manager.py    # Interview flow management
│   ├── scoring.py              # Rubric-based scoring
│   └── report_generator.py     # Markdown/PDF report generation
├── tests/                      # Unit tests
│   ├── test_ocr.py
│   ├── test_stt.py
│   └── test_scoring.py
├── examples/                   # Example assets
│   ├── sample_screenshot.png
│   ├── sample_audio.wav
│   └── sample_report.md
└── docs/                       # Documentation
    └── architecture.md
```

## 📊 Scoring System

The system evaluates responses on 4 criteria with weighted scoring:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Technical Depth | 30% | How well they explain implementation |
| Clarity | 25% | Structure, vocabulary, confidence |
| Originality | 25% | Uniqueness of design/idea |
| Understanding | 20% | Conceptual grasp |

**Formula**: `Overall Score = Σ(Criterion Score × Weight)`

### Scoring Logic

- **Technical Depth**: Based on technical keywords, code references, implementation details
- **Clarity**: Based on sentence structure, length, transition words
- **Originality**: Based on unique indicators, personal experience mentions
- **Understanding**: Based on answer relevance, explanation quality

## 🔧 Requirements

### Python Packages

See `requirements.txt` for complete list. Key dependencies:

- `streamlit`: Web UI framework
- `opencv-python`: Image processing
- `pytesseract`: OCR text extraction
- `openai-whisper`: Speech-to-text
- `langchain`: LLM integration
- `reportlab`: PDF generation

### System Requirements

- **RAM**: 4GB minimum (8GB recommended for Whisper)
- **Storage**: ~2GB for models and dependencies
- **OS**: Windows, macOS, or Linux

## 🐛 Troubleshooting

### Tesseract Not Found

**Error**: `TesseractNotFoundError`

**Solution**: 
1. Install Tesseract OCR
2. Update path in `modules/ocr_text_extractor.py` if needed

### Whisper Model Loading Issues

**Error**: Slow or failed model loading

**Solution**: 
- The app automatically falls back to "tiny" model if "base" fails
- First run downloads the model (~150MB for base, ~75MB for tiny)

### OpenAI API Errors

**Error**: API key issues

**Solution**: 
- The app works without OpenAI API using fallback question generation
- For better questions, set a valid API key in sidebar

### PDF Generation Errors

**Error**: ReportLab font issues

**Solution**: 
- Ensure reportlab is installed: `pip install reportlab`
- On Linux, may need: `sudo apt-get install python3-reportlab`

## 📝 Example Output

### Sample Report Structure

```markdown
# AI-Driven Interview Report

## Executive Summary
- Overall Score: 78/100
- Questions Asked: 5

## Extracted Content
- Screen text from OCR
- Speech transcript
- Keywords detected

## Interview Q&A
- Question 1: ...
- Answer 1: ...

## Scoring Breakdown
- Technical Depth: 82/100 (30% weight)
- Clarity: 75/100 (25% weight)
- ...

## Feedback
- Strengths: ...
- Areas for Improvement: ...
- Suggestions: ...
```

## 🤝 Contributing

This is a complete project. To extend:

1. Add new scoring criteria in `modules/scoring.py`
2. Customize question templates in `modules/question_generator.py`
3. Enhance OCR preprocessing in `modules/screen_capture.py`
4. Add new report formats in `modules/report_generator.py`

## 📄 License

This project is provided as-is for educational and demonstration purposes.

## 🎯 Future Enhancements

- Real-time screen capture
- Multi-language support
- Video analysis
- Advanced UI element detection
- Custom rubric configuration
- Export to multiple formats (JSON, CSV)

---

**Built with ❤️ using Python, Streamlit, Whisper, Tesseract, and LangChain**

