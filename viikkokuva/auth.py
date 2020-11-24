import contextlib
import atexit
import logging
import os
import sys

import msal

from . import settings

if settings.TOKEN_CACHE:
    cache = msal.SerializableTokenCache()
    with contextlib.suppress(FileNotFoundError):
        with open(settings.TOKEN_CACHE) as f:
            cache.deserialize(f.read())

    def serialize_cache():
        if cache.has_state_changed:
            with open(settings.TOKEN_CACHE, "w") as f:
                f.write(cache.serialize())

    atexit.register(serialize_cache)
else:
    cache = None

SCOPES = ["User.Read", "Tasks.ReadWrite", "Tasks.ReadWrite.Shared"]

logger = logging.getLogger(__name__)

app = msal.PublicClientApplication(
    authority=settings.AUTH_ENDPOINT,
    client_id=settings.CLIENT_ID,
    token_cache=cache,
)


def get_msal_client():
    return app


def get_tokens():
    logger.debug("Getting tokens")
    accounts = app.get_accounts()
    result = None
    if accounts:
        account = accounts[0]
        logger.debug("Found account %s, trying cached token", account)
        result = app.acquire_token_silent(SCOPES, account=account)
    if not result:
        logger.debug("Could not find cached token, trying refresh token")
        refresh_token = settings.REFRESH_TOKEN
        result = app.acquire_token_by_refresh_token(
            refresh_token=refresh_token,
            scopes=SCOPES,
        )
        if error := result.get("error"):
            logger.warning("Error when trying to acquire tokens: %r", error)
    return result
