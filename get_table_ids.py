import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("FEISHU_APP_ID")
APP_SECRET = os.getenv("FEISHU_APP_SECRET")
APP_TOKEN = os.getenv("FEISHU_APP_TOKEN")

def get_tables():
    url_auth = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": APP_ID, "app_secret": APP_SECRET}
    token = requests.post(url_auth, json=payload).json().get("tenant_access_token")
    
    if not token:
        print("[!] Token 获取失败")
        return

    # 获取该 BNR 下的所有表
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables"
    headers = {"Authorization": f"Bearer {token}"}
    
    res = requests.get(url, headers=headers).json()
    if res.get("code") == 0:
        tables = res.get("data", {}).get("items", [])
        print(f"[+] 找到 {len(tables)} 个数据表:")
        for t in tables:
            print(f"- 表名: {t.get('name')}, Table ID: {t.get('table_id')}")
    else:
        print(f"[!] 获取失败: {res.get('msg')}")

if __name__ == "__main__":
    get_tables()
