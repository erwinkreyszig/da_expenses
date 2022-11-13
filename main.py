import datetime
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def root():
    return render_template("index.html")


@app.route("/2022/")
def for_2022():
    import os.path

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    # write it here temporarily
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    SPREADSHEET_ID = "1ZoAuDHqhGEK5BUuBSFdWdUrc51NOUr7YnJ7gStetS-0"
    RANGE_NAME = "January!A1:E500"

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        values = result.get("values", [])
        x = str(values)
    except HttpError as err:
        x = "Error error"



    return render_template("2022.html", mvar=x)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)