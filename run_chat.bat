@echo off
echo Starting AhadChat...
echo.
echo Installing dependencies if needed...
pip install -r requirements.txt
echo.
echo Starting the chat application...
echo.
echo The app will open in your browser automatically.
echo If not, go to: http://localhost:8501
echo.
echo Press Ctrl+C to stop the application.
echo.
streamlit run app.py
pause 