import requests
from bs4 import BeautifulSoup
import hashlib
import time
import smtplib
from email.mime.text import MIMEText
import logging

# URLs to monitor
URLS = [
    "https://jeemain.nta.nic.in/results-for-jeemain-2025-session-1/",
    "https://jeemain.nta.nic.in/results-for-jeemain-2025-session-1/link"
]

# File to store the previous hash of the website content
HASH_FILE = "website_hashes.txt"

# Email configuration
EMAIL_SENDER = "vanshcgindia@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "errq yrwv mkfa dpwt"  # Replace with your app-specific password
EMAIL_RECEIVER = "vanshcgindia@gmail.com"  # Replace with your email

# Log file configuration
LOG_FILE = "website_change_detector.log"

# Set up logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def fetch_website_content(url):
    """Fetch the content of the website."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return None

def get_content_hash(content):
    """Generate a hash of the website content."""
    return hashlib.md5(content.encode("utf-8")).hexdigest()

def load_previous_hashes():
    """Load previous hashes from the file."""
    try:
        with open(HASH_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

def save_hashes(hashes):
    """Save current hashes to the file."""
    with open(HASH_FILE, "w") as file:
        file.write("\n".join(hashes))

def send_email(subject, body):
    """Send an email notification."""
    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = EMAIL_SENDER
    message["To"] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, message.as_string())
        logging.info("Email notification sent!")
    except Exception as e:
        logging.error(f"Error sending email: {e}")

def detect_changes():
    """Check for changes in the websites."""
    previous_hashes = load_previous_hashes()
    current_hashes = []

    for i, url in enumerate(URLS):
        content = fetch_website_content(url)
        if content is None:
            current_hashes.append("")  # Use an empty string for failed fetches
            continue

        current_hash = get_content_hash(content)
        current_hashes.append(current_hash)

        if i < len(previous_hashes):
            if current_hash != previous_hashes[i]:
                logging.info(f"Change detected on {url}!")
                send_email("Website Change Detected", f"Change detected on {url}!")
            else:
                logging.info(f"No changes on {url}.")
        else:
            logging.info(f"Initialized monitoring for {url}.")

    save_hashes(current_hashes)

if __name__ == "__main__":
    logging.info("Starting website change detector...")
    try:
        while True:
            logging.info("Checking for changes...")
            detect_changes()
            time.sleep(30)  # Wait for 30 seconds before checking again
    except KeyboardInterrupt:
        logging.info("Script stopped by user.")
