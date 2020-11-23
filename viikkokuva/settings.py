from datetime import datetime
import os

from dotenv import load_dotenv

load_dotenv()

AUTH_ENDPOINT = "https://login.microsoftonline.com/consumers"
GRAPH_ENDPOINT = "https://graph.microsoft.com/v1.0"

CLIENT_ID = os.getenv("CLIENT_ID")
TASK_LIST_ID = os.getenv("TASK_LIST_ID")
TIMEZONE = os.getenv("TIMEZONE", "UTC")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

BIG_DATE = datetime.fromisoformat(os.getenv("BIG_DATE"))
