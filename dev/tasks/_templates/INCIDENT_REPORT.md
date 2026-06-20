<!-- 格式·防跑偏 | 结构型(固定节序) | 【开发os级别·模板】勿改本文件。
     用法:事故/缺陷复盘单。⛔ 修正即事件:正式事实的修正**禁静默覆盖**——须走「修正事件 / 补偿事件 / 引用人工决策的命令」
        前向追加(corrections are events, not silent overwrites)。⛔ 强制回归测试:每单必产一个复现本事故的回归测试。
     造件:复制到对应目录,删本注释头再填。开头声明 provenance:
       「来自仓库模板 dev/tasks/_templates/INCIDENT_REPORT.md」/「基于仓库模板扩展示例」/「非仓库规定模板,仅为说明」。 -->

# <INC-NNNN> · <事故标题>

> provenance:<来自仓库模板 dev/tasks/_templates/INCIDENT_REPORT.md>

## Header（wiring · 反引）
| 字段 | 值 |
|---|---|
| **severity** | `<SEV-1|SEV-2|SEV-3 —— 怎么填:按本项目严重度定义,见 RULES.project / GATES>` |
| status | `open` → `mitigated` → `corrected` → `closed` |
| incident_owner | `<人>` |
| review_receipt_ref | `<REVIEW-NNNN>` |
| test_evidence_refs | `<TEST-NNNN —— 含强制回归测试>` |

## 1. 影响范围
<受影响对象 / 命令 / 用户 / 数据账 / 集成 占位>

## 2. 根因
<5-why;为什么门没抓住(门是纸做的?)>

## 3. 即时缓解
<冻结了什么 / 改了什么开关 占位>

## 4. 修正 / 补偿（禁静默覆盖）
> 正式事实只能前向修正:走修正事件 / 补偿事件 / 引用人工决策的命令——别直接改库覆盖既往。
- correction/compensation 事件:`<事件 + 引用的人工决策 + 证据 id>`

## 5. 新增测试（强制回归 · checklist）
- [ ] **回归测试**:复现本事故的探针(种这个已知坏,门必抓) → 证据 `<TEST-NNNN>`
- [ ] `<相关补强测试>`

## 6. 更新的文档
- `<同步更新的 RULES.project / TSD / GATES 触发条件 等>`

## 7. 评审
<本单经谁过目;reviewer / source_ref(非聊天) —— 见 REVIEW_RECEIPT 反自批规则>
