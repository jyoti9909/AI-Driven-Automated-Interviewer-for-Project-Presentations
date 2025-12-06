"""
Automatic ffmpeg installer for Windows
Downloads and sets up ffmpeg if not found
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil
from pathlib import Path

def check_ffmpeg():
    """Check if ffmpeg is available"""
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE,
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def download_ffmpeg():
    """Download and extract ffmpeg for Windows"""
    print("Downloading ffmpeg...")
    
    # Create ffmpeg directory
    ffmpeg_dir = Path(__file__).parent / "ffmpeg"
    ffmpeg_dir.mkdir(exist_ok=True)
    
    # Download ffmpeg essentials build (smaller, ~70MB)
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = ffmpeg_dir / "ffmpeg.zip"
    
    try:
        print(f"Downloading from {url}")
        print("This may take a few minutes...")
        urllib.request.urlretrieve(url, zip_path)
        
        print("Extracting ffmpeg...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(ffmpeg_dir)
        
        # Find the extracted bin folder
        for item in ffmpeg_dir.iterdir():
            if item.is_dir() and item.name.startswith('ffmpeg'):
                bin_dir = item / 'bin'
                if bin_dir.exists():
                    # Add to PATH for this session
                    os.environ['PATH'] = str(bin_dir) + os.pathsep + os.environ['PATH']
                    
                    print(f"\n✅ ffmpeg installed successfully!")
                    print(f"Location: {bin_dir}")
                    print("\nIMPORTANT: Add this to your PATH permanently:")
                    print(f"   {bin_dir}")
                    print("\nOr restart the application to use ffmpeg.")
                    
                    # Clean up zip file
                    zip_path.unlink()
                    return str(bin_dir)
        
        print("❌ Error: Could not find ffmpeg bin directory")
        return None
        
    except Exception as e:
        print(f"❌ Error downloading ffmpeg: {e}")
        print("\nPlease install manually from: https://www.gyan.dev/ffmpeg/builds/")
        return None

def main():
    print("=" * 50)
    print("ffmpeg Setup for AI Interviewer")
    print("=" * 50)
    print()
    
    if check_ffmpeg():
        print("✅ ffmpeg is already installed and available!")
        return 0
    
    print("❌ ffmpeg not found. Installing...")
    print()
    
    result = download_ffmpeg()
    
    if result:
        print("\n" + "=" * 50)
        print("Setup complete! Please restart the application.")
        print("=" * 50)
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())

