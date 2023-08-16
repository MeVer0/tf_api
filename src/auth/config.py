from dotenv import load_dotenv
import os

load_dotenv()

secret = os.environ.get("SECRET")

# SMTP
username = os.environ.get("SMTP_USERNAME")
password = os.environ.get("SMTP_PASSWORD")
