import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("FEISHU_APP_ID")
APP_SECRET = os.getenv("FEISHU_APP_SECRET")
APP_TOKEN = os.getenv("FEISHU_APP_TOKEN")

def get_feishu_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": APP_ID, "app_secret": APP_SECRET}
    try:
        r = requests.post(url, json=payload).json()
        return r.get("tenant_access_token")
    except Exception as e:
        print(f"Error getting token: {e}")
        return None

def find_my_bitables():
    token = get_feishu_access_token()
    if not token: 
        print("[!] 无法获取 Tenant Access Token，请检查 APP_ID 和 APP_SECRET")
        return
    
    # 获取特定多维表格下的所有表
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables"
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"[*] 正在扫描 App Token [{APP_TOKEN}] 下的所有表...")
    try:
        r = requests.get(url, headers=headers)
        print(f"[*] 状态码: {r.status_code}")
        res = r.json()
        if res.get("code") == 0:
            tables = res.get("data", {}).get("items", [])
            if not tables:
                print("[!] 未发现任何表。")
            else:
                print(f"[+] 发现 {len(tables)} 个表：")
                for t in tables:
                    print(f"---")
                    print(f"名称: {t.get('name')}")
                    print(f"Table ID (填入 .env): {t.get('table_id')}")
        else:
            print(f"[!] 扫描失败: {json.dumps(res, ensure_ascii=False)}")
    except Exception as e:
        print(f"[!] 报错: {e}")

if __name__ == "__main__":
    find_my_bitables()
