<!-- 格式·防跑偏 | 结构型(固定节序) | 【开发os级别·模板】勿改本文件。
     用法:架构决策记录(重大架构取舍 / R4 变更)。决策账本本体在 dev/DECISIONS.md(append-only)——
       ADR 是其**单条决策的展开档**;DECISIONS 留一行指针引本 ADR id,别两处重述(单一源,见 RULES §单一源)。
     造件:复制到对应目录,删本注释头再填。开头声明 provenance:
       「来自仓库模板 dev/tasks/_templates/ADR.md」/「基于仓库模板扩展示例」/「非仓库规定模板,仅为说明」。 -->

# <ADR-NNNN> · <决策标题>

> provenance:<来自仓库模板 dev/tasks/_templates/ADR.md>

## Header（wiring · 反引）
| 字段 | 值 |
|---|---|
| **status** | `proposed` \| `accepted` \| `deprecated` \| `superseded` |
| supersedes / superseded_by | `<ADR-NNNN / —>` |
| review_receipt_ref | `<REVIEW-NNNN —— 人审回执>` |
| tsd_refs | `<TSD-NNNN —— 落地本决策的设计契约>` |
| task_refs | `<TASK-NNNN>` |
| 关联 | `<相关需求/代码/数据 占位>` |

## 1. 背景 / 问题
<要决什么;约束与压力>

## 2. 决策
<选了什么,一句话能复述>

## 3. 备选方案（含「为何没选」）
| 方案 | 优点 | 缺点 | 为何**没**选 |
|---|---|---|---|
| `<A · 选中>` | … | … | （选中） |
| `<B>` | … | … | `<被排除的真实理由>` |
| `<C>` | … | … | `<…>` |

## 4. 影响
<对架构/数据/接口/后续工作的影响;残余风险>

## 5. 审批证据（approval evidence）
> agent 可起草,但 status=accepted 须溯到**可定位的人确认**(非聊天/非 PROGRESS)。
| 字段 | 值 |
|---|---|
| decision_scope | `<本决策约束的范围>` |
| source_ref | `<可定位的人确认来源>` |
| accepted_at | `<日期>` |
| confirmed_by | `<人>` |
| follow_up_docs | `<需同步更新的文档 占位>` |

## 6. 后续动作
- `<落地任务 / 要建的工件 / 要改的文档>`
