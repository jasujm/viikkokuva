import msal
import flask

from . import settings, auth

app = flask.Flask(__name__)

msal_client = msal.PublicClientApplication(
    authority=settings.AUTH_ENDPOINT,
    client_id=settings.CLIENT_ID,
)


@app.route("/")
def home():
    url = msal_client.get_authorization_request_url(
        scopes=auth.SCOPES,
        redirect_uri=flask.url_for("token", _external=True),
        domain_hint="consumers",
    )
    return flask.redirect(url)


@app.route("/token")
def token():
    code = flask.request.args.get("code")
    result = msal_client.acquire_token_by_authorization_code(
        code=code,
        scopes=auth.SCOPES,
        redirect_uri=flask.url_for("token", _external=True),
    )
    return flask.jsonify(result)
