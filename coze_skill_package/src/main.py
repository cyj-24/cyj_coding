import random

# 战略主题池
THEMES = [
    "Market Access", "VBP Impact", "NRDL Negotiation", "DRG/DIP Payment", 
    "Pharma R&D Digitalization", "AI in Drug Discovery", "Pharma Globalization", 
    "Cell Therapy", "Precision Medicine", "Oncology Trends", "ADC Drug Market", 
    "MNC China Strategy", "Local Biotech Rise", "Pharma Licensing"
]

def get_random_theme():
    """随机选择一个医药战略主题"""
    selected = random.choice(THEMES)
    return selected

def construct_search_query(theme):
    """构建针对顶级咨询公司的搜索指令"""
    domains = [
        "iqvia.com", "mckinsey.com", "bcg.com", "bain.com", 
        "deloitte.com", "zs.com", "kpmg.com"
    ]
    site_query = " OR ".join([f"site:{d}" for d in domains])
    return f"({site_query}) (China Pharma) (2025 OR 2026) ({theme}) filetype:pdf"

async def main(args):
    """技能执行主逻辑"""
    theme = get_random_theme()
    query = construct_search_query(theme)
    
    return {
        "selected_theme": theme,
        "search_query": query,
        "status": "Ready to search",
        "instruction": f"Please use Google Search with the generated query: {query}"
    }
