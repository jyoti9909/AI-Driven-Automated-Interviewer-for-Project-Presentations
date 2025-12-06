"""
Quick test to verify PDF support
"""

print("Testing PDF library installation...")
print("=" * 50)

try:
    from PyPDF2 import PdfReader
    print("✅ PyPDF2 is installed and working!")
    print("   You can use PDF files in the application.")
except ImportError as e:
    print("❌ PyPDF2 not found")
    print(f"   Error: {e}")
    print("\n   Install with: pip install PyPDF2")

print("=" * 50)
print("\nIf PyPDF2 is installed but the app still shows error:")
print("1. Stop the Streamlit app (Ctrl+C in terminal)")
print("2. Close the browser tab")
print("3. Run: streamlit cache clear")
print("4. Restart: python -m streamlit run app.py")

