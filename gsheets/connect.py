from googleapiclient.discovery import build
from google.oauth2 import service_account
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = os.path.join(THIS_FOLDER, "keys.json")
# import pandas as pd

# sheet_id = "1eKEQMoiQkzedgCFkJloNDDAGUimBmA1UktBixGytLSo"
# sheet_name = "Dados"
# url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
# df = pd.read_csv(url)


class ConnectGS:
    def __init__(self):
        self.creds = None
        self.creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = build("sheets", "v4", credentials=self.creds)

        # Call the Sheets API
        self.sheet = service.spreadsheets()

    def get_worksheet_range(self, worksheet, range):
        return f"{worksheet}!{range}"

    def read_sheet(self, sheet_id, worksheet, range):
        """The ID, worksheet and range of a sample spreadsheet"""
        # SAMPLE_SPREADSHEET_ID = "1m8jS9QNxtm1FqWP4PLc0VO2z1NQsGe-cWkwcFdd0m5Y"
        worksheet_range = self.get_worksheet_range(worksheet, range)
        result = (
            self.sheet.values()
            .get(spreadsheetId=sheet_id, range=worksheet_range)
            .execute()
        )
        return result

    def write_sheet(self, sheet_id, worksheet, range, values):
        # The ID, worksheet and range of a sample spreadsheet.
        # SAMPLE_SPREADSHEET_ID = "1m8jS9QNxtm1FqWP4PLc0VO2z1NQsGe-cWkwcFdd0m5Y"
        # values = [["a", 3], ["b", 5], ["c", 6]]
        body = {"values": values}
        worksheet_range = self.get_worksheet_range(worksheet, range)

        result = (
            self.sheet.values()
            .update(
                spreadsheetId=sheet_id,
                range=worksheet_range,
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )
        print(f"{result.get('updatedCells')} cells updated.")
        return result


# if __name__ == "__main__":
#     SAMPLE_SPREADSHEET_ID = "1m8jS9QNxtm1FqWP4PLc0VO2z1NQsGe-cWkwcFdd0m5Y"
#     gs = ConnectGS()
#     # data = gs.read_sheet(SAMPLE_SPREADSHEET_ID, worksheet="Produtores", range="A1:G8")
#     data = gs.write_sheet(
#         SAMPLE_SPREADSHEET_ID,
#         worksheet="testing",
#         range="A2",
#         values=[["a", 3], ["b", 5], ["c", 6]],
#     )

#     print(data)
