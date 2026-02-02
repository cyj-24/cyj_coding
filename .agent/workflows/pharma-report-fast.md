---
description: 快速执行医药行研猎手 (Pharma Strategy Report Hunter)，自动跳过点击确认环节。
---

// turbo-all

1. 启动 `pharma_strategy_report_hunter` 技能。
2. **零干扰原则 (Zero-Confirmation Policy)**：
   - **核心规避**：严禁调用 `execute_browser_javascript` 或 `evaluate_script`（这些是触发手动确认的根源）。
   - **分析方案**：必须使用 `read_browser_page` 获取文本，将处理逻辑交给我自己的后台模型。
   - **交互限制**：仅允许使用基础点击 (`click`)、导航 (`navigate`) 和后端抓取 (`read_url_content`)。
3. **随机选择话题**：从技能内置的 50 个医药行业战略主题中随机选取一个。
4. **白名单搜寻**：在指定咨询机构域名下执行深挖。
5. **链接与输出策略**：
   - **PDF 优先**：必须在首位展示经过验证的 `.pdf` 直链。
   - **双语桥接**：中文总结，保持“面试/工作怎么用”章节输出为中文。
   - **保底方案**：如果 PDF 加密，则提供 Landing Page。
