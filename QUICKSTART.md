# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Tesseract OCR (Required for OCR)

**Windows:**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install the executable
3. If not in PATH, update `modules/ocr_text_extractor.py` line 12 with your Tesseract path

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

### Step 2: (Optional) Set OpenAI API Key

For enhanced question generation:

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or enter it in the Streamlit app sidebar.

### Step 3: Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📝 Demo Instructions

1. **Upload Content Tab:**
   - Upload a screenshot (PNG/JPG) of your project
   - Record or upload audio explaining your project
   - Click "Start Interview"

2. **Interview Tab:**
   - Answer the AI's questions (3-5 questions)
   - Type your responses and click "Submit Answer"

3. **Results Tab:**
   - View your score (0-100)
   - See breakdown by criterion
   - Read feedback and suggestions

4. **Report Tab:**
   - Download markdown report
   - Generate and download PDF report

## ⚠️ Troubleshooting

**Tesseract not found:**
- Install Tesseract (see Step 1)
- Update path in `modules/ocr_text_extractor.py` if needed

**Whisper model loading slowly:**
- First run downloads the model (~150MB)
- App automatically falls back to "tiny" model if needed

**OpenAI API errors:**
- App works without API key (uses fallback questions)
- For better questions, set a valid API key

## 🎯 Tips

- **Screenshots:** Use clear, high-contrast images for better OCR
- **Audio:** Speak clearly, 30+ seconds recommended
- **Answers:** Be detailed and technical for better scores

---

**Ready to go!** Run `streamlit run app.py` and start your interview! 🎤

