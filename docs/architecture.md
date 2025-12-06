# Architecture Documentation

## System Overview

The AI-Driven Automated Interviewer is a modular system designed to evaluate student project presentations through automated interviewing. The system processes visual and audio inputs, generates context-aware questions, and produces comprehensive evaluation reports.

## Component Architecture

### 1. Input Layer

#### Screen Capture Module (`screen_capture.py`)
- **Purpose**: Handles image input and preprocessing
- **Responsibilities**:
  - Load images from file uploads
  - Preprocess images for OCR (grayscale, thresholding, denoising)
  - Maintain current image state

#### OCR Text Extractor (`ocr_text_extractor.py`)
- **Purpose**: Extract text and detect elements from images
- **Responsibilities**:
  - Extract all text using Tesseract OCR
  - Extract keywords (technical terms, code patterns)
  - Detect code snippets (function definitions, imports, etc.)
  - Detect UI elements (buttons, text fields) using contour detection
- **Dependencies**: Tesseract OCR, OpenCV

#### Speech-to-Text Module (`speech_to_text.py`)
- **Purpose**: Convert audio to text
- **Responsibilities**:
  - Load Whisper model (base or tiny)
  - Transcribe audio files or bytes
  - Return transcription with metadata (language, segments)
- **Dependencies**: OpenAI Whisper

### 2. Processing Layer

#### Question Generator (`question_generator.py`)
- **Purpose**: Generate context-aware interview questions
- **Responsibilities**:
  - Generate initial questions from extracted content
  - Generate follow-up questions from Q&A context
  - Fallback to rule-based generation if LLM unavailable
- **Dependencies**: LangChain, OpenAI (optional)

#### Interview Manager (`interview_manager.py`)
- **Purpose**: Manage interview flow and conversation state
- **Responsibilities**:
  - Initialize interview session
  - Track conversation history
  - Manage question-answer pairs
  - Control interview completion
- **State Management**:
  - Conversation history
  - Current context
  - Question index
  - Completion status

### 3. Evaluation Layer

#### Scoring System (`scoring.py`)
- **Purpose**: Evaluate responses based on rubric
- **Responsibilities**:
  - Score individual Q&A pairs on 4 criteria
  - Calculate weighted final scores
  - Generate feedback (strengths, weaknesses, suggestions)
- **Rubric**:
  - Technical Depth (30%)
  - Clarity (25%)
  - Originality (25%)
  - Understanding (20%)

### 4. Output Layer

#### Report Generator (`report_generator.py`)
- **Purpose**: Generate markdown and PDF reports
- **Responsibilities**:
  - Generate markdown report with all data
  - Generate PDF report with formatting
  - Save reports to files
- **Dependencies**: ReportLab, Markdown

## Data Flow

```
1. User uploads image + audio
   ↓
2. Screen Capture → OCR → Extract text, keywords, code
   ↓
3. Speech-to-Text → Transcribe audio
   ↓
4. Combine context (screen + speech + keywords)
   ↓
5. Interview Manager starts interview
   ↓
6. Question Generator creates initial question
   ↓
7. User answers → Interview Manager tracks
   ↓
8. Question Generator creates follow-up
   ↓
9. Repeat 3-5 times
   ↓
10. Scoring System evaluates all Q&A pairs
    ↓
11. Report Generator creates markdown + PDF
```

## State Management

The application uses Streamlit's session state to maintain:

- `interview_manager`: Current interview session
- `scoring_system`: Scoring instance
- `report_generator`: Report generator instance
- `context`: Extracted content (screen text, speech, keywords)
- `stt_model`: Loaded Whisper model
- `interview_started`: Boolean flag
- `report_data`: Data for report generation

## Error Handling

### Model Loading Failures
- Whisper: Falls back to "tiny" model if "base" fails
- Tesseract: Provides clear error messages if not installed
- OpenAI: Works without API key using fallback generation

### Processing Errors
- OCR failures: Returns empty string, continues gracefully
- STT failures: Returns error in result dict
- PDF generation: Catches exceptions, shows error message

## Performance Considerations

### Model Loading
- Whisper models are loaded once and cached in session state
- First load may take 30-60 seconds

### Processing Speed
- OCR: ~1-3 seconds per image
- STT: ~5-15 seconds per 30-second audio (depends on model size)
- Question generation: ~2-5 seconds with OpenAI API, instant with fallback

### Memory Usage
- Base Whisper model: ~150MB
- Tiny Whisper model: ~75MB
- Image processing: Minimal (processed in-memory)

## Extensibility

### Adding New Scoring Criteria
1. Update `rubric` dict in `scoring.py`
2. Add scoring method `_score_new_criterion()`
3. Update `evaluate_qa_pair()` to call new method

### Custom Question Templates
1. Modify prompts in `question_generator.py`
2. Add new question types in `_generate_with_llm()`
3. Update fallback logic in `_generate_fallback_question()`

### New Report Formats
1. Add method in `report_generator.py` (e.g., `generate_json()`)
2. Update Streamlit app to include new format option
3. Add download button for new format

## Security Considerations

- API keys: Stored in environment variables or session state (not persisted)
- File uploads: Processed in memory, temporary files deleted
- User data: Not stored permanently (session-based)

## Testing Strategy

### Unit Tests
- Test OCR extraction with sample images
- Test STT with sample audio
- Test scoring logic with mock Q&A pairs
- Test report generation with sample data

### Integration Tests
- Test full flow: upload → interview → scoring → report
- Test error handling at each stage
- Test state management across tabs

## Deployment Considerations

### Local Deployment
- Run with: `streamlit run app.py`
- Access at: `http://localhost:8501`

### Cloud Deployment
- Streamlit Cloud: Push to GitHub, deploy via Streamlit Cloud
- Docker: Create Dockerfile with all dependencies
- Requirements: Ensure Tesseract is installed in container

### Scaling
- Current design: Single-user session-based
- For multiple users: Add user authentication, database for reports
- For production: Consider async processing, queue system for heavy tasks

