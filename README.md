# 🧠 Trinexial Technologies - Mock Aptitude Test

A **proctored online aptitude test platform** featuring MSB-style multitasking blocking, live camera/microphone monitoring, and automated email scorecard delivery.

🌐 **Live Demo:** [https://amith-15-code.github.io/TrinexialTest/](https://amith-15-code.github.io/TrinexialTest/)

---

## 🚀 Features

* **Proctored Testing**: Fullscreen enforcement, tab-switch detection, and real-time camera/mic monitoring
* **Subject Coverage**: Digital Electronics, VLSI, DSP, DC Circuits, and Aptitude
* **Real-time Violation Tracking**: Monitors and limits multitasking violations
* **Automated Email System**: Sends professional scorecards to candidates instantly
* **Modern UI**: Responsive interface with real-time status indicators and intuitive design

---

## ⚙️ Setup Instructions

### 1️⃣ Gmail App Password Setup

Before running the server, set up your **Gmail App Password** for secure email delivery:

1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Navigate to **Security → 2-Step Verification** (enable if not already)
3. Go to **App passwords → Generate app password**
4. Select **“Mail” → “Other (Custom name)”** and enter *Trinexial Test*
5. Copy the generated **16-character password**

---

### 2️⃣ Environment Setup

```bash
# Set Gmail App Password (Windows PowerShell)
$env:GMAIL_APP_PASSWORD="your-16-character-app-password"

# Or set permanently (Windows)
setx GMAIL_APP_PASSWORD "your-16-character-app-password"
```

---

### 3️⃣ Run the Server

```bash
# Navigate to the project directory
cd "E:\Easy EDA\jarvis-ai-assistant-main\jarvis-ai-assistant-main\Frontend\TrinexialTest"

# Start the local server
python server.py

# Or specify a custom port
python server.py 8080
```

---

### 4️⃣ Access the Test

Open your browser and visit:
👉 **[http://localhost:8000](http://localhost:8000)**

Or access the hosted version:
🌐 **[https://amith-15-code.github.io/TrinexialTest/](https://amith-15-code.github.io/TrinexialTest/)**

---

## 🧩 Test Flow

1. **Login** — Enter your name, email, and optional roll number
2. **Permissions** — Grant camera/mic access and enter fullscreen
3. **Attempt Test** — 15 questions across 5 subjects (45 minutes total)
4. **Submit** — Auto submission on completion or after 5 violations
5. **Email Delivery** — Scorecard sent instantly to your registered email

---

## 🔒 Proctoring Features

* **Fullscreen Enforcement** — Restricts test to fullscreen mode
* **Tab Switch Detection** — Tracks and warns multitasking attempts
* **Camera Monitoring** — Live camera feed during the test
* **Microphone Monitoring** — Detects real-time audio activity
* **Clipboard Blocking** — Prevents copy/paste operations
* **Auto Submit** — Automatically ends test after 5 violations

---

## 📧 Email Scorecard

Automatically sends a **professional HTML scorecard** including:

* Candidate name and details
* Total score and percentage
* Subject-wise breakdown
* Timestamp and test details
* Professional branding from *Trinexial Technologies*

---

## 📁 File Structure

```
TrinexialTest/
├── index.html          # Main test interface
├── styles.css          # Styling and responsive design
├── app.js              # Frontend logic and proctoring features
├── server.py           # HTTP server and API endpoints
├── email_service.py    # Handles email delivery
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## 🧰 Troubleshooting

### ⚠️ Email Not Sending

* Check if Gmail App Password is correctly configured
* Ensure internet connection is active
* Confirm 2-Step Verification is enabled on Gmail

### 🎥 Camera/Mic Issues

* Use **Google Chrome** or **Microsoft Edge**
* Allow permissions when prompted
* Verify browser security settings

### 🖥️ Fullscreen Issues

* Use modern browsers (Chrome, Edge, Firefox)
* Enable fullscreen permissions
* Disable interfering extensions

---

## 🔐 Security Notes

* Uses **App Password** instead of regular Gmail password
* Camera/mic access is **temporary and secure**
* No personal data stored permanently
* Test data sent only via secure email

---

## 📞 Contact

For support or queries:
📧 **[amithvenkatesh223@gmail.com](mailto:amithvenkatesh223@gmail.com)**
🏢 **Trinexial Technologies**

🌐 **Official Website:** [https://amith-15-code.github.io/TrinexialTest/](https://amith-15-code.github.io/TrinexialTest/)
