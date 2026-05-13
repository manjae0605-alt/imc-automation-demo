"""
구글시트 → data.json
매일 09:00 KST에 GitHub Actions가 이 스크립트를 실행해
시트 데이터를 받아와 data.json으로 저장합니다.
"""

import os
import json
import gspread
from google.oauth2.service_account import Credentials


def fetch_data():
    print("🚀 시트 데이터 가져오기 시작...")

    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    service_account_info = json.loads(os.environ['GOOGLE_JSON_KEY'])
    creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
    client = gspread.authorize(creds)

    sheet_id = os.environ['SHEET_ID']
    sheet = client.open_by_key(sheet_id).sheet1

    rows = sheet.get_all_records()
    rows = [r for r in rows if r.get('BRAND')]

    print(f"✅ {len(rows)}개 행 로드 완료")

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print("✅ data.json 저장 완료")


if __name__ == "__main__":
    fetch_data()
