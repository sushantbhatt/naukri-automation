"""
Naukri.com Login & Resume Upload Automation Script using Playwright
No external driver download needed - browsers are bundled
"""

import os
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

# Try to load from .env file if it exists (for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

async def login_naukri(page, email, password):
    """
    Automate Naukri login
    """
    print("Navigating to Naukri login page...")
    await page.goto("https://www.naukri.com/nlogin/login", wait_until="domcontentloaded")
    
    # Wait and fill email field
    print("Entering email/username...")
    await page.wait_for_selector("#usernameField", timeout=10000)
    await page.fill("#usernameField", email)
    print(f"✓ Email entered: {email}")
    
    # Fill password field
    print("Entering password...")
    await page.fill("#passwordField", password)
    print("✓ Password entered")
    
    # Click login button
    print("Clicking login button...")
    await page.click("button:has-text('Login')")
    print("✓ Login button clicked")
    
    # Wait for navigation
    print("Waiting for login to complete (30 seconds)...")
    try:
        await page.wait_for_load_state("domcontentloaded", timeout=30000)
    except:
        print("⚠️  Page load timeout, checking current state...")
    
    # Wait a bit for any redirects
    await page.wait_for_timeout(3000)
    
    # Check if login was successful
    current_url = page.url
    print(f"Current URL after login attempt: {current_url}")
    
    if "nlogin" not in current_url and "naukri.com" in current_url:
        print("✓ Login successful!")
        print(f"Logged in URL: {current_url}")
        return True
    else:
        print("✗ Login may have failed or verification required")
        print(f"Still on URL: {current_url}")
        print("\n⚠️  If a verification/OTP dialog appears, please complete it manually")
        print("Script will wait 60 seconds for manual verification...")
        
        # Wait for user to manually verify if needed
        for i in range(12):
            await page.wait_for_timeout(5000)
            current_url = page.url
            if "nlogin" not in current_url and "naukri.com" in current_url:
                print(f"✓ Login verified! URL: {current_url}")
                return True
        
        return False

async def upload_resume(page, resume_path):
    """
    Navigate to profile page, find and click 'Update Resume' button, then upload resume
    """
    print("\n" + "="*50)
    print("Uploading Resume...")
    print("="*50)
    
    # Check if file exists
    if not os.path.exists(resume_path):
        print(f"✗ Error: Resume file not found at {resume_path}")
        return False
    
    # Navigate to profile page
    print("Navigating to profile page...")
    profile_url = "https://www.naukri.com/mnjuser/profile?id=&altresid"
    await page.goto(profile_url, wait_until="domcontentloaded")
    
    print(f"Current URL: {page.url}")
    
    # Wait for page to fully load
    await page.wait_for_timeout(3000)
    
    # Scroll to find the Resume section
    print("Looking for Resume section...")
    
    try:
        # Find the text "Update resume" in the DOM
        update_resume_link = page.locator("text='Update resume'").first
        
        # Check if found
        count = await page.locator("text='Update resume'").count()
        print(f"Found {count} occurrence(s) of 'Update resume'")
        
        if count == 0:
            # Try case-insensitive
            update_resume_link = page.locator("text=/update resume/i").first
            count = await page.locator("text=/update resume/i").count()
            print(f"Found {count} occurrence(s) with case-insensitive search")
        
        if count == 0:
            print("✗ Could not find 'Update resume' text on page")
            return False
        
        # Scroll into view
        await update_resume_link.scroll_into_view_if_needed()
        await page.wait_for_timeout(500)
        
        print(f"✓ Found 'Update resume' link/button")
        print("Clicking 'Update resume'...")
        
        # Click the element
        await update_resume_link.click()
        
        print("✓ Clicked 'Update resume' button")
        
        # Wait for file input to appear
        await page.wait_for_timeout(1000)
        
    except Exception as e:
        print(f"✗ Error finding/clicking Update resume: {str(e)}")
        return False
    
    # Now upload the file
    try:
        print(f"\nUploading resume file: {resume_path}")
        
        # Wait for file input to be available
        try:
            await page.wait_for_selector('input[type="file"]', timeout=5000)
            print("✓ File input dialog appeared")
        except:
            print("⚠️  No file input found, but proceeding with upload...")
        
        # Get all file inputs
        all_inputs = page.locator('input[type="file"]')
        input_count = await all_inputs.count()
        print(f"Found {input_count} file input(s)")
        
        if input_count == 0:
            print("✗ No file input found on page")
            return False
        
        # Use the first file input
        file_input = all_inputs.first
        print(f"Using file input for upload...")
        
        # Set the file
        await file_input.set_input_files(resume_path)
        
        print("✓ Resume file uploaded successfully!")
        
        # Wait for upload to process
        await page.wait_for_timeout(3000)
        
        # Look for success message
        try:
            success_indicators = page.locator("text=/[Ss]uccess|uploaded|[Uu]pdated/i")
            count = await success_indicators.count()
            if count > 0:
                msg = await success_indicators.first.inner_text()
                print(f"✓ Upload confirmation: {msg[:50]}")
        except:
            pass
        
        print("✓ Resume upload completed")
        return True
            
    except Exception as e:
        print(f"✗ Error during upload: {str(e)}")
        return False

async def main_automation(email, password, resume_path):
    """
    Main automation function - Login and Upload Resume
    """
    
    async with async_playwright() as p:
        # Launch Chromium
        try:
            browser = await p.edge.launch(headless=True)
            print("Launching Microsoft Edge...")
        except:
            print("Launching Chromium...")
            browser = await p.chromium.launch(headless=True)
        
        try:
            context = await browser.new_context()
            page = await context.new_page()
            
            # Step 1: Login
            print("\n" + "="*50)
            print("STEP 1: LOGIN")
            print("="*50)
            login_success = await login_naukri(page, email, password)
            
            if not login_success:
                print("✗ Login failed. Exiting.")
                await context.close()
                await browser.close()
                return False
            
            # Wait before proceeding to next step
            await page.wait_for_timeout(2000)
            
            # Step 2: Upload Resume
            upload_success = await upload_resume(page, resume_path)
            
            # Keep browser open for viewing
            print("\n" + "="*50)
            print("Process Complete!")
            print("="*50)
            print("Browser will close in 10 seconds...")
            await page.wait_for_timeout(10000)
            
            await context.close()
            await browser.close()
            
            return upload_success
            
        except Exception as e:
            await browser.close()
            print(f"Error: {str(e)}")
            return False

def main():
    """
    Main function
    """
    email = os.getenv('NAUKRI_EMAIL')
    password = os.getenv('NAUKRI_PASSWORD')
    
    if not email or not password:
        print("❌ Error: NAUKRI_EMAIL and NAUKRI_PASSWORD environment variables must be set!")
        print("\nFor GitHub Actions: Add them in Settings → Secrets and variables → Actions")
        print("For Local: Create .env file or set environment variables")
        return
    
    # Get resume path - try Resume.pdf first, then test.pdf
    resume_path = os.path.join(os.path.dirname(__file__), 'Resume.pdf')
    if not os.path.exists(resume_path):
        # Try alternative filename
        resume_path = os.path.join(os.path.dirname(__file__), 'Resume.pdf')
    
    print("\n" + "="*60)
    print("NAUKRI AUTOMATION - LOGIN & RESUME UPLOAD")
    print("="*60)
    print(f"Email: {email}")
    print(f"Resume Path: {resume_path}")
    print(f"Resume Exists: {os.path.exists(resume_path)}")
    print("="*60 + "\n")
    
    asyncio.run(main_automation(email, password, resume_path))

if __name__ == "__main__":
    main()
