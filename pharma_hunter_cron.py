import os
import random
import requests
import json
from openai import OpenAI
from dotenv import load_dotenv
import google.generativeai as genai
import hmac
import hashlib
import base64
import time

# 加载本地 .env 文件
load_dotenv()

# ================= 配置区 =================
# 1. 飞书机器人配置 (用于发送消息)
FEISHU_WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL")
FEISHU_SECRET = os.getenv("FEISHU_SECRET")

# 2. 飞书 Bitable 配置 (用于持久化去重数据库)
APP_ID = os.getenv("FEISHU_APP_ID")
APP_SECRET = os.getenv("FEISHU_APP_SECRET")
APP_TOKEN = os.getenv("FEISHU_APP_TOKEN")
TABLE_ID = os.getenv("FEISHU_TABLE_ID")

# 3. 搜索配置 (Serper.dev)
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# 4. AI 配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 5. 持久化存储配置
HISTORY_FILE = "sent_reports.json"

# ================= 核心逻辑 =================

def get_feishu_access_token():
    """获取飞书应用访问令牌 (Tenant Access Token)"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": APP_ID, "app_secret": APP_SECRET}
    try:
        res = requests.post(url, json=payload).json()
        return res.get("tenant_access_token")
    except Exception as e:
        print(f"[!] 获取飞书 Token 失败: {e}")
        return None

def load_history():
    """从本地 JSON 加载历史 (GitHub Actions 主方案)"""
    history = set()
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                history = set(data)
                print(f"[*] 已从本地加载 {len(history)} 条历史记录。")
        except Exception as e:
            print(f"[!] 加载本地历史失败: {e}")
    
    # 兼容/备选：从 Bitable 加载 (如果配置了且没有被墙)
    if APP_TOKEN and TABLE_ID:
        bitable_history = load_history_from_bitable()
        history.update(bitable_history)
    
    return history

def load_history_from_bitable():
    """从飞书多维表格加载已发送报告的链接 (作为备选)"""
    token = get_feishu_access_token()
    if not token: return set()
    
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records"
    headers = {"Authorization": f"Bearer {token}"}
    # 尝试加载中文字段名“链接”
    params = {"page_size": 100, "field_names": json.dumps(["链接"])}
    
    sent_links = set()
    try:
        res = requests.get(url, headers=headers, params=params).json()
        records = res.get("data", {}).get("items", [])
        for rec in records:
            # 兼容：优先读取名为“链接”或“Link”的字段
            fields = rec.get("fields", {})
            link_data = fields.get("链接") or fields.get("Link")
            if not link_data: continue
            
            if isinstance(link_data, dict):
                sent_links.add(link_data.get("link"))
            elif isinstance(link_data, str):
                sent_links.add(link_data)
        print(f"[*] 已从 Bitable 加载 {len(sent_links)} 条历史记录。")
    except Exception as e:
        print(f"[!] 加载 Bitable 历史失败: {e}")
    return sent_links

def save_history(links):
    """保存历史到本地 JSON (GitHub Actions 会自动将其 push 到仓库)"""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(list(links), f, ensure_ascii=False, indent=2)
        print(f"[+] 历史记录已更新并保存至 {HISTORY_FILE}")
    except Exception as e:
        print(f"[!] 保存本地历史失败: {e}")

def save_to_bitable(theme, title, link, insight):
    """向飞书多维表格写入记录 (作为可视化备选)"""
    if not (APP_TOKEN and TABLE_ID):
        return
    token = get_feishu_access_token()
    if not token: return
    
    # 增强逻辑：如果配置的 TABLE_ID 报错 NOTEXIST，尝试自动获取第一个表的 ID
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # 获取表格列表以验证 ID
    tables_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables"
    try:
        t_res = requests.get(tables_url, headers=headers).json()
        valid_table_id = TABLE_ID
        if t_res.get("code") == 0:
            tables = t_res.get("data", {}).get("items", [])
            table_ids = [t.get("table_id") for t in tables]
            if TABLE_ID not in table_ids and tables:
                valid_table_id = tables[0].get("table_id")
                print(f"[*] 发现 Table ID 匹配错误，已自动切换为第一个表: {valid_table_id}")
        else:
            print(f"[!] 无法获取表格列表 (可能权限不足或 ID 有误): {t_res.get('msg')}")
    except Exception as e:
        print(f"[*] 检查表格 ID 时出错: {e}")
        valid_table_id = TABLE_ID

    url_records = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{valid_table_id}/records"
    
    payload = {
        "fields": {
            "主题": theme,
            "标题": title,
            "链接": {"link": link, "text": "点击查看全文"},
            "洞察": insight,
            "时间": int(time.time() * 1000)
        }
    }
    
    try:
        response = requests.post(url_records, headers=headers, json=payload)
        res = response.json()
        if res.get("code") == 0:
            print("[+] 已成功同步至飞书多维表格。")
        else:
            log_id = res.get("error", {}).get("log_id", "N/A")
            print(f"[!] 写入 Bitable 失败: {json.dumps(res, ensure_ascii=False)}")
            print(f"[*] 请将此 Log ID 发给我以便排查: {log_id}")
    except Exception as e:
        print(f"[!] 写入 Bitable 出错: {e}")

def gen_sign(timestamp, secret):
    """飞书机器人签名校验逻辑"""
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return sign

# 战略主题池 (中英双语映射)
THEMES = {
    "Market Access": "市场准入", "VBP Impact": "集采影响", "NRDL Negotiation": "医保谈判", 
    "DRG/DIP Payment": "支付改革", "Pharma R&D Digitalization": "研发数字化",
    "AI in Drug Discovery": "AI制药", "Clinical Trial Efficiency": "临床效率", 
    "Decentralized Clinical Trials (DCT)": "远程临床试验", "Real World Evidence (RWE)": "真实世界研究", 
    "Precision Medicine": "精准医疗", "Gene Therapy": "基因治疗", "Cell Therapy": "细胞治疗", 
    "ADC Drug Market": "ADC药物", "Biosimilars": "生物类似药", "Vaccine Innovation": "疫苗创新",
    "Oncology Trends": "肿瘤趋势", "Immunology Market": "免疫市场", "Rare Diseases": "罕见病", 
    "Chronic Disease Management": "慢病管理", "CNS Trends": "中枢神经",
    "Omnichannel Marketing": "全渠道营销", "Digital Therapeutics": "数字疗法", 
    "Patient Centricity": "以患者为中心", "Launch Excellence": "卓越上市", 
    "Drug Life Cycle": "生命周期", "Pharma Supply Chain": "医药供应链", 
    "DTP Pharmacy": "DTP药房", "Internet Hospital": "互联网医院", 
    "Pharmacy Retail Strategy": "零售战略", "Lower-tier Market": "下沉市场",
    "MNC China Strategy": "跨国药企战略", "Local Biotech Rise": "本土Biotech崛起", 
    "CXO Trends": "CXO趋势", "Pharma Licensing": "医药BD交易", "Pharma M&A": "医药并购",
    "Cross-border Collaboration": "跨境合作", "Patent Cliff": "专利悬崖", 
    "Pharma Compliance": "医药合规", "ESG in Pharma": "医药ESG", "Pharma Talent Strategy": "医药人才战略",
    "Consumer Health": "消费医疗", "OTC Market": "OTC市场", "Medical Aesthetics": "医美趋势", 
    "TCM Internationalization": "中医药国际化", "Hospital Management": "医院管理策略",
    "Private Healthcare": "私立医疗", "Commercial Health Insurance": "商业医保", 
    "Drug Regulatory Reforms": "药监改革", "Patient Data Privacy": "患者数据隐私", 
    "Pharma Globalization": "药企出海"
}

# 医药行业核心关键词
PHARMA_KEYWORDS = ["pharma", "healthcare", "medical", "biotech", "医药", "医疗", "生物技术", "药企", "医院", "制药"]

def is_link_valid(url):
    """验证链接是否为活链 (200 OK)"""
    try:
        # 使用 HEAD 请求快速检查，如果被禁用则回退到 GET (stream=True 只读头)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        r = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
        if r.status_code == 200:
            return True
        # 部分服务器禁用了 HEAD，尝试 GET
        r = requests.get(url, headers=headers, timeout=10, stream=True, allow_redirects=True)
        return r.status_code == 200
    except Exception:
        return False

def get_report_from_serper(theme_en, history):
    """使用 Serper.dev 搜索顶级咨询公司的 全球 PDF 报告（通过 history 去重）"""
    theme_zh = THEMES.get(theme_en, "")
    print(f"[*] 正在搜刮顶级机构全球研报: {theme_en}...")
    url = "https://google.serper.dev/search"
    
    # 保持顶级机构设置
    sites = [
        "iqvia.com", "mckinsey.com", "bcg.com", "bain.com", "rolandberger.com", 
        "deloitte.com", "lek.com", "zs.com", "pwc.com", "ey.com", "kpmg.com", "accenture.com"
    ]
    site_query = " OR ".join([f"site:{s}" for s in sites])
    query = f"({site_query}) (Pharma OR Healthcare OR Medical) (2025 OR 2026) ({theme_en} OR {theme_zh}) (report OR whitepaper) filetype:pdf"
    
    payload = json.dumps({"q": query})
    headers = {'X-API-KEY': SERPER_API_KEY, 'Content-Type': 'application/json'}
    
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        results = response.json().get("organic", [])
        
        # 过滤与验证
        for result in results:
            link = result.get('link', '')
            title = result.get('title', '')
            snippet = result.get('snippet', '')
            
            # 1. 跳过已发送的
            if link in history:
                continue
                
            # 2. 必须包含医药行业核心关键词 (过滤杂讯)
            combined_text = (title + snippet).lower()
            if not any(kw in combined_text for kw in PHARMA_KEYWORDS):
                continue
                
            # 3. 防死链验证：必须是活链
            print(f"[*] 正在探测链接可用性: {link}...")
            if not is_link_valid(link):
                print(f"[!] 链接探测失败 (404或超时)，跳过。")
                continue
                
            # 返回第一个符合条件的
            return {
                'title': title,
                'link': link,
                'snippet': snippet
            }
        return None # If loop finishes without finding a valid report
    except Exception as e:
        print(f"[!] Serper 搜索出错: {e}")
        return None

def summarize_with_ai(report_data, theme_en):
    """提取全球研报精华并生成正式的中文战略简报"""
    if not report_data:
        return None

    theme_zh = THEMES.get(theme_en, "医药研报")
    prompt = f"""
    角色：顶级医药战略咨询顾问。
    任务：分析以下报告（可能为英文或中文），并为药企高管生成一份专业的【中文】战略简报。
    重点：侧重于报告中关于 2025-2026 年的前瞻性洞察。
    
    【核心要求】
    1. 简报语言：必须使用【中文】进行总结和提炼（即便原始报告是英文）。
    2. 真实性原则：严禁编造数据！仅提炼摘要中明确提到的比例、金额或趋势。如果没有具体数字，请进行定性描述。
    3. 行业校验：首先判断该报告是否属于医药、医疗或生物技术领域。如果不属于，请直接返回“INVALID_INDUSTRY”。
    
    【报告原始信息】
    标题: {report_data.get('title')}
    链接: {report_data.get('link')}
    摘要: {report_data.get('snippet')}
    目标医药主题: {theme_zh} ({theme_en})
    
    【输出格式】
    ### 【核心洞察】
    - (基于原文核心逻辑的中文提炼)
    ### 【关键数据】
    - (仅保留原文中出现的真实数据，无数据则写“趋势描述”)
    ### 【职场应用】
    - (提供 1-2 句高阶中文话术，适合在会议中引用)
    """

    last_error = ""
    if GEMINI_API_KEY:
        print("[*] 正在向 Gemini 3 Flash 请教洞察...")
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            # 官方正式名称：'gemini-3-flash-preview'
            model = genai.GenerativeModel('gemini-3-flash-preview')
            response = model.generate_content(prompt)
            if response.text:
                return response.text
            else:
                raise Exception("Gemini returned empty response")
        except Exception as e:
            last_error = str(e)
            print(f"[!] Gemini 调用失败: {last_error}，将尝试备用方案...")
    
    if OPENAI_API_KEY:
        print("[*] 正在使用 OpenAI/备用接口进行总结...")
        client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
        
    return f"AI 接口不可用。错误原因：{last_error or '未配置 Key'}"

def send_to_feishu(content, report_url):
    """发送消息到飞书群机器人 (使用富文本卡片格式)"""
    if not FEISHU_WEBHOOK_URL:
        print("[!] 未配置飞书 Webhook 地址。")
        return

    headers = {"Content-Type": "application/json"}
    
    # 构造卡片内容
    card_content = {
        "header": {
            "title": {"tag": "plain_text", "content": "🔍 医药行业战略情报 | Gemini 3 Flash"},
            "template": "blue"
        },
        "elements": [
            {
                "tag": "div",
                "text": {"tag": "lark_md", "content": content}
            },
            {
                "tag": "hr"
            },
            {
                "tag": "note",
                "elements": [{"tag": "plain_text", "content": "本简报由 Gemini 3 Flash 针对最新战略趋势自动生成"}]
            },
            {
                "tag": "action",
                "actions": [{
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": "查看原报告资源"},
                    "url": report_url,
                    "type": "primary"
                }]
            }
        ]
    }

    payload = {
        "msg_type": "interactive",
        "card": card_content
    }

    # 如果配置了签名，则添加签名校验
    if FEISHU_SECRET:
        timestamp = int(time.time())
        payload["timestamp"] = str(timestamp)
        payload["sign"] = gen_sign(timestamp, FEISHU_SECRET)

    r = requests.post(FEISHU_WEBHOOK_URL, headers=headers, data=json.dumps(payload))
    if r.status_code == 200:
        print("[+] 飞书推送成功！")
        return True
    else:
        print(f"[!] 飞书推送失败: {r.text}")
        return False

def main():
    # 0. 验证必要配置
    if not all([SERPER_API_KEY, GEMINI_API_KEY]):
        print("[!] 错误：缺少 AI 配置（Gemini）。")
        # 即使只有 OpenAI 也可以跑，但目前主推 Gemini
        if not OPENAI_API_KEY:
            exit(1)
        
    # 1. 加载历史 (优先 JSON)
    history = load_history()

    # 2. 随机选取一个主题进行深挖
    theme_key = random.choice(list(THEMES.keys()))
    theme_zh = THEMES[theme_key]
    
    print(f"[*] 正在搜刮顶级机构全球研报: {theme_key}...")
    
    # 3. Serper 搜刮 (带去重)
    report = get_report_from_serper(theme_key, history)
    
    if report:
        # 4. AI 深度总结
        summary = summarize_with_ai(report, theme_key)
        
        if summary and "INVALID_INDUSTRY" not in summary:
            # 5. 飞书群推送
            if send_to_feishu(summary, report['link']):
                # 6. 持久化
                # 记录到历史集合
                history.add(report['link'])
                # 保存到本地 JSON (GitHub Actions 会捕获并提交)
                save_history(history)
                # (可选) 同步到 Bitable
                save_to_bitable(theme_zh, report['title'], report['link'], summary)
                print("[+] 流程全部完成。")
            else:
                print("[!] 飞书消息发送失败。")
        else:
            print("[!] AI 总结失败或研报不符要求。")
    else:
        print("[!] 任务中止：未获取到未发送过的有效医药行业官方报告。")

if __name__ == "__main__":
    main()
