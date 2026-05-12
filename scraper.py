import requests
from bs4 import BeautifulSoup
import json
import os
import smtplib
from email.mime.text import MIMEText

URL = "https://web.cs.ucla.edu/classes/spring26/cs32/announcements.html"
STATE_FILE = "seen.json"

# Email credentials from GitHub Secrets
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")

def get_announcements():
    # Disguise the scraper as a normal web browser
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(URL, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    announcements = []
    for tr in soup.find_all('tr'):
        cells = tr.find_all(['td', 'th'])
        if len(cells) >= 2:
            date_text = cells[0].get_text(strip=True)
            info_text = cells[1].get_text(strip=True)
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
    
    # Load previously seen announcements (with a safety check for empty files)
    seen_announcements = set()
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                # Read the file and ensure it's not totally blank before parsing
                content = f.read().strip()
                if content:
                    seen_announcements = set(json.loads(content))
        except json.JSONDecodeError:
            print("Notice: seen.json was empty. Starting fresh.")
            pass 

    new_announcements = [a for a in current_announcements if a not in seen_announcements]

    if new_announcements:
        print(f"Found {len(new_announcements)} new announcement(s)! Sending email...")
        send_email(new_announcements)
        
        with open(STATE_FILE, 'w') as f:
            json.dump(current_announcements, f)
    else:
        print("No new announcements.")

if __name__ == "__main__":
    main()
