---
name: pharma_strategy_report_hunter
description: 寻找并深入分析医药行业战略报告，提供咨询顾问式的洞察。
---

# Pharma Strategy Report Hunter (医药行研猎手)

## 核心逻辑 (The Thought Process)
此 Skill 的设计旨在解决“信息噪音”问题。咨询背景的候选人极其挑剔，他们不需要“新闻”，他们需要“深度洞察(Insights)”。
因此，本 Skill 采用 **“漏斗式”** 筛选机制：
1.  **第一层 (Source Filter)**: 仅通过 `site:` 指令锁定 MBB/IQVIA 等顶级机构官网，从源头杜绝营销号。
2.  **第二层 (Format Filter)**: 强制使用 `filetype:pdf`，因为深度报告通常以 PDF 白皮书形式发布，网页多为浅层资讯。
3.  **第三层 (Content Filter)**: 要求 AI 不做简单的“摘要”，而是提炼“Consulting Implications” (对战略顾问意味着什么)。

## 执行指令 (Instructions)

### 第一步：随机聚焦 (Randomize Focus)
为了避免每次都能看到相同的报告，请在开始搜索前，先从以下 **战略主题池** 中**随机**选择一个作为本次的搜索重点：
*   **Themes**: [
    Market Access (准入策略), VBP Impact (集采影响), NRDL Negotiation (医保谈判), DRG/DIP Payment (支付改革), Pharma R&D Digitalization (研发数字化),
    AI in Drug Discovery (AI制药), Clinical Trial Efficiency (临床效率), Decentralized Clinical Trials (DCT), Real World Evidence (RWE), Precision Medicine (精准医疗),
    Gene Therapy (基因治疗), Cell Therapy (细胞治疗), ADC Drug Market (ADC药物), Biosimilars (生物类似药), Vaccine Innovation (疫苗创新),
    Oncology Trends (肿瘤趋势), Immunology Market (免疫市场), Rare Diseases (罕见病), Chronic Disease Management (慢病管理), CNS Trends (中枢神经),
    Omnichannel Marketing (全渠道营销), Digital Therapeutics (数字疗法), Patient Centricity (以患者为中心), Launch Excellence (卓越上市), Drug Life Cycle (生命周期),
    Pharma Supply Chain (医药供应链), DTP Pharmacy (DTP药房), Internet Hospital (互联网医院), Pharmacy Retail Strategy (零售战略), Lower-tier Market (下沉市场),
    MNC China Strategy (跨国企战略), Local Biotech Rise (本土Biotech), CXO Trends (CXO趋势), Pharma Licensing (BD交易), Pharma M&A (医药并购),
    Cross-border Collaboration (跨境合作), Patent Cliff (专利悬崖), Pharma Compliance (医药合规), ESG in Pharma (医药ESG), Pharma Talent Strategy (人才战略),
    Consumer Health (消费医疗), OTC Market (OTC市场), Medical Aesthetics (医美趋势), TCM Internationalization (中医药国际化), Hospital Management (医院管理),
    Private Healthcare (私立医疗), Commercial Health Insurance (商业医保), Drug Regulatory Reforms (药监改革), Patient Data Privacy (数据隐私), Pharma Globalization (药企出海)
]

**Current Focus**: [此处填入你本次随机选中的主题]

### 第二步：定向捕获 (Targeted Search)
结合随机选中的主题，使用以下指令进行搜索。
*(将 `{Selected Theme}` 替换为你刚才选中的主题英文名)*

```text
(site:iqvia.com OR site:mckinsey.com OR site:bcg.com OR site:bain.com OR site:rolandberger.com OR site:deloitte.com OR site:lek.com OR site:zs.com OR site:pwc.com OR site:ey.com OR site:kpmg.com OR site:accenture.com OR site:kearney.com) (China Pharma OR 中国医药) (2025 OR 2026) ({Selected Theme}) filetype:pdf
```

### 第三步：价值评估 (Evaluate)
阅读搜索结果。
1.  **Variety Rule**: 不要总是只看第一个结果。请浏览前 10 个结果，随机挑选一个与 `{Selected Theme}` 高度相关的报告。
2.  **筛选标准**：
    *   必须涵盖 2024-2026 的最新数据。
    *   必须包含具体的数据图表，而非纯文字描述。

    *   pure marketing (公司宣传册)
    *   outdated (旧数据)

### 第三步：链接验证 (Verify Link)
**CRITICAL**: 在最终输出之前，必须验证 PDF 链接是否有效。
1.  尝试访问该 URL。
2.  如果返回 404 或无法访问：
    *   **Action**: 使用 `site:domain.com "report title"` 重新搜索该报告的最新 Landing Page。
    *   **Fallback**: 如果找不到 PDF 直链，请提供报告的官方 Landing Page（发布页）链接。
    *   **Advanced Recovery (防爬虫策略)**:
        *   如果 Landing Page 可访问但 PDF 链接隐藏（如 Deloitte/McKinsey），**必须**调用 `browser_subagent` 工具。
        *   **Prompt**: "Navigate to [Landing Page URL]. Find the 'Download PDF' button (English or Chinese). Return the direct .pdf href."
        *   获取到的直链通常无鉴权即可访问，请直接输出该 .pdf 链接。
    *   **Error Handling**: 绝不要输出未经验证的死链。

### 第四步：战略提炼 (Summarize)
请对选中的这份报告进行 **“咨询顾问式”** 解读，输出以下 3 点（中文输出）：

1.  **The "So What?" (核心洞察)**:
    *   不要废话，直接告诉我这份报告最反直觉或最重要的一个结论是什么？
    *   *Example: "虽然 VBP 导致成熟产品销售额断崖下跌，但 IQVIA 数据显示，MNC 通过‘零售渠道’和‘数字化’实现了 15% 的利润回补。"*

2.  **Key Numbers (关键数据)**:
    *   列出报告中支撑上述结论的 1-2 个硬核数据。
    *   *Example: "院外市场规模已达 800亿 RMB，CAGR 保持在 22%。"*

3.  **Application (面试/工作怎么用)**:
    *   【关键】将报告结论转化为具体的面试话术或周报汇报词（**必须输出为中文，以便直接使用**）。
    *   *Example: "面试 Tips: 如果遇到‘集采后如何增长’的 Case，直接引用此报告的‘全渠道布局模型’，能体现你的 Big Picture 思维。"*

## 输出示例 (Output Example)

**【本周严选：IQVIA 2025 中国医院药品统计报告】**
🔗 **下载链接**: [点击下载 PDF](URL)

🔹 **核心洞察**: 医院市场的“马太效应”加剧。虽然总体处方量上涨，但创新药进院的平均周期反而从 6 个月拉长到了 9 个月，意味着 Launch Strategy 必须前置到临床 II 期。
🔹 **关键数据**: Top 100 医院贡献了全市场 45% 的创新药销售额；DTP 药房处方外流率首次突破 18%。
🔹 **实战应用**: 面试时如果被问到 "Launch Excellence"，别只聊学术推广，一定要强调 **“KA Access (重点医院准入)”** 和 **“DTP 闭环”** 的重要性。
