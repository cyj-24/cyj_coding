---
name: "医药战略研报猎手"
description: "自动检索顶级咨询机构（McKinsey, BCG, IQVIA）的医药行业报告并生成战略洞察。"
---

# Pharma Strategy Report Hunter (医药行研猎手)

## 核心逻辑
本技能采用“漏斗式”筛选机制，锁定全球顶级咨询机构（MBB、IQVIA、Deloitte等）的官方 PDF 报告，提炼最具实战价值的“咨询顾问式洞察”。

## 执行流程
1. **随机聚焦**：从 50 个预设的深度话题中随机选择一个（如 VBP 影响、ADC 市场、药企出海等）。
2. **定向搜索**：通过 `site:` 指令在白名单域名中搜素最新的 PDF 报告。
3. **价值提炼**：
   - **So What?**：最核心、最反直觉的战略结论。
   - **Key Numbers**：支撑结论的硬核数据。
   - **Application**：直接可用的面试话术或汇报词（中文输出）。

## 使用工具
- `google_search`: 用于定向抓取 PDF。
- `link_reader`: 用于读取报告全文。
