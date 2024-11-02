import datetime
import os
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build

NUTRITIONIX_APP_ID = os.getenv("APP_ID")
NUTRITIONIX_API_KEY = os.getenv("API_KEY")

GENDER = "female"
WEIGHT_KG = 40
HEIGHT_CM = 140
AGE = 31

nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
nutritionix_headers = {
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_API_KEY,
    "Content-Type": "application/json"
}

exercise_text = input("Tell me which exercise you did: ")

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}
response = requests.post(url=nutritionix_endpoint, json=parameters, headers=nutritionix_headers)
data = response.json()["exercises"][0]
exercise = data["name"].title()
duration = data["duration_min"]
calories = data["nf_calories"]
date = datetime.date.today().strftime("%d/%m/%Y")
time = datetime.datetime.now().strftime("%H:%M:%S")
new_entry = [[date, time, exercise, duration, calories]]


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = 'passkey.json'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1TJ4k-Mgr5TmoPamnb7Ur1cG7r9X1qejJj9lTi7H6f9o"

service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="workouts!A1:E").execute()
values = result.get("values", [])

request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="workouts!A1:E",
                                valueInputOption="USER_ENTERED", body={"values": new_entry}).execute()
