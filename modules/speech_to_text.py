"""
Speech-to-Text Module
Converts audio to text using OpenAI Whisper
"""

import whisper
import numpy as np
from typing import Optional, Dict
import tempfile
import os
import subprocess
import sys
import glob
import platform


class SpeechToText:
    """Handles speech-to-text conversion using Whisper"""
    
    def __init__(self, model_size: str = "base"):
        """
        Initialize Whisper model
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
        """
        self.model_size = model_size
        self.model = None
        self.ffmpeg_available = self._check_ffmpeg()
        self._load_model()
    
    def _check_ffmpeg(self) -> bool:
        """Check if ffmpeg is available and auto-configure if needed"""
        # First try if ffmpeg is already in PATH
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE,
                         check=True)
            print("✅ FFmpeg found in PATH")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("FFmpeg not in PATH, searching common locations...")
        
        # If not in PATH, search common Windows locations
        if platform.system() == 'Windows':
            # Get project directory
            project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            possible_paths = [
                # Project bundled FFmpeg
                os.path.join(project_dir, 'ffmpeg_bundle'),
                os.path.join(project_dir, 'ffmpeg'),
                # System locations
                r'C:\ProgramData\chocolatey\bin',
                r'C:\Program Files\ffmpeg\bin',
                r'C:\Program Files (x86)\ffmpeg\bin',
                r'C:\ffmpeg\bin',
                r'C:\Tools\ffmpeg\bin',
            ]
            
            # Also search in user's local app data
            if os.environ.get('LOCALAPPDATA'):
                possible_paths.append(os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'WinGet', 'Packages'))
            
            # Search for ffmpeg.exe
            for base_path in possible_paths:
                if os.path.exists(base_path):
                    # Look for ffmpeg.exe directly
                    ffmpeg_path = os.path.join(base_path, 'ffmpeg.exe')
                    if os.path.exists(ffmpeg_path):
                        print(f"✅ Found FFmpeg at: {ffmpeg_path}")
                        # Add to PATH for this session
                        os.environ['PATH'] = base_path + os.pathsep + os.environ.get('PATH', '')
                        return True
                    
                    # Search in subdirectories (for WinGet installations)
                    for root, dirs, files in os.walk(base_path):
                        if 'ffmpeg.exe' in files:
                            ffmpeg_dir = root
                            ffmpeg_path = os.path.join(ffmpeg_dir, 'ffmpeg.exe')
                            print(f"✅ Found FFmpeg at: {ffmpeg_path}")
                            # Add to PATH for this session
                            os.environ['PATH'] = ffmpeg_dir + os.pathsep + os.environ.get('PATH', '')
                            return True
        
        print("❌ FFmpeg not found in common locations")
        return False
    
    def _load_model(self):
        """Load Whisper model"""
        try:
            print(f"Loading Whisper model: {self.model_size}")
            self.model = whisper.load_model(self.model_size)
            print("Whisper model loaded successfully")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            print("Falling back to tiny model...")
            try:
                self.model = whisper.load_model("tiny")
                self.model_size = "tiny"
            except Exception as e2:
                print(f"Error loading fallback model: {e2}")
                self.model = None
    
    def transcribe_audio(self, audio_data: bytes, language: Optional[str] = None) -> Dict:
        """
        Transcribe audio data to text
        
        Args:
            audio_data: Audio bytes (WAV format expected)
            language: Optional language code (e.g., 'en')
            
        Returns:
            Dictionary with transcription and metadata
        """
        if self.model is None:
            return {
                'text': '',
                'language': None,
                'error': 'Whisper model not loaded'
            }
        
        if not self.ffmpeg_available:
            return {
                'text': '',
                'language': None,
                'error': 'ffmpeg not found. Please install ffmpeg: https://www.gyan.dev/ffmpeg/builds/ or use chocolatey: choco install ffmpeg'
            }
        
        try:
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                tmp_file.write(audio_data)
                tmp_path = tmp_file.name
            
            # Transcribe
            result = self.model.transcribe(
                tmp_path,
                language=language,
                task="transcribe",
                fp16=False  # Disable fp16 for Windows compatibility
            )
            
            # Clean up
            try:
                os.unlink(tmp_path)
            except:
                pass
            
            return {
                'text': result['text'].strip(),
                'language': result.get('language', 'unknown'),
                'segments': result.get('segments', []),
                'error': None
            }
        except Exception as e:
            error_msg = str(e)
            if "ffmpeg" in error_msg.lower() or "file specified" in error_msg.lower():
                error_msg = f"ffmpeg is required but not found. Please install from: https://www.gyan.dev/ffmpeg/builds/. Original error: {error_msg}"
            return {
                'text': '',
                'language': None,
                'error': error_msg
            }
    
    def transcribe_file(self, file_path: str, language: Optional[str] = None) -> Dict:
        """
        Transcribe audio file to text
        
        Args:
            file_path: Path to audio file
            language: Optional language code
            
        Returns:
            Dictionary with transcription and metadata
        """
        if self.model is None:
            return {
                'text': '',
                'language': None,
                'error': 'Whisper model not loaded'
            }
        
        if not self.ffmpeg_available:
            return {
                'text': '',
                'language': None,
                'error': 'ffmpeg not found. Please install ffmpeg: https://www.gyan.dev/ffmpeg/builds/ or use chocolatey: choco install ffmpeg'
            }
        
        try:
            result = self.model.transcribe(
                file_path,
                language=language,
                task="transcribe",
                fp16=False  # Disable fp16 for Windows compatibility
            )
            
            return {
                'text': result['text'].strip(),
                'language': result.get('language', 'unknown'),
                'segments': result.get('segments', []),
                'error': None
            }
        except Exception as e:
            error_msg = str(e)
            if "ffmpeg" in error_msg.lower() or "file specified" in error_msg.lower():
                error_msg = f"ffmpeg is required but not found. Please install from: https://www.gyan.dev/ffmpeg/builds/. Original error: {error_msg}"
            return {
                'text': '',
                'language': None,
                'error': error_msg
            }
    
    def get_model_info(self) -> Dict:
        """Get information about the loaded model"""
        return {
            'model_size': self.model_size,
            'loaded': self.model is not None
        }

