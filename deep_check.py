import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("FEISHU_APP_ID")
APP_SECRET = os.getenv("FEISHU_APP_SECRET")
APP_TOKEN = os.getenv("FEISHU_APP_TOKEN")

def check_app_status():
    # 1. 获取 Tenant Access Token
    url_auth = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": APP_ID, "app_secret": APP_SECRET}
    token_res = requests.post(url_auth, json=payload).json()
    token = token_res.get("tenant_access_token")
    
    if not token:
        print(f"[!] 无法获取 Token: {token_res}")
        return

    print(f"[+] 成功获取 Tenant Access Token")

    # 2. 尝试获取多维表格基本信息 (检查 bitable:app 权限)
    url_app = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}"
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"[*] 正在验证对 App [{APP_TOKEN}] 的权限...")
    res = requests.get(url_app, headers=headers).json()
    
    if res.get("code") == 0:
        print(f"[SUCCESS] 权限已完全打通！能够读取表格信息。")
        print(f"表格名称: {res.get('data', {}).get('app', {}).get('name')}")
    else:
        print(f"[FAILURE] API 依然报错: {res.get('msg')}")
        print(f"错误码: {res.get('code')}")
        print(f"Log ID (可提交给飞书技术支持): {res.get('error', {}).get('log_id')}")
        
    # 3. 检查应用的可访问多维表格列表
    url_list = "https://open.feishu.cn/open-apis/bitable/v1/apps"
    res_list = requests.get(url_list, headers=headers).json()
    print(f"[*] 应用当前可看到的全部表格列表: {json.dumps(res_list.get('data', {}).get('items', []), ensure_ascii=False)}")

if __name__ == "__main__":
    check_app_status()
