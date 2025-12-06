"""
Setup script for AI-Driven Automated Interviewer
"""

import subprocess
import sys
import os


def check_tesseract():
    """Check if Tesseract is installed"""
    try:
        import pytesseract
        # Try to get version
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract OCR found (version: {version})")
        return True
    except Exception as e:
        print(f"⚠️  Tesseract OCR not found: {e}")
        print("   Please install Tesseract:")
        print("   - Windows: https://github.com/UB-Mannheim/tesseract/wiki")
        print("   - macOS: brew install tesseract")
        print("   - Linux: sudo apt-get install tesseract-ocr")
        return False


def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False


def main():
    """Main setup function"""
    print("🚀 Setting up AI-Driven Automated Interviewer\n")
    
    # Install requirements
    if not install_requirements():
        return
    
    print("\n" + "="*50)
    print("Checking system dependencies...")
    print("="*50 + "\n")
    
    # Check Tesseract
    tesseract_ok = check_tesseract()
    
    print("\n" + "="*50)
    print("Setup Summary")
    print("="*50)
    print(f"Python packages: ✅ Installed")
    print(f"Tesseract OCR: {'✅ Found' if tesseract_ok else '⚠️  Not found (required for OCR)'}")
    print("\n📝 Next steps:")
    print("   1. If Tesseract is missing, install it (see instructions above)")
    print("   2. (Optional) Set OPENAI_API_KEY environment variable for better questions")
    print("   3. Run: streamlit run app.py")
    print("\n✨ Setup complete!")


if __name__ == "__main__":
    main()

