from datetime import datetime
import enum
import logging

from dateutil.utils import today
from dateutil.relativedelta import relativedelta
import requests

from . import auth, settings

logger = logging.getLogger(__name__)


class PictureType:
    title: str

    @staticmethod
    def delta(big_date: datetime, now: datetime):
        raise NotImplemented


class WeekPicture(PictureType):
    title = "Viikkokuva"

    @staticmethod
    def delta(big_date: datetime, now: datetime):
        return (now - big_date).days // 7


class MonthPicture(PictureType):
    title = "Kuukausikuva"

    @staticmethod
    def delta(now: datetime, big_date: datetime):
        rdelta = relativedelta(big_date, now)
        return 12 * rdelta.years + rdelta.months


class PictureChoice(PictureType, enum.Enum):
    week = WeekPicture
    month = MonthPicture

    def title(self):
        big_date = settings.BIG_DATE
        now = today()
        return f"📷 {self.value.title} {self.value.delta(big_date, now)}"


def get_task_payload(choice):
    reminder_date = today() + relativedelta(days=3, hour=12)
    return {
        "title": choice.title(),
        "isReminderOn": True,
        "reminderDateTime": {
            "dateTime": reminder_date.isoformat(),
            "timeZone": settings.TIMEZONE,
        },
    }


def create_task(choice: PictureChoice, dry_run=False):
    endpoint = f"{settings.GRAPH_ENDPOINT}/me/todo/lists/{settings.TASK_LIST_ID}/tasks"
    payload = get_task_payload(choice)
    if dry_run:
        logger.info(
            "Dry-run. Would have created task.\nEndpoint: %s\nPayload: %r",
            endpoint,
            payload,
        )
        return

    tokens = auth.get_tokens()
    if access_token := tokens.get("access_token"):
        logger.info("Creating new task")
        try:
            response = requests.post(
                endpoint,
                headers={"Authorization": f"Bearer {access_token}"},
                json=payload,
                timeout=3,
            )
            response.raise_for_status()
        except requests.Timeout:
            logger.warning("Timed out when creating task", exc_info=True)
        except requests.HTTPError:
            logger.warning("HTTP Error when creating task", exc_info=True)
        else:
            logger.info("Task successfully created")
    else:
        logger.warning("Not creating task, missing access token")
