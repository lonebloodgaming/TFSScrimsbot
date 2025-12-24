import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope)

client = gspread.authorize(creds)

sheet = client.open("PUBG Scrims").sheet1

def add_team(team, slot):
    sheet.append_row([slot, team])
