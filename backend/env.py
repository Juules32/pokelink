import os
from dotenv import load_dotenv

load_dotenv()

CRON_SECRET = os.getenv('CRON_SECRET')
ENVIRONMENT = os.getenv('ENVIRONMENT')
BLOB_HOST = os.getenv('BLOB_HOST')
CONNECTION_STRING = os.getenv('CONNECTION_STRING')
