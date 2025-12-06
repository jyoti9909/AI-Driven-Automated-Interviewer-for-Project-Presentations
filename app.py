"""
AI-Driven Automated Interviewer for Project Presentations
Streamlit Web Application
"""

import streamlit as st
import time
import os
from datetime import datetime
import tempfile
import io

# Import modules
from modules.screen_capture import ScreenCapture
from modules.ocr_text_extractor import OCRTextExtractor
from modules.speech_to_text import SpeechToText
from modules.question_generator import QuestionGenerator
from modules.interview_manager import InterviewManager
from modules.scoring import ScoringSystem
from modules.report_generator import ReportGenerator

# PDF processing
try:
    from PyPDF2 import PdfReader
    PDF_SUPPORT = True
except ImportError:
    try:
        from pypdf import PdfReader
        PDF_SUPPORT = True
    except ImportError:
        PDF_SUPPORT = False

# Enhanced PDF extraction
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="AI Interviewer",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'interview_manager' not in st.session_state:
    st.session_state.interview_manager = None
if 'scoring_system' not in st.session_state:
    st.session_state.scoring_system = ScoringSystem()
if 'report_generator' not in st.session_state:
    st.session_state.report_generator = ReportGenerator()
if 'context' not in st.session_state:
    st.session_state.context = {}
if 'stt_model' not in st.session_state:
    st.session_state.stt_model = None
if 'interview_started' not in st.session_state:
    st.session_state.interview_started = False
if 'current_answer' not in st.session_state:
    st.session_state.current_answer = ""
if 'image_processed' not in st.session_state:
    st.session_state.image_processed = False
if 'audio_processed' not in st.session_state:
    st.session_state.audio_processed = False
if 'last_uploaded_image' not in st.session_state:
    st.session_state.last_uploaded_image = None
if 'last_audio_data' not in st.session_state:
    st.session_state.last_audio_data = None


def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file with improved extraction"""
    
    # Try pdfplumber first (better for complex layouts, tables, multi-column)
    if PDFPLUMBER_AVAILABLE:
        try:
            return extract_with_pdfplumber(pdf_file)
        except Exception as e:
            print(f"pdfplumber extraction failed: {e}, falling back to PyPDF2")
    
    # Fallback to PyPDF2
    try:
        return extract_with_pypdf2(pdf_file)
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def extract_with_pdfplumber(pdf_file):
    """Extract text using pdfplumber (better for complex PDFs)"""
    import pdfplumber
    
    # Reset file pointer
    pdf_file.seek(0)
    
    all_text = []
    
    with pdfplumber.open(pdf_file) as pdf:
        total_pages = len(pdf.pages)
        
        for page_num, page in enumerate(pdf.pages, 1):
            # Add page separator
            all_text.append(f"\n--- Page {page_num} of {total_pages} ---\n")
            
            # Extract text with layout preservation
            page_text = page.extract_text(layout=True)
            
            if not page_text:
                # Try without layout mode
                page_text = page.extract_text()
            
            if page_text:
                all_text.append(page_text)
                all_text.append("\n")
            
            # Extract tables separately if present
            tables = page.extract_tables()
            if tables:
                all_text.append("\n[Tables found on this page]\n")
                for table_idx, table in enumerate(tables, 1):
                    all_text.append(f"\nTable {table_idx}:\n")
                    for row in table:
                        if row:
                            all_text.append(" | ".join([str(cell) if cell else "" for cell in row]))
                            all_text.append("\n")
                    all_text.append("\n")
    
    full_text = "".join(all_text)
    return clean_extracted_text(full_text)


def extract_with_pypdf2(pdf_file):
    """Extract text using PyPDF2 (fallback method)"""
    # Reset file pointer to beginning
    pdf_file.seek(0)
    
    pdf_reader = PdfReader(pdf_file)
    total_pages = len(pdf_reader.pages)
    
    all_text = []
    
    for page_num, page in enumerate(pdf_reader.pages, 1):
        # Add page separator
        all_text.append(f"\n--- Page {page_num} of {total_pages} ---\n")
        
        # Try layout mode first
        try:
            page_text = page.extract_text(extraction_mode="layout")
        except:
            page_text = None
        
        # If layout mode doesn't work, try plain mode
        if not page_text or len(page_text.strip()) < 10:
            page_text = page.extract_text()
        
        if page_text and page_text.strip():
            all_text.append(page_text)
            all_text.append("\n")
    
    # Combine all text
    full_text = "".join(all_text)
    
    # Clean up the text
    full_text = clean_extracted_text(full_text)
    
    return full_text.strip()


def clean_extracted_text(text):
    """Clean and format extracted text"""
    import re
    
    # Remove excessive whitespace while preserving paragraph breaks
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Remove excessive spaces
        line = re.sub(r' +', ' ', line)
        # Keep the line even if it's just whitespace (for formatting)
        cleaned_lines.append(line.strip())
    
    # Join lines back together
    cleaned_text = '\n'.join(cleaned_lines)
    
    # Remove more than 2 consecutive newlines
    cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
    
    return cleaned_text


def initialize_models():
    """Initialize AI models"""
    if st.session_state.stt_model is None:
        with st.spinner("Loading Whisper model (using tiny model for faster performance)..."):
            try:
                # Use tiny model by default for better performance and less hanging
                st.session_state.stt_model = SpeechToText(model_size="tiny")
            except Exception as e:
                st.error(f"Error loading Whisper model: {e}")
                st.session_state.stt_model = None


def main():
    """Main application"""
    st.title("🎤 AI-Driven Automated Interviewer")
    st.markdown("### For Project Presentations")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Model info
        if st.session_state.stt_model:
            st.success("✅ Whisper model loaded")
        else:
            st.warning("⚠️ Whisper model not loaded")
        
        # Model selection
        use_openai = st.checkbox("Use OpenAI API (requires API key)", value=False)
        if use_openai:
            api_key = st.text_input("OpenAI API Key", type="password", 
                                  help="Enter your OpenAI API key")
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
        
        st.markdown("---")
        st.markdown("### 📋 Instructions")
        st.markdown("""
        1. **Upload** a screenshot of your project
        2. **Record** or upload audio explaining your project
        3. **Click Transcribe** to process audio
        4. **Start Interview** to begin
        5. **Answer** the AI's questions
        6. **Review** your score and feedback
        """)
        
        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Images are auto-processed when uploaded
        - Audio requires clicking "Transcribe"
        - Results are cached (no re-processing)
        - Using tiny Whisper model for speed
        """)
    
    # Initialize models
    initialize_models()
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📸 Upload Content", "🎙️ Interview", "📊 Results", "📄 Report"])
    
    # Tab 1: Upload Content
    with tab1:
        st.header("Step 1: Upload Project Content")
        
        # Add reset button
        col_reset1, col_reset2 = st.columns([3, 1])
        with col_reset2:
            if st.button("🔄 Reset All", help="Clear all uploaded content and start fresh"):
                st.session_state.context = {}
                st.session_state.image_processed = False
                st.session_state.audio_processed = False
                st.session_state.last_uploaded_image = None
                st.session_state.last_audio_data = None
                st.session_state.interview_started = False
                st.session_state.interview_manager = None
                st.success("✅ Reset complete! Upload new content.")
                st.rerun()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📸 Document Upload")
            uploaded_image = st.file_uploader(
                "Upload a screenshot or PDF of your project",
                type=['png', 'jpg', 'jpeg', 'pdf'],
                help="Upload an image or PDF of your project slides, UI, or code",
                key="image_uploader"
            )
            
            if uploaded_image:
                # Check file type
                is_pdf = uploaded_image.name.lower().endswith('.pdf')
                
                if not is_pdf:
                    st.image(uploaded_image, caption="Uploaded Image", width='stretch')
                else:
                    st.info(f"📄 PDF uploaded: {uploaded_image.name}")
                
                # Check if this is a new file
                file_id = uploaded_image.name + str(uploaded_image.size)
                is_new_file = (st.session_state.last_uploaded_image != file_id)
                
                # Only process if new file or not yet processed
                if is_new_file or not st.session_state.image_processed:
                    with st.spinner(f"Extracting text from {'PDF' if is_pdf else 'image'}..."):
                        try:
                            screen_text = ""
                            
                            if is_pdf:
                                # Process PDF
                                if not PDF_SUPPORT:
                                    raise Exception("PDF support not available. Install PyPDF2: pip install PyPDF2")
                                
                                screen_text = extract_text_from_pdf(uploaded_image)
                                
                                if not screen_text:
                                    st.warning("⚠️ No text detected in PDF. The PDF might be image-based.")
                                    screen_text = ""
                            else:
                                # Process image with OCR
                                screen_capture = ScreenCapture()
                                image = screen_capture.load_image_from_file(uploaded_image)
                                
                                if image is not None:
                                    ocr_extractor = OCRTextExtractor()
                                    preprocessed = screen_capture.preprocess_image(image)
                                    screen_text = ocr_extractor.extract_text(preprocessed if preprocessed is not None else image)
                                    
                                    if not screen_text:
                                        st.warning("⚠️ No text detected in image. Please ensure the image contains readable text.")
                                        screen_text = ""
                            
                            # Extract keywords and code snippets
                            if screen_text:
                                ocr_extractor = OCRTextExtractor()
                                keywords = ocr_extractor.extract_keywords(screen_text)
                                code_snippets = ocr_extractor.detect_code_snippets(screen_text)
                            else:
                                keywords = []
                                code_snippets = []
                            
                            st.session_state.context['screen_text'] = screen_text
                            st.session_state.context['keywords'] = keywords
                            st.session_state.context['code_snippets'] = code_snippets
                            st.session_state.image_processed = True
                            st.session_state.last_uploaded_image = file_id
                            
                            st.success(f"✅ {'PDF' if is_pdf else 'Image'} processed successfully!")
                        except Exception as e:
                            error_str = str(e)
                            st.error(f"❌ Error processing {'PDF' if is_pdf else 'image'}: {error_str}")
                            
                            if is_pdf and "PyPDF2" in error_str:
                                st.info("""
                                **📄 PDF Support Missing**
                                
                                Install with:
                                ```
                                pip install PyPDF2
                                ```
                                Then restart the application.
                                """)
                            elif "tesseract" in error_str.lower() or "not found" in error_str.lower():
                                st.info("""
                                **🔧 Tesseract OCR Installation Required**
                                
                                Quick Fix:
                                ```
                                winget install UB-Mannheim.TesseractOCR
                                ```
                                
                                Then **restart this application**.
                                
                                Alternative: Download from https://github.com/UB-Mannheim/tesseract/wiki
                                """)
                
                # Show cached results if available
                if st.session_state.context.get('screen_text'):
                    extracted_text = st.session_state.context['screen_text']
                    
                    # Show statistics
                    st.write(f"**📊 Extracted:** {len(extracted_text)} characters, {len(extracted_text.split())} words, {len(extracted_text.splitlines())} lines")
                    
                    # Show keywords
                    if st.session_state.context.get('keywords'):
                        st.write(f"**🔑 Keywords:** {', '.join(st.session_state.context['keywords'][:15])}")
                    
                    # Show full text in expandable section
                    with st.expander("📄 View Full Extracted Text", expanded=True):
                        st.text_area(
                            "Full Content",
                            extracted_text,
                            height=400,
                            key="extracted_text_display",
                            help="Full text extracted from your document"
                        )
                    
                    # Show preview
                    st.markdown("**Preview (first 300 chars):**")
                    st.info(extracted_text[:300] + ("..." if len(extracted_text) > 300 else ""))
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Extracted Text",
                        data=extracted_text,
                        file_name="extracted_text.txt",
                        mime="text/plain",
                        help="Download the full extracted text as a .txt file"
                    )
        
        with col2:
            st.subheader("🎙️ Audio Recording")
            st.markdown("Record or upload audio explaining your project (30+ seconds)")
            
            audio_source = st.radio("Audio Source", ["Record", "Upload"], key="audio_source_radio")
            
            audio_data = None
            audio_id = None
            
            if audio_source == "Record":
                audio_data = st.audio_input("Record your explanation")
                if audio_data:
                    audio_bytes = audio_data.read()
                    audio_data.seek(0)  # Reset for display
                    audio_id = f"recorded_{len(audio_bytes)}"
                    audio_data = audio_bytes
            else:
                uploaded_audio = st.file_uploader(
                    "Upload audio file",
                    type=['wav', 'mp3', 'm4a'],
                    help="Upload an audio file of your explanation",
                    key="audio_uploader"
                )
                if uploaded_audio:
                    audio_data = uploaded_audio.read()
                    audio_id = uploaded_audio.name + str(len(audio_data))
            
            if audio_data:
                st.audio(audio_data, format='audio/wav')
                
                # Check if this is new audio
                is_new_audio = (st.session_state.last_audio_data != audio_id)
                
                # Auto-transcribe button or show cached result
                if is_new_audio or not st.session_state.audio_processed:
                    if st.button("🔄 Transcribe Audio", key="transcribe_btn"):
                        with st.spinner("Transcribing audio with Whisper (this may take a moment)..."):
                            if st.session_state.stt_model:
                                try:
                                    # Save to temp file for Whisper
                                    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                                        tmp_file.write(audio_data)
                                        tmp_path = tmp_file.name
                                    
                                    result = st.session_state.stt_model.transcribe_file(tmp_path)
                                    
                                    try:
                                        os.unlink(tmp_path)
                                    except:
                                        pass
                                    
                                    if result['error']:
                                        st.error(f"❌ Transcription error: {result['error']}")
                                        
                                        # Show helpful instructions if ffmpeg is the issue
                                        if "ffmpeg" in result['error'].lower():
                                            st.info("""
                                            **FFmpeg is required for audio processing!**
                                            
                                            Quick fix: Open PowerShell as Admin and run:
                                            ```
                                            winget install Gyan.FFmpeg
                                            ```
                                            Then restart this application.
                                            
                                            📄 See `FFMPEG_INSTALL_GUIDE.md` for more options.
                                            """)
                                    else:
                                        speech_text = result['text']
                                        st.session_state.context['speech_text'] = speech_text
                                        st.session_state.audio_processed = True
                                        st.session_state.last_audio_data = audio_id
                                        st.success("✅ Audio transcribed successfully!")
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Error during transcription: {str(e)}")
                            else:
                                st.error("Speech-to-text model not loaded. Please restart the application.")
                
                # Show cached transcription if available
                if st.session_state.context.get('speech_text'):
                    st.success("✅ Audio transcribed!")
                    st.text_area("Transcription", st.session_state.context['speech_text'], height=150, key="transcription_display")
        
        # Start Interview Button
        if st.session_state.context.get('screen_text') or st.session_state.context.get('speech_text'):
            st.markdown("---")
            if st.button("🚀 Start Interview", type="primary", use_container_width=True):
                # Initialize question generator
                question_gen = QuestionGenerator(use_openai=use_openai)
                
                # Initialize interview manager
                st.session_state.interview_manager = InterviewManager(question_gen)
                st.session_state.interview_manager.start_interview(st.session_state.context)
                st.session_state.interview_started = True
                
                st.success("✅ Interview started! Go to the Interview tab.")
                st.balloons()
    
    # Tab 2: Interview
    with tab2:
        st.header("Step 2: Answer Interview Questions")
        
        if not st.session_state.interview_started or st.session_state.interview_manager is None:
            st.warning("⚠️ Please upload content and start the interview first.")
        else:
            manager = st.session_state.interview_manager
            
            # Display current question
            current_question = manager.get_current_question()
            
            if current_question:
                st.subheader(f"❓ Question {manager.current_question_index + 1} of {manager.max_questions}")
                st.info(current_question)
                
                # Answer input - use dynamic key based on question index
                st.subheader("💬 Your Answer")
                answer = st.text_area(
                    "Type or paste your answer here",
                    height=200,
                    key=f"answer_input_{manager.current_question_index}",
                    placeholder="Enter your detailed answer here..."
                )
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("📤 Submit Answer", type="primary", key=f"submit_btn_{manager.current_question_index}"):
                        if answer.strip():
                            # Submit answer
                            next_question = manager.submit_answer(answer)
                            
                            if next_question:
                                st.success("✅ Answer submitted!")
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.success("✅ Interview completed!")
                                st.info("Go to the Results tab to see your scores.")
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.warning("⚠️ Please enter an answer before submitting.")
            else:
                st.success("🎉 Interview Completed!")
                st.info("Go to the **Results** tab to view your scores and feedback.")
                st.session_state.interview_started = False
            
            # Progress indicator
            if not manager.is_complete():
                st.markdown("---")
                progress = manager.current_question_index / manager.max_questions
                st.progress(progress)
                st.caption(f"Progress: {manager.current_question_index}/{manager.max_questions} questions answered")
            
            # Conversation history
            st.markdown("---")
            st.subheader("📝 Conversation History")
            
            if not manager.conversation_history:
                st.info("No conversation history yet. Answer the question above to begin.")
            else:
                conversation = manager.get_conversation_history()
                
                for item in conversation:
                    if item['type'] == 'question':
                        st.markdown(f"**🤖 Q{item['question_index'] + 1}:** {item['content']}")
                    else:
                        st.markdown(f"**👤 A{item['question_index'] + 1}:** {item['content'][:200]}{'...' if len(item['content']) > 200 else ''}")
                    st.markdown("")
    
    # Tab 3: Results
    with tab3:
        st.header("Step 3: View Results")
        
        if st.session_state.interview_manager is None:
            st.warning("⚠️ No interview data available. Please complete an interview first.")
        else:
            manager = st.session_state.interview_manager
            qa_pairs = manager.get_qa_pairs()
            
            if not qa_pairs:
                st.warning("⚠️ No Q&A pairs found. Please complete the interview first.")
            else:
                # Calculate scores
                with st.spinner("Calculating scores..."):
                    scoring_system = st.session_state.scoring_system
                    qa_scores = []
                    
                    # Get conversation history with expected points
                    conversation = manager.get_conversation_history()
                    
                    for idx, qa in enumerate(qa_pairs):
                        # Find expected points for this question
                        expected_points = []
                        for item in conversation:
                            if (item['type'] == 'question' and 
                                item.get('question_index') == idx and
                                'expected_points' in item):
                                expected_points = item['expected_points']
                                break
                        
                        scores = scoring_system.evaluate_qa_pair(
                            qa['question'],
                            qa['answer'],
                            st.session_state.context,
                            expected_points
                        )
                        qa_scores.append(scores)
                    
                    final_scores = scoring_system.calculate_final_score(qa_scores)
                    feedback = scoring_system.generate_feedback(final_scores, qa_pairs)
                
                # Display overall score
                overall_score = final_scores['overall_score']
                st.metric("Overall Score", f"{overall_score}/100")
                
                # Score breakdown
                st.subheader("📊 Score Breakdown")
                breakdown = final_scores['breakdown']
                rubric = final_scores['rubric']
                
                for criterion, score in breakdown.items():
                    weight = rubric[criterion]['weight'] * 100
                    st.write(f"**{criterion.replace('_', ' ').title()}** ({weight}% weight)")
                    st.progress(score / 100)
                    st.caption(f"Score: {score:.1f}/100 - {rubric[criterion]['description']}")
                
                # Answer Correctness Check
                st.subheader("✅ Answer Correctness")
                
                for idx, (qa, scores) in enumerate(zip(qa_pairs, qa_scores), 1):
                    with st.expander(f"Question {idx}: Review", expanded=False):
                        st.markdown(f"**Question:** {qa['question']}")
                        st.markdown(f"**Your Answer:** {qa['answer'][:200]}...")
                        
                        if 'correctness' in scores:
                            correctness = scores['correctness']
                            is_correct = correctness['is_correct']
                            percent = correctness['correctness_percent']
                            
                            # Show correctness status
                            if is_correct:
                                st.success(f"✅ Answer is correct ({percent}% match)")
                            elif percent >= 50:
                                st.warning(f"⚠️ Answer is partially correct ({percent}% match)")
                            else:
                                st.error(f"❌ Answer needs improvement ({percent}% match)")
                            
                            # Show what was found
                            if correctness['found_points']:
                                st.markdown("**✅ Key points mentioned:**")
                                for point in correctness['found_points']:
                                    st.markdown(f"- ✓ {point}")
                            
                            if correctness['partially_found']:
                                st.markdown("**⚠️ Partially mentioned:**")
                                for point in correctness['partially_found']:
                                    st.markdown(f"- ~ {point}")
                            
                            if correctness['missing_points']:
                                st.markdown("**❌ Missing key points:**")
                                for point in correctness['missing_points']:
                                    st.markdown(f"- ✗ {point}")
                        else:
                            st.info("No expected points available for this question")
                
                st.markdown("---")
                
                # Feedback
                st.subheader("💡 Overall Feedback")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### ✅ Strengths")
                    strengths = feedback['strengths']
                    if strengths:
                        for strength in strengths:
                            st.success(f"**{strength['criterion']}** ({strength['score']}/100)")
                            st.caption(strength['description'])
                    else:
                        st.info("No specific strengths identified.")
                
                with col2:
                    st.markdown("### ⚠️ Areas for Improvement")
                    weaknesses = feedback['weaknesses']
                    if weaknesses:
                        for weakness in weaknesses:
                            st.warning(f"**{weakness['criterion']}** ({weakness['score']}/100)")
                            st.caption(weakness['description'])
                    else:
                        st.info("No major weaknesses identified.")
                
                st.markdown("### 💬 Suggestions")
                suggestions = feedback['suggestions']
                for i, suggestion in enumerate(suggestions, 1):
                    st.write(f"{i}. {suggestion}")
                
                # Store data for report generation
                st.session_state.report_data = {
                    'context': st.session_state.context,
                    'qa_pairs': qa_pairs,
                    'final_scores': final_scores,
                    'feedback': feedback,
                    'question_count': len(qa_pairs),
                    'duration': 'N/A'
                }
    
    # Tab 4: Report
    with tab4:
        st.header("Step 4: Generate Report")
        
        if 'report_data' not in st.session_state:
            st.warning("⚠️ No interview data available. Please complete an interview and view results first.")
        else:
            report_data = st.session_state.report_data
            report_gen = st.session_state.report_generator
            
            # Generate markdown
            st.subheader("📝 Markdown Report")
            markdown_content = report_gen.generate_markdown(report_data)
            st.code(markdown_content, language='markdown')
            
            # Download buttons
            col1, col2 = st.columns(2)
            
            with col1:
                st.download_button(
                    label="📥 Download Markdown",
                    data=markdown_content,
                    file_name=f"interview_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                )
            
            with col2:
                if st.button("📄 Generate PDF Report"):
                    with st.spinner("Generating PDF..."):
                        pdf_path = f"interview_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                        try:
                            report_gen.generate_pdf(report_data, pdf_path)
                            st.success("✅ PDF generated successfully!")
                            
                            with open(pdf_path, 'rb') as pdf_file:
                                st.download_button(
                                    label="📥 Download PDF",
                                    data=pdf_file.read(),
                                    file_name=pdf_path,
                                    mime="application/pdf"
                                )
                        except Exception as e:
                            st.error(f"Error generating PDF: {e}")


if __name__ == "__main__":
    main()

