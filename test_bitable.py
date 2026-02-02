import requests
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("FEISHU_APP_ID")
APP_SECRET = os.getenv("FEISHU_APP_SECRET")
APP_TOKEN = os.getenv("FEISHU_APP_TOKEN")
TABLE_ID = os.getenv("FEISHU_TABLE_ID")

def get_feishu_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": APP_ID, "app_secret": APP_SECRET}
    try:
        r = requests.post(url, json=payload).json()
        return r.get("tenant_access_token")
    except Exception as e:
        print(f"Error getting token: {e}")
        return None

def test_bitable():
    token = get_feishu_access_token()
    if not token: return
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # 1. Test List Fields
    print(f"[*] Testing List Fields for Table: {TABLE_ID}")
    url_fields = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/fields"
    res_f = requests.get(url_fields, headers=headers).json()
    print(f"List Fields Result: {json.dumps(res_f, ensure_ascii=False)}")

    # 2. Test Create Record
    print(f"\n[*] Testing Create Record for Table: {TABLE_ID}")
    url_records = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records"
    payload = {
        "fields": {
            "主题": "测试同步",
            "标题": "这是一条验证权限的测试数据",
            "链接": {"link": "https://www.google.com", "text": "测试链接"},
            "洞察": "如果看到这条数据，说明 Bitable 同步已通！",
            "时间": int(time.time() * 1000)
        }
    }
    res_r = requests.post(url_records, headers=headers, json=payload).json()
    print(f"Create Record Result: {json.dumps(res_r, ensure_ascii=False)}")

if __name__ == "__main__":
    test_bitable()
