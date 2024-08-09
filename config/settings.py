import os
from dotenv import load_dotenv

ENV_PATH = "config/env.env"
LOGGING_CONF_FILE = "config/logging.conf.json"

load_dotenv(dotenv_path=ENV_PATH)

TOKEN = os.getenv('token')
REDIS_URL = os.getenv('redis_url')
DB_PATH = "database.db"
OWM_API = os.getenv('openweathermap_api')
