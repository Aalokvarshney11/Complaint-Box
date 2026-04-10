# Complaint Box - Smart Complaint Management System
![complaint box](images/image.png)
A smart, voice-enabled complaint management system built with Python and Streamlit. Clients can register complaints with voice assistance, and managers can track, manage, and resolve complaints through a dedicated dashboard.

---

## Features

- Voice-enabled interface using ElevenLabs TTS
- Client registration and login system
- Step-by-step complaint submission flow
- Manager dashboard with complaint tracking
- Mark complaints as Solved / Unsolved
- Auto email notification with CSV attachment on every new complaint
- WhatsApp alert to manager via Twilio
- Download solved complaints as CSV
- Secure password hashing using SHA-256
- Session-based access control

---

## Tech Stack

- Python 3.x
- Streamlit
- SQLite3
- ElevenLabs API
- Twilio WhatsApp API
- SMTP Gmail
- python-dotenv

---

## Project Structure
```
complaint_box/
├── app.py                  # Main login/register page
├── database.py             # Database connection and functions
├── setup.py                # One-time setup - creates DB and manager account
├── speaks_fx.py            # ElevenLabs voice function
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not pushed to GitHub)
├── .gitignore              # Files to ignore in Git
├── complaintbox.db         # SQLite database (auto created, not pushed)
└── pages/
    ├── manager_dashboard.py   # Manager interface
    └── client_page.py         # Client complaint interface
```

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/complaint-box.git
cd complaint-box
```

### 2. Create virtual environment
```bash
python -m venv basev
```

Activate on Windows:
```bash
basev\Scripts\activate
```

Activate on Mac/Linux:
```bash
source basev/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup environment variables

Create a `.env` file in the root folder and fill in the following:
```
ELEVENLABS_API_KEY=your_elevenlabs_api_key
EMAIL_USER=your_gmail@gmail.com
EMAIL_PASS=your_16_digit_app_password
OWNER_EMAIL=manager_email@gmail.com
MANAGER_EMAIL=manager_email@gmail.com
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
MANAGER_WHATSAPP=whatsapp:+91xxxxxxxxxx
```

> For Gmail App Password: Go to Google Account Settings, enable 2-Step Verification, then generate an App Password.

> For Twilio WhatsApp: You need to join the sandbox first. Send a WhatsApp message from your phone to the Twilio sandbox number: `join <your-sandbox-keyword>`

### 5. Run setup file (only once)
```bash
python setup.py
```

This will create the database tables and manager account.

### 6. Run the application
```bash
streamlit run app.py
```

---

## Usage

### Client
1. Open the app
2. Go to Register tab and create a new account
3. Login with your credentials
4. Follow the voice guided complaint submission flow
5. Submit your complaint with house number and phone number

### Manager
1. Login with manager credentials
2. View all complaints on the dashboard
3. Check pending complaints in the Unsolved tab
4. Click Mark Solved when a complaint is resolved
5. Download solved complaints as CSV from the Solved tab

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| ELEVENLABS_API_KEY | ElevenLabs API key for voice generation |
| EMAIL_USER | Gmail address used for sending emails |
| EMAIL_PASS | Gmail App Password (16 digits) |
| OWNER_EMAIL | Manager email to receive complaint notifications |
| MANAGER_EMAIL | Manager email for dashboard alerts |
| TWILIO_ACCOUNT_SID | Twilio Account SID |
| TWILIO_AUTH_TOKEN | Twilio Auth Token |
| TWILIO_WHATSAPP_FROM | Twilio WhatsApp sandbox number |
| MANAGER_WHATSAPP | Manager WhatsApp number with country code |

---

## Important Notes

- Never push the `.env` file to GitHub as it contains sensitive credentials
- The `complaintbox.db` file is excluded from Git via `.gitignore`
- The `basev/` virtual environment folder should not be pushed to GitHub
- Run `setup.py` only once during initial setup

---

## Author

Aalok Varshney...