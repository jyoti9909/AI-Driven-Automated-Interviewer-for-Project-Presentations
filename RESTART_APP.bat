@echo off
echo ========================================
echo Restarting AI Interviewer with Fresh Cache
echo ========================================
echo.

echo [1/2] Clearing Streamlit cache...
streamlit cache clear

echo.
echo [2/2] Starting application...
echo.
python -m streamlit run app.py

pause

