import requests
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("FEISHU_APP_ID")
APP_SECRET = os.getenv("FEISHU_APP_SECRET")
APP_TOKEN = os.getenv("FEISHU_APP_TOKEN")

def diagnose_more():
    url_auth = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": APP_ID, "app_secret": APP_SECRET}
    token = requests.post(url_auth, json=payload).json().get("tenant_access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # 1. 尝试列出所有表 (再次验证)
    url_tables = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables"
    res_tables = requests.get(url_tables, headers=headers).json()
    print(f"[*] Table API Response: {res_tables}")

    # 2. 如果之前填写的 TABLE_ID 还在，尝试直接读它
    TABLE_ID = os.getenv("FEISHU_TABLE_ID")
    if TABLE_ID:
        url_records = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records"
        res_records = requests.get(url_records, headers=headers).json()
        print(f"[*] Direct Table Access [{TABLE_ID}]: {res_records.get('msg')}")

if __name__ == "__main__":
    diagnose_more()
