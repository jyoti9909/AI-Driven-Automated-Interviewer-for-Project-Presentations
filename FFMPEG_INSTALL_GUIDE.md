# FFmpeg Installation Guide for Windows

FFmpeg is required for audio processing with Whisper. Here are the easiest ways to install it:

## Option 1: Using Windows Package Manager (Recommended)

Open PowerShell as Administrator and run:

```powershell
winget install Gyan.FFmpeg
```

After installation, **restart your PowerShell/Terminal**.

## Option 2: Using Chocolatey

If you have Chocolatey installed:

```powershell
choco install ffmpeg -y
```

After installation, **restart your PowerShell/Terminal**.

## Option 3: Manual Installation

1. **Download FFmpeg:**
   - Go to: https://www.gyan.dev/ffmpeg/builds/
   - Download: `ffmpeg-release-essentials.zip` (~70MB)

2. **Extract:**
   - Extract the zip file to: `C:\ffmpeg`
   - You should have: `C:\ffmpeg\bin\ffmpeg.exe`

3. **Add to PATH:**
   - Press `Win + X` and select "System"
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", find and select "Path"
   - Click "Edit" → "New"
   - Add: `C:\ffmpeg\bin`
   - Click "OK" on all windows

4. **Verify Installation:**
   - Open a NEW PowerShell window
   - Run: `ffmpeg -version`
   - You should see version information

## Quick Test

After installation, verify ffmpeg is working:

```powershell
ffmpeg -version
```

If you see version information, you're all set!

## Troubleshooting

### "ffmpeg is not recognized"

This means ffmpeg is either:
- Not installed
- Not in your PATH
- You need to restart your terminal/PowerShell

**Solution:** Close all PowerShell/Terminal windows and open a new one.

### Still Having Issues?

Run the automated setup script:

```powershell
python setup_ffmpeg.py
```

This will attempt to download and configure ffmpeg automatically.

---

**After installing ffmpeg, restart the application:**

```powershell
python -m streamlit run app.py
```

