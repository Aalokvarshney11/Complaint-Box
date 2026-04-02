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

Activate karo:

- Windows:
```bash
basev\Scripts\activate
```

- Mac/Linux:
```bash
source basev/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup environment variables

`.env` file banao root folder mein aur yeh fill karo:
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

> Note: Gmail App Password ke liye Google Account Settings mein jakar 2-Step Verification ON karo aur App Password generate karo.

> Note: Twilio WhatsApp ke liye sandbox join karna hoga. Apne phone se Twilio sandbox number pe WhatsApp karo: `join <your-sandbox-keyword>`

### 5. Run setup file (sirf ek baar)
```bash
python setup.py
```

Yeh manager account aur database tables create karega.

### 6. Run the app
```bash
streamlit run app.py
```

---

## Usage

### Client
1. App kholo
2. Register tab mein naya account banao
3. Login karo
4. Voice guided flow follow karo
5. Complaint submit karo with house number and phone number

### Manager
1. Login karo manager credentials se
2. Dashboard mein saari complaints dekho
3. Unsolved tab mein pending complaints dekho
4. Mark Solved button dabao complaint resolve hone par
5. Solved tab mein CSV download karo

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| ELEVENLABS_API_KEY | ElevenLabs API key for voice |
| EMAIL_USER | Gmail address for sending emails |
| EMAIL_PASS | Gmail App Password (16 digits) |
| OWNER_EMAIL | Manager email to receive complaints |
| MANAGER_EMAIL | Manager email for dashboard alerts |
| TWILIO_ACCOUNT_SID | Twilio Account SID |
| TWILIO_AUTH_TOKEN | Twilio Auth Token |
| TWILIO_WHATSAPP_FROM | Twilio WhatsApp sandbox number |
| MANAGER_WHATSAPP | Manager WhatsApp number with country code |

---

## Important Notes

- `.env` file kabhi bhi GitHub pe push mat karo — sensitive credentials hain
- `complaintbox.db` file bhi push mat karo — `.gitignore` mein already add hai
- `basev/` virtual environment folder bhi push mat karo
- `setup.py` sirf ek baar run karna hai — baar baar mat chalao

---

## Author

Aalok Varshney