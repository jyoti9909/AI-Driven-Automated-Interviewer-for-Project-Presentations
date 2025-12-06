"""
Quick Dependency Checker
Checks if Tesseract OCR and FFmpeg are installed
"""

import subprocess
import sys
import os

def check_tesseract():
    """Check if Tesseract is installed"""
    print("Checking Tesseract OCR...")
    
    # Check common Windows paths
    paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    ]
    
    for path in paths:
        if os.path.exists(path):
            print(f"✅ Tesseract found at: {path}")
            return True
    
    # Try command line
    try:
        subprocess.run(['tesseract', '--version'], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE,
                      check=True)
        print("✅ Tesseract found in PATH")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Tesseract NOT found")
        print("\n   Install with: winget install UB-Mannheim.TesseractOCR")
        print("   Or download: https://github.com/UB-Mannheim/tesseract/wiki\n")
        return False

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    print("Checking FFmpeg...")
    
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE,
                      check=True)
        print("✅ FFmpeg found\n")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg NOT found")
        print("\n   Install with: winget install Gyan.FFmpeg")
        print("   Or download: https://www.gyan.dev/ffmpeg/builds/\n")
        return False

def main():
    print("=" * 60)
    print("AI Interviewer - Dependency Check")
    print("=" * 60)
    print()
    
    tesseract_ok = check_tesseract()
    ffmpeg_ok = check_ffmpeg()
    
    print("=" * 60)
    print("Summary:")
    print("=" * 60)
    
    if tesseract_ok and ffmpeg_ok:
        print("✅ All dependencies are installed!")
        print("\nYou can now run: python -m streamlit run app.py")
        return 0
    else:
        print("⚠️  Some dependencies are missing:")
        if not tesseract_ok:
            print("   - Tesseract OCR (required for image text extraction)")
        if not ffmpeg_ok:
            print("   - FFmpeg (required for audio transcription)")
        
        print("\n💡 Install missing dependencies and restart the application.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

