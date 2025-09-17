# Trinexial Technologies - Mock Aptitude Test

A proctored online aptitude test platform with MSB-style blocking multitasking, camera/microphone monitoring, and automated scorecard email delivery.

## Features

- **Proctored Testing**: Fullscreen enforcement, tab-switch detection, camera/mic monitoring
- **Subject Coverage**: Digital Electronics, VLSI, DSP, DC Circuits, and Aptitude questions
- **Real-time Violations**: Tracks and limits multitasking violations
- **Automated Email**: Sends detailed scorecard to candidate's email
- **Professional UI**: Modern, responsive design with real-time status indicators

## Setup Instructions

### 1. Gmail App Password Setup
Before running the server, you need to set up Gmail App Password:

1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Navigate to Security → 2-Step Verification (enable if not already)
3. Go to App passwords → Generate app password
4. Select "Mail" and "Other (Custom name)" → Enter "Trinexial Test"
5. Copy the generated 16-character password

### 2. Environment Setup
```bash
# Set Gmail App Password (Windows PowerShell)
$env:GMAIL_APP_PASSWORD="your-16-character-app-password"

# Or set permanently (Windows)
setx GMAIL_APP_PASSWORD "your-16-character-app-password"
```

### 3. Run the Server
```bash
# Navigate to the test directory
cd "E:\Easy EDA\jarvis-ai-assistant-main\jarvis-ai-assistant-main\Frontend\TrinexialTest"

# Start the server
python server.py

# Or specify custom port
python server.py 8080
```

### 4. Access the Test
Open your browser and go to: `http://localhost:8000`

## Test Flow

1. **Login**: Enter name, email, and optional roll number
2. **Permissions**: Grant camera/microphone access and enter fullscreen
3. **Test**: Answer 15 questions across 5 subjects (45 minutes)
4. **Submission**: Automatic email delivery with detailed scorecard

## Proctoring Features

- **Fullscreen Enforcement**: Test runs in fullscreen mode
- **Tab Switch Detection**: Alerts and counts violations
- **Camera Monitoring**: Live camera feed for proctoring
- **Microphone Level**: Audio activity monitoring
- **Clipboard Blocking**: Prevents copy/paste operations
- **Auto-Submit**: Submits test after 5 violations

## Email Scorecard

The system automatically sends a professional HTML email containing:
- Overall score and percentage
- Subject-wise performance breakdown
- Test details and timestamp
- Next steps information
- Professional branding from Trinexial Technologies

## File Structure

```
TrinexialTest/
├── index.html          # Main test interface
├── styles.css          # Styling and responsive design
├── app.js             # Frontend logic and proctoring
├── server.py          # HTTP server and API endpoints
├── email_service.py   # Email sending functionality
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Troubleshooting

### Email Not Sending
- Verify Gmail App Password is set correctly
- Check internet connection
- Ensure 2-Factor Authentication is enabled on Gmail account

### Camera/Microphone Issues
- Use Chrome or Edge browser
- Allow permissions when prompted
- Check browser security settings

### Fullscreen Issues
- Use modern browsers (Chrome, Edge, Firefox)
- Allow fullscreen permissions
- Disable browser extensions that might interfere

## Security Notes

- Gmail App Password is used instead of regular password
- Camera/mic access is only during test duration
- No data is stored permanently on the server
- All test data is sent via secure email

## Contact

For technical support or questions:
- Email: amithvenkatesh223@gmail.com
- Organization: Trinexial Technologies
