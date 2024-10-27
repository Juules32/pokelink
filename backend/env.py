import os
from dotenv import load_dotenv

load_dotenv()

CRON_SECRET = os.getenv('CRON_SECRET')                  # Exists only in production to allow cron jobs
ENVIRONMENT = os.getenv('ENVIRONMENT')                  # Development or production?
BLOB_HOST = os.getenv('BLOB_HOST')                      # The host name of the blob storage used only in production
CONNECTION_STRING = os.getenv('CONNECTION_STRING')      # The database connection string