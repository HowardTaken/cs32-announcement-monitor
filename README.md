# 🚀 Automated Course Announcement Notifier

An automated web scraping and notification system built to monitor university course websites and deliver real-time email alerts for new announcements.

## 📌 Overview
During my coursework in CS 32 (Introduction to Computer Science II), I noticed that the course website hosted critical updates (homework specs, midterm schedules, extra credit forms) but lacked an automated push-notification system. 

To solve this, I engineered a serverless Python script that autonomously monitors the site, detects changes, and alerts me via email, ensuring I never miss a deadline.

## ⚙️ How It Works (Architecture)
Instead of running a local server 24/7, this project leverages **GitHub Actions** for free, cloud-based automation.
1. **Scheduled Cron Job:** A GitHub Actions workflow triggers the script at the top of every hour.
2. **Web Scraping:** Python (`requests` & `BeautifulSoup`) fetches the live HTML table from the course webpage.
3. **State Management:** The script compares the live data against a persistent `seen.json` file stored in the repository to identify strictly *new* announcements.
4. **Email Dispatch:** If a new row is detected, `smtplib` formats the data and securely dispatches an email via an encrypted SMTP server.
5. **Auto-Commit:** The Action automatically commits the updated `seen.json` back to the repository, updating the state for the next hourly run.

## 🛠️ Tech Stack
* **Language:** Python 3
* **Libraries:** `BeautifulSoup4` (HTML parsing), `requests` (HTTP client), `smtplib` (Email protocol), `json`, `os`
* **CI/CD & Hosting:** GitHub Actions (Automated Workflows)
* **Security:** GitHub Repository Secrets (Environment variable injection for secure credential management)

## 💡 Key Skills Demonstrated
* **Web Scraping:** Navigating DOM structures, extracting specific table data (`<tr>`, `<td>`), and bypassing basic bot-blocking with User-Agent headers.
* **CI/CD Pipelines:** Writing YAML workflows to automate code execution and Git operations.
* **State Management:** Reading, writing, and handling edge cases (like empty states) in JSON.
* **Security Best Practices:** Keeping sensitive credentials out of source code and Git history.
