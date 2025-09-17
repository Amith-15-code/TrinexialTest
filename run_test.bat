@echo off
echo Trinexial Technologies - Mock Aptitude Test Server
echo ================================================
echo.
echo Make sure you have set the GMAIL_APP_PASSWORD environment variable
echo before running this server.
echo.
echo To set it, run:
echo setx GMAIL_APP_PASSWORD "your-16-character-app-password"
echo.
echo Starting server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
python server.py
pause
