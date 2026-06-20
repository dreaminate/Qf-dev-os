<!-- 格式·防跑偏 | 类型(结构型):本文件 = [权威] 主索引【开发os级别】。
固定节序:§铁律 → §读序 → §文件全表(artifact|职责|更新触发|读序) → §增量层落点 → §防漂指针。
铁律:索引只导航、冲突以原文为准(loses-to-original)、改原文同步改本表;新增 OS 文件须在此登记。 -->

# HARNESS_INDEX · 主索引【开发os级别】

> **铁律(先读)**:本表**只导航、不替代原文**。任何条目与原文冲突 → **以原文为准**(loses-to-original)。
> 改了某文件的职责/触发/读序 → **同步改本表那行**;新增 OS 文件 → **必须在此登记**,否则 `validate_dev.py` 视为漂移。
> 机制权威家在「落点」列指向的那个文件,本表**不复述机制**——据行跳到位后,必须读对应原文条款再行事。

## 怎么用本索引
1. 不确定某事归哪个文件 → 查下方「文件全表」按职责定位。
2. 拿到一个改动不知该不该上门禁 → 直接去 `dev/GATES.md`(权威 grader)。
3. 无人值守 / 长跑 → 去 `dev/autonomy/`。
4. 据索引跳到原文后 **读原文条款**,别只凭这张表的一句话职责行事。

## 读序（动手前最小集 → 按需展开）
```
CLAUDE.md(根·路由)
  → GOAL(终态) → STATE(现状 gap) → tasks/BOARD(下一步)
  → exec/HANDOFF(入口) → RULES + RULES.project + DECISIONS
  ── 有风险 ─→ GATES(定风险级+工件+测试)
  ── 无人值守 ─→ autonomy/{OWNER_NEXT 先读, DECISION_RADAR, LOOP_CONTRACT, SAFETY_ENVELOPE, CONCURRENCY, ADVISOR_PROTOCOL}
  ── 重资料 ─→ research/archive/(read-on-demand,别默认全加载)
```

## 文件全表（artifact → 职责 → 更新触发 → 读序）

> 类型:**追加**=append-only(最新在上/末) · **结构**=固定节序相对稳定 · **重生**=每 loop 整篇重写。
> 级别:**OS**=【开发os级别】勿改 · **项目**=【项目级别】填占位。`[权威]`=该机制单一源。

### 入口 / 路由
| artifact | 职责 | 更新触发 | 类型 | 级别 | 读序 |
|---|---|---|---|---|---|
| `CLAUDE.md`(根) | 慢变路由 + 通用规矩 + memory↔dev 分工 + 增量层入口 | 入口/路由本身变 | 结构 | OS | 0 |
| `dev/README.md` | OS 方法与哲学(随骨架走) | 方法论本身变 | 结构 | OS | 按需 |
| `dev/HARNESS_INDEX.md` | **本表**:全文件地图 + 导航铁律 `[权威]` | 任一 OS 文件增删/改职责 | 结构 | OS | 按需 |
| `dev/exec/HANDOFF.md` | 新 session 入口提示词(含增量步骤) | 入口流程变 | 结构 | OS+项目占位 | 1 |

### 四台核心
| artifact | 职责 | 更新触发 | 类型 | 级别 | 读序 |
|---|---|---|---|---|---|
| `dev/GOAL.md` | 终态契约:已定决策 / 硬红线 / 分期 roadmap / DoD / 验收 oracle `[权威终态]` | 终态/分期变 | 结构 | 项目 | 1 |
| `dev/STATE.md` | 现状 gap + 子系统表(含**非声明/provenance 列** `[权威]`) | 每 loop | 重生 | 项目 | 1 |
| `dev/tasks/BOARD.md` | 活跃任务板(todo/in_progress,完成即删行) | 取卡/完成 | 结构 | 项目 | 1 |
| `dev/DECISIONS.md` | 已拍板决策账本(备选/审批证据/反引) | 拍板一项 | 追加 | 项目 | 1 |
| `dev/RULES.md` | OS 铁律宪法 `[权威]` | OS 级(勿擅改) | 结构 | OS | 1 |
| `dev/RULES.project.md` | 本项目红线 / 冻结区 / 致命错误 / 风险阶梯触发条件 | 项目红线变 | 结构 | 项目 | 1 |
| `dev/ISSUES.md` | 已知问题/坑(追加) | 发现问题 | 追加 | 项目 | 按需 |
| `dev/experience.md` | 通用坑/经验 | 踩到通用坑 | 追加 | OS+项目 | 按需 |
| `dev/CODEMAP.md` | 代码结构图(autonomy 是运行契约不画进来) | 结构大改 | 结构 | 项目 | 按需 |

### 增量层① — 风险门禁（grader）
| artifact | 职责 | 更新触发 | 类型 | 级别 | 读序 |
|---|---|---|---|---|---|
| `dev/GATES.md` | **THE GRADER** `[权威]`:风险阶梯 R0–R5 + 必备工件集 + 必跑测试 + 升级地板 + DoR/DoD + 同步矩阵 + 事实源层级 + 可审计取代评审 | 阶梯/工件集变(OS 级) | 结构 | OS+触发占位 | 有风险时 |

### 增量层② — 工件证据库（8 模板,`dev/tasks/_templates/`）
| artifact | 职责 | 更新触发 | 类型 | 级别 | 读序 |
|---|---|---|---|---|---|
| `TASK.md` | 任务卡:OQ `[需拍板]/[已决]` + 计数器 + risk_level + 上下游 id 槽 | 起任务 | 结构 | OS | 起卡 |
| `TSD.md` | 高风险设计契约:4 boolean tripwire + 节脊 | 高风险设计 | 结构 | OS | ≥R3 |
| `LIGHT_TSD.md` | 轻档自降级 + 全-no checklist + 升级触发 | 低风险证明 | 结构 | OS | 低风险 |
| `ADR.md` | 决策记录:status + 备选表 + 审批证据 + 反引 | 架构决策 | 结构 | OS | 决策时 |
| `REVIEW_RECEIPT.md` | 反自批:agent 只起草、approval 溯人确认 | 复核交付 | 结构 | OS | 复核时 |
| `TEST_EVIDENCE.md` | 反过度声明:command/exit_code/status,禁裸写「通过」 | 出测试证据 | 结构 | OS | 测试后 |
| `INCIDENT_REPORT.md` | 事故单:修正即事件 + 强制回归 + 反引 | 出事故 | 结构 | OS | 事故时 |
| `PR_CHECKLIST.md` | 改动自述:风险级+面+文档同步+测试+安全不变量逐条 affirm | 收尾交付 | 结构 | OS | 交付时 |

### 增量层④ — 自治循环 + 多智能体（`dev/autonomy/`）
| artifact | 职责 | 更新触发 | 类型 | 级别 | 读序 |
|---|---|---|---|---|---|
| `LOOP_CONTRACT.md` | read-first→write-back→record-blocked + bounded-autonomy + 反划水 + question-budget `[权威]` | OS 级 | 结构 | OS | 无人值守 |
| `ADVISOR_PROTOCOL.md` | 单写者多模型顾问协议(model-agnostic) `[权威]` | OS 级 | 结构 | OS | 用顾问时 |
| `CONCURRENCY.md` | 并行 agent 共享 repo 并发纪律 + 冲突 stand-down `[权威]` | OS 级 | 结构 | OS | 多 agent |
| `SAFETY_ENVELOPE.md` | 无人值守 writer 安全外壳 + sentinel 控制面 `[权威]` | OS 级 | 结构 | OS | 无人值守 |
| `OWNER_NEXT.md` | owner 明文转向收件箱(压过自设目标) | owner 写/loop 回填 | 结构 | 项目 | **每 tick 先读** |
| `DECISION_RADAR.md` | 两阶段拍板:survey→ruling | 出岔路/拍板 | 结构 | 项目 | 拍板时 |
| `runner/README.md` | runner(无人值守脚本)由项目提供说明 + 最小参考骨架 | runner 约定变 | 结构 | 项目 | 配 runner |
| `dev/exec/GAP_LOG.md` | spec 静默决策账本 GAP-NNNN(同 commit 追加) | 静默决策 | 追加 | 项目 | 补 gap |

### 执行 / 脚本
| artifact | 职责 | 更新触发 | 类型 | 级别 | 读序 |
|---|---|---|---|---|---|
| `dev/exec/LOG.md` | session 流水(每 session 末落一行) | 每 session 末 | 追加 | 项目 | 查历史 |
| `dev/scripts/validate_dev.py` | OS 结构 + canary 自检(连带跑 project) `[权威]` | OS 级(勿擅改) | — | OS | 收尾 |
| `dev/scripts/validate_project.py` | 项目侧泛化检查(默认空跑绿) `[权威]` | 项目 config | — | OS+项目 config | 收尾 |
| `dev/scripts/build_ledger.py` | 现生成全含量任务表 | — | — | OS | 看全账 |
| `dev/scripts/build_card_counters.py` | 从 OQ 标签派生计数器写回 | — | — | OS | 起卡后 |
| `dev/scripts/build_log_index.py` | 活跃+归档 LOG 统一索引 | — | — | OS | 查归档 |
| `dev/research/` | 研究台:findings(设计接线) + archive(read-on-demand) | 出研究 | 追加 | 项目 | 按需 |

## 防漂指针（单一源）
- 风险阶梯 / 门禁工件 → **只在 `GATES.md` 展开**,别处一句指针引(按 § 名钉)。
- 可审计取代评审(工程门可降为「可审计交付」)→ 措辞以 `GATES.md §可审计` 为准,别处只 `[指针]` 引、不改写。
- 非声明 / provenance 字段语义 → 以 `STATE.md` 为准。
- 本表与任一原文冲突 → **改本表对齐原文**(原文是真理,索引是地图)。
