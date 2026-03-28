# Naukri Resume Upload Automation

This is an automated script that logs into Naukri.com and uploads your resume every hour using GitHub Actions.

## 🚀 Features

- ✓ Automated Naukri login
- ✓ Automatic resume upload
- ✓ Runs every 1 hour (even when laptop is off)
- ✓ Runs on GitHub's servers (no local machine needed)
- ✓ Free & secure (uses encrypted secrets)

## 📋 Prerequisites

- GitHub account
- Naukri account with username/email and password
- Updated Resume.pdf file

## 🔧 Setup Instructions

### Step 1: Already Done! ✓
Your code is already pushed to: https://github.com/sushantbhatt/naukri-automation

### Step 2: Add Your Secrets to GitHub

1. Go to your GitHub repository: https://github.com/sushantbhatt/naukri-automation
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add two secrets:

   | Secret Name | Value |
   |-------------|-------|
   | `NAUKRI_EMAIL` | Your Naukri email (e.g., bhattsushant4@gmail.com) |
   | `NAUKRI_PASSWORD` | Your Naukri password |

5. Click **Add secret** for each one

### Step 3: Enable GitHub Actions

1. Go to **Actions** tab in your repo
2. Click **I understand my workflows, go ahead and enable them**
3. Done! ✓

### Step 4: Verify It's Running

1. Go to **Actions** tab
2. Click on the **Run Naukri Automation Every Hour** workflow
3. You should see scheduled runs displayed as green checkmarks ✓

## ⏰ Schedule

The script runs automatically:
- **Every 1 hour** (at minute 0 of every hour)
- You can also manually trigger it from the Actions tab
- Logs are saved for 7 days if there's an error

## 🔒 Security

- Your credentials are encrypted by GitHub
- Only stored as secrets, never displayed in logs
- Code is open source for transparency

## 🛠️ Manual Testing (Local)

To run locally:

```bash
# Install dependencies
pip install -r requirements.txt
playwright install

# Set environment variables
set NAUKRI_EMAIL=your-email@gmail.com
set NAUKRI_PASSWORD=your-password

# Run
python naukri_login.py
```

## 📁 Project Structure

```
naukri-automation/
├── .github/
│   └── workflows/
│       └── schedule.yml          # GitHub Actions configuration
├── naukri_login.py               # Main automation script
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── Resume.pdf                    # Your resume (not tracked in git)
```

## 🐛 Troubleshooting

### GitHub Actions shows errors?
- Check that your email/password are correct in Secrets
- Check the Action logs for specific error messages
- Naukri website might have changed - may need to update selectors

### Script times out?
- Naukri website loading slowly
- Try increasing the timeout in `naukri_login.py` line 37

### Resume not uploading?
- Make sure Resume.pdf exists in the root folder
- Verify it's a valid PDF file
- Check logs for specific error

## 📝 Notes

- Resume must be named `Resume.pdf` and placed in the root folder
- The script waits 60 seconds for any 2FA verification
- Browser window is headless (no visual display on GitHub)

## 🚀 Next Steps (Optional)

Want to improve this automation?
- Add email notifications on success/failure
- Add resume update detection
- Add job application automation
- Add resume versioning

---

**Created with ❤️ for automated job hunting**
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
