<!-- 格式·防跑偏 | 结构型(固定节序) | 【开发os级别·模板】勿改本文件。
     造卡:复制到 tasks/active/<TASK-NNNN>/TASK.md,删本注释头再填。开头声明 provenance:
       「来自仓库模板 dev/tasks/_templates/TASK.md」(正式任务=本档) /「基于仓库模板扩展示例」/「非仓库规定模板,仅为说明」。
     脚手架非枷锁:[必填]不能省;[按需]用得上才留,用不上就删;能力小就精简,别为填而填。
     ⛔ 禁从聊天/PROGRESS 自建正式任务:正式任务卡须溯到一次**可定位的人确认**(human_confirmation_ref);
        随口讨论 ≠ 任务。无外部任务系统才用本档;有则可引 external_task_ref(须含 id/owner/scope 最小 schema)。 -->

# <TASK-NNNN> · <标题>

> provenance:<来自仓库模板 dev/tasks/_templates/TASK.md>

## Header（wiring · 上下游 id 反引）
- **状态**:proposed | approved | in_progress | blocked | review | done   ·   **review_status**:0 未过目 | 1 已过目/确认
<!-- 状态=纯 enum,反映卡完善度+生命周期,**prose 别重述决策/过目**(各有专属字段)。
     **进实现须**:review_status=1 且 Open Questions 待拍=0(两闸皆过)。**done 须**:待拍=0 + 在 done/ + BOARD 标 done。
     review_status = 用户**过目/确认**(开工前过目卡 / done 后确认);0→WARN(软,不挡),过目后→1。 -->
- **risk_level**:`<R0|R1|R2|R3|R4|R5>`   <!-- 按 GATES.md §1 风险阶梯定;不确定取高(GATES §2)。决定下方必备工件/必跑测试。 -->
- **来源**:`<finding / 决策 D-NNNN / STATE gap>`  ·  **优先级**:`P?`  ·  **依赖**:`<其它任务 id>`
- **human_confirmation_ref**:`<可定位的人确认来源,非聊天/非 PROGRESS>`  <!-- 正式任务必填,见顶注禁令 -->
- **关联 id 槽**(有则填,建立可审计图):
  | 类型 | id | 说明 |
  |---|---|---|
  | 设计契约 | `<TSD-NNNN / LIGHT_TSD-NNNN>` | 高风险设计;R3+ 须有 TSD |
  | 决策 | `<ADR-NNNN / D-NNNN>` | 重大架构取舍 |
  | 评审回执 | `<REVIEW-NNNN>` | 人审结论(agent 不可自批) |
  | 测试证据 | `<TEST-NNNN>` | 可复现测试回执 |
  | 分支 | `<branch_name 占位>` | 怎么填:本任务工作分支名 |

## Scope [必填]
<单一能力单元,1 句「做什么 + 不做什么」>

## 上下文 / 动机 [按需]
<为什么现在做,链到 finding / gap / 决策>

## 接线点（file:line，实现时复核）[必填]
| 文件 | 位置 | 改什么(扩展不替换) |
|---|---|---|
| `<path>` | `<行/符号>` | `<接什么线>` |

## 对抗测试设计（种已知 bug，门必抓）[必填]
1. `<名>`:种 `<已知的坏>` → 门必 `<抓的表现>`(含变异要杀的点)

## required-docs（DoD · 按 risk_level 勾）[必填]
> 这张清单当**完成定义**的一半:本卡 risk_level 要求的文档工件齐了才算 done。具体哪些文档由 GATES.md §1 风险阶梯定。
- [ ] `<风险级要求的设计/决策文档,如 TSD / ADR;低风险可 LIGHT_TSD 或 N/A>`
- [ ] `<项目特定契约文档占位 —— 怎么填:列本项目对该改动面强制同步的契约文件名>`

## required-tests（DoD · 按 risk_level 勾）[必填]
> 完成定义的另一半:风险级要求的测试类都有 TEST-NNNN 证据(或显式 not_run + 回填 owner)。测试类由 GATES.md §1 定。
- [ ] `<单元 / 对抗 / 幂等 / 权限 / 状态机 …按风险级>` → 证据 `<TEST-NNNN>`

## 复用 [按需]
<现有可复用的 file:符号,别重造(查索引/grep 现有实现)>

## 红线 [按需]
<相关 RULES.project 红线 / 致命错误(不可逆动作即停工)>

## 非目标 [按需]
<明确不做什么,防 scope 蔓延>

## Open Questions（已决 {已决}/{总}）[按需]
<进实现前必须全部决完。需拍板的逐条标**规范标签** [需拍板](待) / [已决](已拍)——**只认这两个名、别用变体**(标签漂→计数连锁错)。**计数器 `已决 D/总` 由 `python dev/scripts/build_card_counters.py` 从标签派生写回、人别手敲**(validate 核对标签规范+计数);**已决=总(如 4/4)才可进实现**(满格=完成,直觉化)。非拍板的开口(留 hook / 归后续 / 实现时定)不标、不计入。>

## 验收一句话 [必填]
<种什么坏 → 门必抓;不破坏现有测试基线>
