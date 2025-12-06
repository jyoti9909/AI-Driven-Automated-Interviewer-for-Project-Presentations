"""
Automatic FFmpeg installer and configurator
Downloads and sets up FFmpeg if not found
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
from pathlib import Path
import shutil

def check_ffmpeg():
    """Check if ffmpeg is available"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              timeout=5)
        return result.returncode == 0
    except:
        return False

def download_ffmpeg():
    """Download and extract FFmpeg for Windows"""
    print("=" * 60)
    print("Downloading FFmpeg...")
    print("=" * 60)
    
    # Create ffmpeg directory in project
    project_dir = Path(__file__).parent
    ffmpeg_dir = project_dir / "ffmpeg_bundle"
    ffmpeg_dir.mkdir(exist_ok=True)
    
    # Download FFmpeg essentials (smaller, ~70MB)
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = ffmpeg_dir / "ffmpeg.zip"
    
    try:
        print(f"Downloading from: {url}")
        print("This may take a few minutes (downloading ~70MB)...")
        print()
        
        # Download with progress
        def reporthook(count, block_size, total_size):
            percent = int(count * block_size * 100 / total_size)
            sys.stdout.write(f"\rProgress: {percent}%")
            sys.stdout.flush()
        
        urllib.request.urlretrieve(url, zip_path, reporthook)
        print("\n✅ Download complete!")
        
        # Extract
        print("\nExtracting FFmpeg...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(ffmpeg_dir)
        
        # Find the bin directory
        for item in ffmpeg_dir.iterdir():
            if item.is_dir() and item.name.startswith('ffmpeg'):
                bin_dir = item / 'bin'
                if bin_dir.exists():
                    print(f"✅ FFmpeg extracted to: {bin_dir}")
                    
                    # Clean up zip
                    zip_path.unlink()
                    
                    # Add to PATH for this session
                    os.environ['PATH'] = str(bin_dir) + os.pathsep + os.environ.get('PATH', '')
                    
                    # Create a batch file to add to PATH permanently
                    create_path_script(bin_dir)
                    
                    return str(bin_dir)
        
        print("❌ Error: Could not find FFmpeg bin directory after extraction")
        return None
        
    except Exception as e:
        print(f"\n❌ Error downloading/extracting FFmpeg: {e}")
        return None

def create_path_script(ffmpeg_bin):
    """Create a script to add FFmpeg to PATH permanently"""
    script_path = Path(__file__).parent / "add_ffmpeg_to_path.bat"
    
    with open(script_path, 'w') as f:
        f.write('@echo off\n')
        f.write('echo Adding FFmpeg to system PATH...\n')
        f.write(f'setx PATH "%PATH%;{ffmpeg_bin}"\n')
        f.write('echo.\n')
        f.write('echo FFmpeg added to PATH!\n')
        f.write('echo Please restart your terminal/PowerShell for changes to take effect.\n')
        f.write('pause\n')
    
    print(f"\n📝 Created script: {script_path}")
    print("   Run this script to add FFmpeg to PATH permanently")

def try_winget_install():
    """Try to install FFmpeg using winget"""
    print("\nTrying to install FFmpeg using Windows Package Manager...")
    try:
        result = subprocess.run([
            'winget', 'install', '--id=Gyan.FFmpeg',
            '--accept-source-agreements',
            '--accept-package-agreements',
            '--silent'
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ FFmpeg installed via winget!")
            print("⚠️  You need to restart your terminal for it to work")
            return True
        else:
            print("⚠️  winget install failed or already installed")
            return False
    except Exception as e:
        print(f"⚠️  winget not available: {e}")
        return False

def main():
    print("=" * 60)
    print("FFmpeg Auto-Installer")
    print("=" * 60)
    print()
    
    # Check if already available
    if check_ffmpeg():
        print("✅ FFmpeg is already installed and available!")
        print("\nYou're all set! Audio transcription will work.")
        return 0
    
    print("❌ FFmpeg not found in PATH")
    print()
    
    # Try Method 1: winget
    print("Method 1: Using Windows Package Manager (winget)")
    if try_winget_install():
        print("\n" + "=" * 60)
        print("Installation Complete!")
        print("=" * 60)
        print("\n⚠️  IMPORTANT: You must restart your terminal/PowerShell")
        print("   and then restart the Streamlit application")
        print("\n   Close this terminal and open a new one, then run:")
        print("   python -m streamlit run app.py")
        return 0
    
    # Try Method 2: Direct download
    print("\nMethod 2: Direct Download")
    print("(This will download FFmpeg and bundle it with the app)")
    print()
    
    response = input("Download FFmpeg now? (y/n): ").lower()
    if response == 'y':
        ffmpeg_path = download_ffmpeg()
        if ffmpeg_path:
            print("\n" + "=" * 60)
            print("Installation Complete!")
            print("=" * 60)
            print(f"\nFFmpeg installed to: {ffmpeg_path}")
            print("\nThe application will now automatically use this FFmpeg.")
            print("Restart the Streamlit app and audio transcription will work!")
            print("\nOptional: Run 'add_ffmpeg_to_path.bat' to add to system PATH")
            return 0
        else:
            print("\n❌ Automatic download failed")
    
    # Manual instructions
    print("\n" + "=" * 60)
    print("Manual Installation Instructions")
    print("=" * 60)
    print("\n1. Download FFmpeg from:")
    print("   https://www.gyan.dev/ffmpeg/builds/")
    print("\n2. Extract to C:\\ffmpeg\\")
    print("\n3. Add C:\\ffmpeg\\bin to your PATH")
    print("\n4. Restart terminal and the application")
    
    return 1

if __name__ == "__main__":
    sys.exit(main())

