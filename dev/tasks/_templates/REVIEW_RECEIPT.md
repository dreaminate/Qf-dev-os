<!-- 格式·防跑偏 | 结构型(固定节序) | 【开发os级别·模板】勿改本文件。
     用法:证明某对象(任务/设计/决策/发布门)**经人评审**的回执;只记评审**结论**,不定义事实/行为。
     ⛔ 反自批铁律:agent 只能 created_by=agent_draft **起草**,**不得**把 status 标 valid;
        valid/approved 须溯到一次**可定位的人确认**(source_ref),且**不得**来自聊天摘要 / PROGRESS prose。
     造件:复制到对应目录,删本注释头再填。开头声明 provenance:
       「来自仓库模板 dev/tasks/_templates/REVIEW_RECEIPT.md」/「基于仓库模板扩展示例」/「非仓库规定模板,仅为说明」。 -->

# <REVIEW-NNNN> · <被评审对象简称>

> provenance:<来自仓库模板 dev/tasks/_templates/REVIEW_RECEIPT.md>

## 回执字段
| 字段 | 值 |
|---|---|
| **status** | `draft` \| `valid` \| `superseded` \| `invalid`　<!-- agent 不可置 valid;valid 须人确认 --> |
| reviewed_object | `<被审对象类型 + 路径/id + 版本。类型枚举占位:怎么填——列本项目可被审的对象类> |
| scope | `<审了什么 / 没审什么>` |
| risk_level | `<R0–R5>`（GATES.md §1） |
| reviewer | `<评审人 id / 角色>` |
| **decision** | `approved` \| `approved_with_conditions` \| `request_changes` \| `rejected` |
| conditions | `<若 approved_with_conditions:逐条;及 recheck 触发条件>` |
| **source_ref** | `<可定位的人确认来源 —— 非聊天/非 PROGRESS>` |
| **created_by** | `human` \| `agent_draft`　<!-- agent_draft 不可单独成 valid --> |

## 发现（findings + 处置）
| # | 严重度 | 发现 | 处置 / 落点(task/incident id) |
|---|---|---|---|
| 1 | `<HIGH/MED/LOW>` | `<问题>` | `<怎么解 + id>` |

## 安全核对（safe-checks · 通过项）
- `<逐条列已核对且通过的安全点>`
