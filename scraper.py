import requests
from bs4 import BeautifulSoup
import json
import os
import smtplib
from email.mime.text import MIMEText

# Configuration
URL = "https://web.cs.ucla.edu/classes/spring26/cs32/announcements.html"
STATE_FILE = "seen.json"

# Email credentials from environment variables (kept safe in GitHub Secrets)
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD") # Use a Gmail App Password
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")

def get_announcements():
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract all text, looking for the lines that contain the announcements
    # UCLA CS websites typically use simple tables or lists for this.
    announcements = []
    
    # We grab table rows and filter out the ones that start with a date pattern
    for tr in soup.find_all('tr'):
        cells = tr.find_all(['td', 'th'])
        if len(cells) >= 2:
            date_text = cells[0].get_text(strip=True)
            info_text = cells[1].get_text(strip=True)
            # Basic check to see if the first column looks like a date (e.g., "5/5/26")
            if "/" in date_text and len(date_text) <= 10: 
                announcements.append(f"{date_text}: {info_text}")
                
    return announcements

def send_email(new_announcements):
    subject = "🚨 New CS 32 Announcement!"
    body = "Here are the new announcements posted to the CS 32 website:\n\n"
    for ann in new_announcements:
        body += f"- {ann}\n\n"
    body += f"View them here: {URL}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

def main():
    print("Fetching announcements...")
    current_announcements = get_announcements()
    
    # Load previously seen announcements
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            seen_announcements = set(json.load(f))
    else:
        seen_announcements = set()

    # Find which ones are new
    new_announcements = [a for a in current_announcements if a not in seen_announcements]

    if new_announcements:
        print(f"Found {len(new_announcements)} new announcement(s)! Sending email...")
        send_email(new_announcements)
        
        # Update the state file
        with open(STATE_FILE, 'w') as f:
            json.dump(current_announcements, f)
    else:
        print("No new announcements.")

if __name__ == "__main__":
    main()
