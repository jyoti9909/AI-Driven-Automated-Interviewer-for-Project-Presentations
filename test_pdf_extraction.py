"""
Test PDF extraction capabilities
"""

import sys

print("=" * 60)
print("PDF Extraction Test")
print("=" * 60)

# Test PyPDF2
print("\n1. Testing PyPDF2...")
try:
    from PyPDF2 import PdfReader
    print("   ✅ PyPDF2 installed and ready")
except ImportError as e:
    print(f"   ❌ PyPDF2 not available: {e}")

# Test pdfplumber
print("\n2. Testing pdfplumber...")
try:
    import pdfplumber
    print("   ✅ pdfplumber installed and ready")
    print("   ✨ Enhanced extraction with table support available!")
except ImportError as e:
    print(f"   ⚠️  pdfplumber not available: {e}")
    print("   Falling back to PyPDF2 only")

print("\n" + "=" * 60)
print("Summary")
print("=" * 60)

try:
    from PyPDF2 import PdfReader
    pdf_support = True
except:
    pdf_support = False

try:
    import pdfplumber
    enhanced_support = True
except:
    enhanced_support = False

if pdf_support and enhanced_support:
    print("✅ PDF support: EXCELLENT (pdfplumber + PyPDF2)")
    print("   - Full text extraction")
    print("   - Table detection")
    print("   - Multi-column support")
    print("   - Layout preservation")
elif pdf_support:
    print("✅ PDF support: GOOD (PyPDF2 only)")
    print("   - Basic text extraction")
    print("   - Install pdfplumber for enhanced features:")
    print("     pip install pdfplumber")
else:
    print("❌ PDF support: NOT AVAILABLE")
    print("   Install required libraries:")
    print("     pip install PyPDF2 pdfplumber")

print("\n" + "=" * 60)

