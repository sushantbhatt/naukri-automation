# Naukri Login Automation Script

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables (Recommended - Don't hardcode credentials!)

**Windows (PowerShell):**
```powershell
$env:NAUKRI_EMAIL = "bhattsushant4@gmail.com"
$env:NAUKRI_PASSWORD = "sushantbhattbhatt4"
```

**Windows (CMD):**
```cmd
set NAUKRI_EMAIL=bhattsushant4@gmail.com
set NAUKRI_PASSWORD=sushantbhattbhatt4
```

**Linux/Mac:**
```bash
export NAUKRI_EMAIL="bhattsushant4@gmail.com"
export NAUKRI_PASSWORD="sushantbhattbhatt4"
```

### 3. Run the Script
```bash
python naukri_login.py
```

## Alternative: Using .env File (More Secure)

1. Install python-dotenv:
```bash
pip install python-dotenv
```

2. Create `.env` file in the same directory:
```
NAUKRI_EMAIL=bhattsushant4@gmail.com
NAUKRI_PASSWORD=sushantbhattbhatt4
```

3. Update the script to use python-dotenv at the top of `main()`:
```python
from dotenv import load_dotenv
load_dotenv()
```

## ⚠️ Security Best Practices

- ✅ Never commit `.env` or credentials to version control
- ✅ Use environment variables or config files
- ✅ Add `.env` to `.gitignore`
- ✅ Consider using a password manager
- ❌ Never hardcode credentials in scripts

## Troubleshooting

- **"Element not found"**: Naukri website HTML may have changed. Check the element IDs
- **Login fails silently**: The website may require additional verification (OTP, CAPTCHA)
- **Headless mode issues**: Disable headless mode to see what's happening

## Note on Terms of Service

Check Naukri's ToS before automating. Some websites restrict automated access.
