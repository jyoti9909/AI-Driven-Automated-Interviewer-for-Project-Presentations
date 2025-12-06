# API Reference - AI Interview System

## Module APIs

### screen_capture.py

#### ScreenCapture Class

```python
class ScreenCapture:
    """Handles image capture and preprocessing"""
```

**Methods:**

##### `load_image_from_file(file_obj) -> Optional[np.ndarray]`
Load image from uploaded file object.

**Parameters:**
- `file_obj`: Streamlit UploadedFile object

**Returns:**
- `np.ndarray`: Image array in BGR format
- `None`: If loading fails

**Example:**
```python
from modules.screen_capture import ScreenCapture

sc = ScreenCapture()
image = sc.load_image_from_file(uploaded_file)
if image is not None:
    print(f"Image shape: {image.shape}")
```

##### `preprocess_image(image: np.ndarray) -> Optional[np.ndarray]`
Preprocess image for better OCR results.

**Parameters:**
- `image`: Input image array

**Returns:**
- `np.ndarray`: Preprocessed grayscale image
- `None`: If preprocessing fails

**Processing Steps:**
1. Convert to grayscale
2. Apply binary threshold
3. Noise reduction

---

### ocr_text_extractor.py

#### OCRTextExtractor Class

```python
class OCRTextExtractor:
    """Extracts text and detects elements from images"""
```

**Methods:**

##### `extract_text(image: np.ndarray) -> str`
Extract text from image using Tesseract OCR.

**Parameters:**
- `image`: Image array (BGR or grayscale)

**Returns:**
- `str`: Extracted text

**Example:**
```python
from modules.ocr_text_extractor import OCRTextExtractor

ocr = OCRTextExtractor()
text = ocr.extract_text(image)
print(f"Extracted: {text}")
```

##### `extract_detailed(image: np.ndarray) -> Dict`
Extract text with word-level details.

**Parameters:**
- `image`: Image array

**Returns:**
```python
{
    'full_text': str,           # Complete text
    'words': [                  # List of word objects
        {
            'text': str,        # Word text
            'confidence': int,  # OCR confidence (0-100)
            'x': int,          # X position
            'y': int,          # Y position
            'width': int,      # Bounding box width
            'height': int      # Bounding box height
        }
    ],
    'word_count': int          # Total words
}
```

##### `extract_keywords(text: str, min_length: int = 4) -> List[str]`
Extract technical keywords from text.

**Parameters:**
- `text`: Input text
- `min_length`: Minimum keyword length (default: 4)

**Returns:**
- `List[str]`: List of keywords (max 20)

**Example:**
```python
keywords = ocr.extract_keywords(text, min_length=5)
print(f"Keywords: {keywords}")
```

##### `detect_code_snippets(text: str) -> List[str]`
Detect code-like patterns in text.

**Parameters:**
- `text`: Input text

**Returns:**
- `List[str]`: List of code snippets (max 10)

**Patterns Detected:**
- Function definitions: `def function_name()`
- Class definitions: `class ClassName`
- Import statements: `import module`
- Function calls: `function()`
- Variable assignments: `var = value`

---

### speech_to_text.py

#### SpeechToText Class

```python
class SpeechToText:
    """Handles speech-to-text conversion using Whisper"""
```

**Methods:**

##### `__init__(model_size: str = "base")`
Initialize Whisper model.

**Parameters:**
- `model_size`: Model size ("tiny", "base", "small", "medium", "large")

**Example:**
```python
from modules.speech_to_text import SpeechToText

stt = SpeechToText(model_size="tiny")
```

##### `transcribe_file(file_path: str, language: Optional[str] = None) -> Dict`
Transcribe audio file to text.

**Parameters:**
- `file_path`: Path to audio file
- `language`: Optional language code (e.g., 'en')

**Returns:**
```python
{
    'text': str,           # Transcribed text
    'language': str,       # Detected/specified language
    'segments': List,      # Segment details
    'error': Optional[str] # Error message if failed
}
```

**Example:**
```python
result = stt.transcribe_file('audio.wav', language='en')
if not result['error']:
    print(f"Transcription: {result['text']}")
```

##### `transcribe_audio(audio_data: bytes, language: Optional[str] = None) -> Dict`
Transcribe audio bytes to text.

**Parameters:**
- `audio_data`: Audio file bytes
- `language`: Optional language code

**Returns:**
- Same as `transcribe_file()`

---

### question_generator.py

#### QuestionGenerator Class

```python
class QuestionGenerator:
    """Generates interview questions based on context"""
```

**Methods:**

##### `__init__(use_openai: bool = True, model_name: str = "gpt-3.5-turbo")`
Initialize question generator.

**Parameters:**
- `use_openai`: Whether to use OpenAI API
- `model_name`: OpenAI model name

##### `generate_initial_question(context: Dict) -> Dict`
Generate initial interview question with expected answer points.

**Parameters:**
```python
context = {
    'screen_text': str,      # Extracted text from image/PDF
    'speech_text': str,      # Transcribed audio
    'keywords': List[str],   # Detected keywords
    'code_snippets': List[str]  # Detected code
}
```

**Returns:**
```python
{
    'question': str,              # The interview question
    'expected_points': List[str]  # 3-5 key points answer should contain
}
```

**Example:**
```python
from modules.question_generator import QuestionGenerator

qgen = QuestionGenerator(use_openai=True)
context = {
    'screen_text': 'Machine learning project...',
    'keywords': ['neural network', 'training', 'accuracy']
}
q_data = qgen.generate_initial_question(context)
print(f"Q: {q_data['question']}")
print(f"Expected: {q_data['expected_points']}")
```

##### `generate_followup_question(previous_question: str, answer: str, context: Dict) -> Dict`
Generate follow-up question based on previous Q&A.

**Parameters:**
- `previous_question`: Previous question text
- `answer`: Student's answer
- `context`: Original context dict

**Returns:**
- Same format as `generate_initial_question()`

---

### interview_manager.py

#### InterviewManager Class

```python
class InterviewManager:
    """Manages interview conversation flow"""
```

**Attributes:**
```python
max_questions: int = 5               # Maximum questions to ask
current_question_index: int          # Current question number (0-indexed)
conversation_history: List[Dict]     # Full conversation
interview_started: bool              # Interview status
interview_completed: bool            # Completion status
```

**Methods:**

##### `start_interview(context: Dict) -> None`
Start a new interview session.

**Parameters:**
- `context`: Context dict with extracted content

**Side Effects:**
- Resets conversation history
- Generates first question
- Sets interview_started = True

**Example:**
```python
from modules.interview_manager import InterviewManager
from modules.question_generator import QuestionGenerator

qgen = QuestionGenerator()
manager = InterviewManager(qgen)
manager.start_interview(context)
```

##### `submit_answer(answer: str) -> Optional[str]`
Submit student's answer and get next question.

**Parameters:**
- `answer`: Student's answer text

**Returns:**
- `str`: Next question text
- `None`: If interview is complete

**Example:**
```python
answer = "I used Python and TensorFlow..."
next_q = manager.submit_answer(answer)
if next_q:
    print(f"Next: {next_q}")
else:
    print("Interview complete!")
```

##### `get_current_question() -> Optional[str]`
Get the current unanswered question.

**Returns:**
- `str`: Current question text
- `None`: If no current question

##### `get_conversation_history() -> List[Dict]`
Get full conversation history.

**Returns:**
```python
[
    {
        'type': 'question',
        'content': str,
        'expected_points': List[str],
        'timestamp': str,
        'question_index': int
    },
    {
        'type': 'answer',
        'content': str,
        'timestamp': str,
        'question_index': int
    },
    ...
]
```

##### `get_qa_pairs() -> List[Dict]`
Get question-answer pairs only.

**Returns:**
```python
[
    {
        'question': str,
        'answer': str,
        'timestamp': str
    },
    ...
]
```

##### `is_complete() -> bool`
Check if interview is complete.

**Returns:**
- `bool`: True if all questions answered

---

### scoring.py

#### ScoringSystem Class

```python
class ScoringSystem:
    """Evaluates interview performance"""
```

**Rubric:**
```python
rubric = {
    'technical_depth': {
        'weight': 0.30,  # 30%
        'description': 'How well they explain implementation'
    },
    'clarity': {
        'weight': 0.25,  # 25%
        'description': 'Structure, vocabulary, confidence'
    },
    'originality': {
        'weight': 0.25,  # 25%
        'description': 'Uniqueness of design/idea'
    },
    'understanding': {
        'weight': 0.20,  # 20%
        'description': 'Conceptual grasp'
    }
}
```

**Methods:**

##### `evaluate_qa_pair(question: str, answer: str, context: Dict, expected_points: List[str] = None) -> Dict`
Evaluate a single Q&A pair.

**Parameters:**
- `question`: Question text
- `answer`: Student's answer
- `context`: Project context
- `expected_points`: Expected key points (optional)

**Returns:**
```python
{
    'technical_depth': float,  # Score 0-100
    'clarity': float,          # Score 0-100
    'originality': float,      # Score 0-100
    'understanding': float,    # Score 0-100
    'correctness': {           # If expected_points provided
        'is_correct': bool,
        'correctness_percent': float,
        'found_points': List[str],
        'partially_found': List[str],
        'missing_points': List[str],
        'total_expected': int
    }
}
```

**Example:**
```python
from modules.scoring import ScoringSystem

scorer = ScoringSystem()
scores = scorer.evaluate_qa_pair(
    question="How did you implement authentication?",
    answer="I used JWT tokens and bcrypt...",
    context={'keywords': ['JWT', 'security']},
    expected_points=['JWT tokens', 'password hashing', 'session']
)
print(f"Technical: {scores['technical_depth']}")
print(f"Correctness: {scores['correctness']['correctness_percent']}%")
```

##### `calculate_final_score(qa_scores: List[Dict]) -> Dict`
Calculate weighted final score from all Q&A pairs.

**Parameters:**
- `qa_scores`: List of score dicts from evaluate_qa_pair

**Returns:**
```python
{
    'overall_score': float,  # Weighted average 0-100
    'breakdown': {           # Individual criterion averages
        'technical_depth': float,
        'clarity': float,
        'originality': float,
        'understanding': float
    },
    'rubric': Dict  # Copy of rubric with weights
}
```

##### `generate_feedback(final_scores: Dict, qa_pairs: List[Dict]) -> Dict`
Generate detailed feedback.

**Parameters:**
- `final_scores`: Output from calculate_final_score
- `qa_pairs`: List of Q&A pairs

**Returns:**
```python
{
    'strengths': [
        {
            'criterion': str,
            'score': float,
            'description': str
        }
    ],
    'weaknesses': [
        {
            'criterion': str,
            'score': float,
            'description': str
        }
    ],
    'suggestions': List[str]  # Actionable recommendations
}
```

---

### report_generator.py

#### ReportGenerator Class

```python
class ReportGenerator:
    """Generates interview reports"""
```

**Methods:**

##### `generate_markdown_report(interview_data: Dict, scores: Dict, feedback: Dict) -> str`
Generate markdown formatted report.

**Parameters:**
```python
interview_data = {
    'context': Dict,          # Extracted content
    'qa_pairs': List[Dict],   # Question-answer pairs
    'timestamp': str          # Interview time
}
```
- `scores`: From calculate_final_score
- `feedback`: From generate_feedback

**Returns:**
- `str`: Markdown formatted report

**Example:**
```python
from modules.report_generator import ReportGenerator

repgen = ReportGenerator()
markdown = repgen.generate_markdown_report(
    interview_data={'context': {...}, 'qa_pairs': [...]},
    scores=final_scores,
    feedback=feedback_data
)

# Save to file
with open('report.md', 'w') as f:
    f.write(markdown)
```

##### `generate_pdf_report(interview_data: Dict, scores: Dict, feedback: Dict, filename: str) -> bool`
Generate PDF formatted report.

**Parameters:**
- Same as markdown, plus:
- `filename`: Output PDF filename

**Returns:**
- `bool`: True if successful, False otherwise

**Example:**
```python
success = repgen.generate_pdf_report(
    interview_data=data,
    scores=final_scores,
    feedback=feedback_data,
    filename='interview_report.pdf'
)
if success:
    print("PDF generated!")
```

---

## Usage Examples

### Complete Interview Flow

```python
from modules.screen_capture import ScreenCapture
from modules.ocr_text_extractor import OCRTextExtractor
from modules.speech_to_text import SpeechToText
from modules.question_generator import QuestionGenerator
from modules.interview_manager import InterviewManager
from modules.scoring import ScoringSystem
from modules.report_generator import ReportGenerator

# 1. Extract Content
sc = ScreenCapture()
ocr = OCRTextExtractor()
stt = SpeechToText(model_size="tiny")

image = sc.load_image_from_file(uploaded_image)
text = ocr.extract_text(image)
keywords = ocr.extract_keywords(text)

audio_result = stt.transcribe_file('audio.wav')
speech_text = audio_result['text']

context = {
    'screen_text': text,
    'speech_text': speech_text,
    'keywords': keywords,
    'code_snippets': []
}

# 2. Conduct Interview
qgen = QuestionGenerator(use_openai=True)
manager = InterviewManager(qgen)
manager.start_interview(context)

# Simulate answering 5 questions
for i in range(5):
    current_q = manager.get_current_question()
    print(f"Q{i+1}: {current_q}")
    
    answer = input("Your answer: ")
    next_q = manager.submit_answer(answer)
    
    if not next_q:
        break

# 3. Calculate Scores
scorer = ScoringSystem()
qa_pairs = manager.get_qa_pairs()
conversation = manager.get_conversation_history()

qa_scores = []
for idx, qa in enumerate(qa_pairs):
    # Get expected points for this question
    expected_points = []
    for item in conversation:
        if item['type'] == 'question' and item['question_index'] == idx:
            expected_points = item.get('expected_points', [])
            break
    
    scores = scorer.evaluate_qa_pair(
        qa['question'],
        qa['answer'],
        context,
        expected_points
    )
    qa_scores.append(scores)

final_scores = scorer.calculate_final_score(qa_scores)
feedback = scorer.generate_feedback(final_scores, qa_pairs)

# 4. Generate Reports
repgen = ReportGenerator()

interview_data = {
    'context': context,
    'qa_pairs': qa_pairs,
    'timestamp': datetime.now().isoformat()
}

# Markdown report
markdown = repgen.generate_markdown_report(interview_data, final_scores, feedback)
with open('report.md', 'w') as f:
    f.write(markdown)

# PDF report
repgen.generate_pdf_report(interview_data, final_scores, feedback, 'report.pdf')

print(f"Overall Score: {final_scores['overall_score']}")
```

### Standalone Components

#### Using OCR Only

```python
from modules.screen_capture import ScreenCapture
from modules.ocr_text_extractor import OCRTextExtractor

sc = ScreenCapture()
ocr = OCRTextExtractor()

# From file
image = sc.load_image_from_file(uploaded_file)
text = ocr.extract_text(image)
keywords = ocr.extract_keywords(text)
code = ocr.detect_code_snippets(text)

print(f"Text: {text}")
print(f"Keywords: {keywords}")
print(f"Code: {code}")
```

#### Using Speech-to-Text Only

```python
from modules.speech_to_text import SpeechToText

stt = SpeechToText(model_size="tiny")
result = stt.transcribe_file('recording.wav', language='en')

if not result['error']:
    print(f"Transcription: {result['text']}")
    print(f"Language: {result['language']}")
```

#### Using Scoring Only

```python
from modules.scoring import ScoringSystem

scorer = ScoringSystem()

# Evaluate single answer
scores = scorer.evaluate_qa_pair(
    question="Explain your approach",
    answer="I used a modular architecture...",
    context={'keywords': ['modular', 'architecture']},
    expected_points=['modular design', 'separation of concerns']
)

print(f"Scores: {scores}")
print(f"Correct: {scores['correctness']['is_correct']}")
```

---

## Error Handling

All methods that can fail return error information:

### OCR Methods
```python
try:
    text = ocr.extract_text(image)
except Exception as e:
    print(f"OCR failed: {e}")
```

### Speech-to-Text
```python
result = stt.transcribe_file('audio.wav')
if result['error']:
    print(f"Transcription failed: {result['error']}")
else:
    print(f"Success: {result['text']}")
```

### Report Generation
```python
success = repgen.generate_pdf_report(data, scores, feedback, 'report.pdf')
if not success:
    print("PDF generation failed")
```

---

## Type Hints

All modules use type hints for better IDE support:

```python
from typing import List, Dict, Optional
import numpy as np

def extract_keywords(text: str, min_length: int = 4) -> List[str]:
    ...

def transcribe_file(file_path: str, language: Optional[str] = None) -> Dict:
    ...

def load_image_from_file(file_obj) -> Optional[np.ndarray]:
    ...
```

---

## Testing

### Unit Tests

```python
# tests/test_ocr.py
from modules.ocr_text_extractor import OCRTextExtractor

def test_keyword_extraction():
    ocr = OCRTextExtractor()
    text = "Python Machine Learning Algorithm"
    keywords = ocr.extract_keywords(text)
    assert 'Python' in keywords
    assert 'Machine' in keywords
```

### Integration Tests

```python
# Test full flow
def test_interview_flow():
    # Setup
    qgen = QuestionGenerator(use_openai=False)
    manager = InterviewManager(qgen)
    
    context = {'screen_text': 'test project', 'keywords': ['test']}
    manager.start_interview(context)
    
    # Test question generation
    assert manager.get_current_question() is not None
    
    # Test answer submission
    next_q = manager.submit_answer("test answer")
    assert next_q is not None or manager.is_complete()
```

---

## Best Practices

1. **Always check for None/errors:**
   ```python
   image = sc.load_image_from_file(file)
   if image is None:
       return error_response
   ```

2. **Use context managers for resources:**
   ```python
   with tempfile.NamedTemporaryFile() as tmp:
       # Use temporary file
       pass
   ```

3. **Cache expensive operations:**
   ```python
   if not st.session_state.get('model_loaded'):
       st.session_state.stt_model = SpeechToText()
       st.session_state.model_loaded = True
   ```

4. **Validate inputs:**
   ```python
   if not answer.strip():
       raise ValueError("Answer cannot be empty")
   ```

5. **Handle exceptions gracefully:**
   ```python
   try:
       result = process()
   except Exception as e:
       logger.error(f"Processing failed: {e}")
       return fallback_result()
   ```

---

## Version History

### v2.0
- Added answer validation with expected points
- Enhanced PDF extraction with pdfplumber
- Improved FFmpeg auto-detection
- Performance optimizations

### v1.0
- Initial release
- Basic OCR, STT, interview flow
- Scoring and reporting

---

For implementation examples, see the main `app.py` file and the complete documentation in `DOCUMENTATION.md`.

