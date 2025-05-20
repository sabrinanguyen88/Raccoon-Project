import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]

# Load credentials from the service account JSON key
creds = Credentials.from_service_account_file("creds.json", scopes=SCOPES)

# Authorize and open the sheet
client = gspread.authorize(creds)
sheet = client.open("DS Collab Project Data").sheet1

# Get and print all data
data = sheet.get_all_values()
for row in data:
    print(row)