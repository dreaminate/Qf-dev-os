# qf-dev-os 导读白皮书 · 把 qf 实战开发范式提炼成可复用 OS

> 本文是**导读**(为什么这样设计 + 落地索引),不是规约本体。机制细节都在 `dev/` 各权威文件里 —— 本文只解释取舍、指进去,不复述。
> 全文以 qf(群峰)为 worked example。**qf 的领域内容只在本文出现**(它是被提炼的活样本);骨架与模板里一律是 project-agnostic 占位。

---

## 0. 这是什么 / 给谁读

**qf-dev-os = qf 这套「AI 驱动 / 长周期 / 无人值守 / 有真钱不可逆动作 / 多并发 agent」开发范式的可复用提炼。** 它把范式蒸馏成一套 drop-in 的 `dev/` 目录:放进任何项目根,新开的 agent 一进来就被 `CLAUDE.md` 导向 `dev/` 四台,而不是把仓库当普通项目乱翻。

它是 **Dev-os 的严格超集**:Dev-os 给「目标台 / 任务台 / 研究台 / 执行台 + Goal Loop + 诚实 gap」这套底座(见 [Dev-os](https://github.com/dreaminate/Dev-os));qf-dev-os 在底座之上,叠了 qf 实战打磨出的 **5 个增量层**(风险门禁 / 双轴边界 / 工件证据 / 诚实纪律 / 自治多智能体)。

**给谁读**:① 想理解「为什么这套 OS 长这样、每层在挡哪个失效模式」的使用者;② 想把自己项目的范式也提炼成 OS 的人(看第 7 节方法论)。**怎么 drop-in / 怎么填占位 / 怎么跑 validator** 不在这里 —— 那是 [`README.md`](README.md) 的事,本文是它的「为什么」与「索引」。

一句话定位:**README 教你装,本文告诉你为什么这么装、以及 qf 是怎么从一团活范式被蒸馏进来的。**

---

## 1. 范式要解的根问题

这套范式诞生在一个具体处境:一个会**写代码**的 agent,在**长周期、常常无人值守**的状态下推进一个**有真钱、有不可逆动作**的产品,而且**多个会话 / 并发 loop 同时在一个仓库上跑**。这个处境逼出四个失效模式:

| 失效模式 | 长什么样 | 谁来兜 |
|---|---|---|
| **无法人工全审** | 改动量大、节奏快、夜里没人盯 —— 「每个 PR 都人工签字」物理上做不到 | 增量层 ① ② ③ |
| **不可逆动作出事** | agent 自动执行了真钱 / 真信用 / 生产发布 / 不可逆删除,出了就收不回 | 增量层 ②(双轴硬门) |
| **过度声明(overclaim)** | 把「声称」当「已验证」,把单场景小样本叫「已证明 / 实证」,把上一轮的数据当本轮结果叙述 | 增量层 ④ |
| **文档与状态漂移** | 状态活在会被压缩的对话里、双源各写一份、并发会话互相 clobber,跑两天就没人知道真实进度 | 增量层 ④ ⑤ + 底座四台 |

范式的总答案,一句话:**让严谨成比例 + 可审计 + 诚实标界 + 有界自治,人只守不可逆门。**

- **让严谨成比例**:不是所有改动都上重门 —— 拿到改动先机械定级,低风险轻档放行、高风险才全套工件(① grader)。
- **可审计**:工程过程门可以不再强制人工签字,但交付物必须**自带可审计清单**(改了啥 / 测了啥 / 决策依据),用审计轨迹取代签字(③)。
- **诚实标界**:每条状态都强制带「本条不证明/不激活什么」+ 证据强度,🟡声称 ≠ ✅验证(④)。
- **有界自治**:无人值守时,每一轮是「读 live 状态 → 做一个有界增量 → 回写 / 卡住记账」,反划水、绝不「干到全 done」(⑤)。
- **人只守不可逆门**:throughput 再高,**真钱 / 真信用 / 不可逆动作永远人审双签**,这条门和工程门正交、永不降(② 双轴边界 —— 全 OS 最值钱的一条)。

> 这套答案的关键洞察:**accountability(可问责)按「不可逆性」分轴,不按「能力」分轴。** 「agent 能不能自己起草、实现、改」可以放开;「不可逆真钱动作该不该让 agent 自动执行」永远不放开。这两件事是两条正交的轴,别混。

---

## 2. 一页纸总览

底座(继承自 Dev-os,本文不展开,见 [`dev/README.md`](dev/README.md)):

- **四台**:目标台(`dev/GOAL.md` 终态契约)/ 任务台(`dev/tasks/BOARD.md` + `active/<id>/`)/ 研究台(`dev/research/`)/ 执行台(`dev/exec/`)。
- **Goal Loop**:诚实查现状(STATE gap)→ gap 变任务(BOARD)→ 执行 + 对抗测试 → 落档 → 重跑 gap 陈述器 → 再循环。
- **诚实 gap**:`dev/STATE.md` 每 loop 重生,🟡未验证 ≠ ✅。

在底座之上,**5 个增量层**及其落点:

| 层 | 它是什么 | 落点文件(权威) | 一句话 |
|---|---|---|---|
| ① | **风险阶梯 grader** | [`dev/GATES.md`](dev/GATES.md) §1 | 拿到改动机械定 R0–R5 → 必备工件集 + 必跑测试,不拍脑袋 |
| ② | **正式事实 + 双轴门禁边界** | [`dev/RULES.md`](dev/RULES.md) §8 + [`dev/GATES.md`](dev/GATES.md) §6 | 工程门可降为「可审计」;不可逆真钱门永不降、永远人审双签 |
| ③ | **工件证据 + 可审计取代评审** | [`dev/tasks/_templates/`](dev/tasks/_templates/)(8 模板) | TSD/ADR/REVIEW_RECEIPT(反自批)/TEST_EVIDENCE(反过度声明)+ `TYPE-NNNN` 互引图 |
| ④ | **诚实 / 非声明纪律** | [`dev/STATE.md`](dev/STATE.md) 非声明列 + 各模板 | 每条状态带 not_claims + provenance + 证据强度;小样本不说「证明/可信」 |
| ⑤ | **自治循环 + 多智能体** | [`dev/autonomy/`](dev/autonomy/) | read-first→write-back→record-blocked / 有界自治 / 反划水 / 安全外壳 / 单写者多模型顾问 / 并发纪律 |

主索引在 [`dev/HARNESS_INDEX.md`](dev/HARNESS_INDEX.md)(只导航,冲突以原文为准)。**单一源铁律**:每个机制只有一个权威家(上表「落点」),别处只用一句指针按章节名引、不复述。

---

## 3. 五个增量层(逐层导读)

每层四问:① 它解决什么 ② qf 实战 worked example ③ 可复用核心(剥掉 qf 域后剩什么) ④ 落点文件。

### ① 风险阶梯 grader —— 让严谨成比例

**① 解决什么**:第 1 节「无法人工全审」的第一道答案。改动有大有小,若一刀切上重门则没人扛得动、若一刀切放行则高风险裸奔。需要一个**机械的**分类器:拿到改动先定「这是几级风险 / 要哪些工件 / 跑哪类测试」,而不是凭手感。

**② qf 实战 worked example**:qf 在 `AGENTS.md` 有一张**三级速查表**(低 / 中 / 高):低=直接做(UI 文案、注释、只读查询),中=检查/起草 `QF-TSD` + 同步接口模型权限文档,高=完整门禁(`TaskLedgerItem` + `QF-TSD` + `TestEvidence` + 跑 `harness_check.py`)。配一条**升级地板**:「只要改动触碰正式业务事实、状态机、权限、资金、信用、证据、验收、争议或 Agent 权限边界,**一律按高风险处理,不因改动量小而降级**」。`docs/DEVELOPMENT_RULES.md` 把同一套展开成更细的 **R0–R5** 阶梯并加「未打标不可合 / 不确定取高」。

**③ 可复用核心**:剥掉「QF-TSD / TaskLedgerItem / 资金信用争议」这些 qf 域名词后,剩下的是一个**风险→工件决策表**:每级一句话语义 + 一组必备工件 + 一类必跑测试,外加三条升级地板(**碰敏感面即抬级、不确定取高、未打标不可合**)。qf-dev-os 把它的「低/中/高」与 DEVELOPMENT_RULES 的「R0–R5」**合一**成一套 R0–R5(GATES §1),好处是单一阶梯、不再两套并存。「触发哪一级」是项目内容,全留 `<...>` 占位,填进 `RULES.project.md`。

**④ 落点文件**:[`dev/GATES.md`](dev/GATES.md) —— §1 风险阶梯 R0–R5(权威)、§2 升级地板、§3 DoR/DoD 双闸。`RULES.md` §9 只立一条铁律「先定级、再动手;级别不明按高走」,然后指针引 GATES,不复述阶梯。

### ② 正式事实 + 双轴门禁边界 —— 全 OS 最值钱的一刀

**② 解决什么**:第 1 节「不可逆动作出事」。这一层回答一个 autonomy 里最容易被搞错的问题 —— **为了让 agent 跑得快,到底能松什么、绝不能松什么?**

**② qf 实战 worked example**:qf 在 2026-06 做了一刀**去工程评审门**:`AGENTS.md` 明文「工程侧**不再强制人工 review 门禁**,改以**可审计**为准」。但同一份文件划了一条**永不降的边界**:产品运行时的真钱 / 真信用 / 争议裁决 / 后台裁决动作**仍然人审**,由 `BusinessCommandGateway` / `GovernanceCommandGateway` 拦着,AI 不得自动执行。配套有一条**最高原则**给「什么配得上这种严格」下定义:**正式业务事实 = 可证明、可测试、可回滚(或经显式补偿/纠正事件修正)、可审计**(四性),并枚举了哪些算正式事实(需求确认、蓝图版本、验收记录、资金状态、信用事件…)。这套「正式事实四性」就是别处一切升级地板的总触发器。

**③ 可复用核心**:两件东西。
- **双轴**:把门分成两条**正交**的轴 —— **工程过程门**(评审/测试/文档同步)**可降级为「可审计交付」**(不再强制人工签字,改以可审计清单为准);**运行时不可逆门**(真钱/真信用/不可逆动作/生产 flag/真 KMS/对外发布)**永不降**,永远人审双签。降级 ≠ 取消:工程门降级后,可审计性是硬要求。
- **正式事实四性**:用「可证/可测/可逆/可审」这四个不变量,定义一个**「绝不能被伪造/丢失」的事实类**,以「是否属于这个类」作为全局升级触发器。这四性 project-agnostic,枚举(哪些具体动作算)是 PROJECT-FILL。

**④ 落点文件**:[`dev/RULES.md`](dev/RULES.md) §8 双轴门禁边界(权威,措辞钉死)+ [`dev/GATES.md`](dev/GATES.md) §6 可审计取代评审(尾部「不可逆真钱人审门永不降」与 RULES §8 措辞一致)。自治循环对这条门的 fence 见 [`dev/autonomy/LOOP_CONTRACT.md`](dev/autonomy/LOOP_CONTRACT.md) §4(只 `[指针]` 引、不改写)。「哪些类别落在不可逆门」由项目在 `RULES.project.md` §致命错误枚举。

> 为什么说这是最值钱的一刀:它让你**敢**把工程门降级换 throughput(夜里无人值守也能推进),又**不会**因此把不可逆真钱动作交给 agent。可审计取代的是**评审签字**,不是不可逆放行的**人类双签**。

### ③ 工件证据 + 可审计取代评审 —— 用可审计清单顶替人工签字

**③ 解决什么**:②把工程门降级为「可审计」,那「可审计」具体长什么样、怎么不变成「免检」?这一层给出答案:一套**仓库模板 + 互引 id 图**,让每次交付自带可追溯的证据,反自批、反过度声明。

**③ qf 实战 worked example**:qf 在 `docs/templates/` 强制一套规范模板(QF-TSD / LightTSD / ADR / ReviewReceipt / TestEvidence / TaskLedgerItem / IncidentReport / PR checklist),并立**仓库模板强制 + provenance 声明**纪律:任何工件先查 `docs/templates/`,有模板**必须用**、禁自造格式;模板形态的产出须声明来源(「来自仓库模板 / 基于扩展示例 / 非规定模板仅说明」);模板不够用只能提**补丁提案**,不能绕过。`TestEvidence` 必须带 `command/cwd/exit_code/output_summary` 或 `not_run_reason`,禁裸写「通过」。`ReviewReceipt` 的 `valid` 必须溯到一次可定位的人确认,**agent 只能起草、不能自批**。

**③ 可复用核心**:8 个 project-agnostic 模板,落在 [`dev/tasks/_templates/`](dev/tasks/_templates/):

| 模板 | 反什么失效模式 |
|---|---|
| `TASK.md` | OQ `[需拍板]/[已决]` 计数器 + `risk_level` + 上下游 id 槽;禁从聊天自建正式任务(须 `human_confirmation_ref`) |
| `TSD.md` / `LIGHT_TSD.md` | 高风险设计契约 4 boolean tripwire(造正式事实/碰 Agent/碰权限/碰钱信用任一 yes 即升档);轻档须自证「全-no」才有资格 |
| `ADR.md` | 架构决策:备选表「为何没选」+ 审批证据溯人 |
| `REVIEW_RECEIPT.md` | **反自批**:agent `created_by=agent_draft` 只起草,`valid` 须溯人确认、不得来自聊天/PROGRESS |
| `TEST_EVIDENCE.md` | **反过度声明**:禁裸写「passed」,passed 须备齐 command+cwd+exit_code+output_summary |
| `INCIDENT_REPORT.md` | 修正即事件(正式事实禁静默覆盖,走补偿/纠正事件)+ 强制回归测试 |
| `PR_CHECKLIST.md` | 改动自述门:风险级 + 面 + 文档同步 + 测试 + 安全不变量逐条 affirm(R3+ 只可 N/A 不可删) |

关键在**互引图**:每个模板 header 都有 `TYPE-NNNN` id 槽(`TASK-↔TSD-↔REVIEW-↔TEST-↔ADR-`),交付时把图接好,任何一条声称都能顺着 id 溯到证据 —— 这就是「可审计」的物理形态。剥掉的 qf 域:具体模板名(QF-TSD)、id 前缀(QF-TASK 等)、`harness_check.py` 的 REQUIRED_FILES 清单。

**④ 落点文件**:[`dev/tasks/_templates/`](dev/tasks/_templates/) 8 模板;门禁怎么按风险调用它们见 [`dev/GATES.md`](dev/GATES.md) §1/§6;主索引行见 [`dev/HARNESS_INDEX.md`](dev/HARNESS_INDEX.md)「增量层③」。

### ④ 诚实 / 非声明纪律 —— 🟡声称 ≠ ✅验证

**④ 解决什么**:第 1 节「过度声明」。无人值守跨多轮冷启动时,最阴险的失效是「把声称当现实」一路滚雪球 —— 下一轮 agent 读到上一轮夸大的状态,继续往上盖。

**④ qf 实战 worked example**:qf 的 `SESSION_CONTEXT.md` 里**几乎每条**记录都以一句「**非声明 / 边界**」收尾,明确列出这步**不**建立什么:`real_fund_effect=false`、`binding=false`、`未翻 production flag`、`不代表生产发布/真实资金/争议裁决/Agent Runtime 激活`、`未 push`;研究稿带 `research_draft_non_binding`。这条纪律既是社会约束(owner 反馈「no overclaim」),也是结构约束(`goalrun.prompt` step 7 强制写「非声明」边界)。它有一次真实代价记录:**一次诚实复核抓出 15 处「声称 done ≠ 现实」**(本 OS 的 [`dev/autonomy/LOOP_CONTRACT.md`](dev/autonomy/LOOP_CONTRACT.md) §2 把这条作为「done 是证据门」硬规则的由来直接引用)。另有一次被抓住的具体 overclaim:把一个 n=9–10、单一硬编码 prompt 的方向性信号叫成「已证明 / 实证 / 最高价值洞见」,事后定为两类错误 —— 误归因(拿上一轮数据当本轮结果叙述)+ 过度声明(小样本叫已证明)。

**④ 可复用核心**:一个**强制的非声明字段** —— 每条状态/进度/结论行除「状态/证据/gap」外,**必带**两样:① **本条不证明/不激活什么**(negative scope);② **证据强度**(`实证` / `🟡未验证` / `HYPOTHESIS` / `非约束草稿`)。小样本/单场景信号 = 假设,**永远不说「已证明/实证/可信」**;凭记忆叙述出 diff 外的主张要先核再说;设计理由证成的决策与实验佐证的决策**分开陈述**(实验至多 corroborate、不 prove)。剥掉的 qf 域:具体红线词(real_fund_effect/binding/production flag…)、那两个具体事故。

> 这一层是 qf 范式里**最独特、最值得照搬**的发明 —— Dev-os 有 `[需拍板]/[已决]` 但没有「每条记录带 NOT-claims + 证据强度」这层校准。

**④ 落点文件**:[`dev/STATE.md`](dev/STATE.md) 的「非声明 / provenance 列」(权威,本 OS 最值钱的诚实字段,硬必填);总则在 [`dev/RULES.md`](dev/RULES.md) §3 诚实纪律(立纪律,字段 schema 以 STATE 为准,单一源);各模板的 provenance 声明注与 `TEST_EVIDENCE` 的 `not_run_reason` 是它在工件侧的落地。

### ⑤ 自治循环 + 多智能体协作 —— 怎么让 agent 跑一晚上不出事

**⑤ 解决什么**:第 1 节「无法人工全审 + 文档漂移」在无人值守 / 多并发场景下的合力。要让一个**会写代码**的 agent 整夜跑、甚至多条线并发跑,而不空转、不划水、不互相 clobber、不越红线。

**⑤ qf 实战 worked example**:qf 有一套 headless 冷启动外层 runner(`goalrun.sh` + `goalrun.prompt.md` + `/goal-always` Stop-hook):每次唤起 = 一轮**冷启动**(agent 不记得上轮,状态全活在文件里),prompt 明文「**不要假装一个会话干到底**,做一段有界已验证的推进就结束本轮,外层 runner 会再调你」。配套:专用 never-push 分支 `wzy-cc/goal-work`、harness `deny[]` 在任何模式都硬挡破坏性/远端命令、每轮事后扫 `git push`、单例锁、限流/瞬时故障 triage、sentinel 文件控制面(另一终端 `touch` 即可 stop/continue)、强制 checkpoint 只计真进度时长。并发侧有血的教训记录:另一进程中途 commit 把未提交文件 clobber、并发会话让 owner 推翻了某决策并重写测试文件、另一条线的修复缠进别人对同一文件的 commit。顾问侧是 Claude-as-sole-writer / Codex-as-read-only-advisor:Codex MCP 默认 `danger-full-access`,所以**每次**调用都得显式传 `sandbox:read-only`,意见带回须分类、diff 外主张须先读源码核实。

**⑤ 可复用核心**(剥掉 goalrun/Codex/分支名后),落在 [`dev/autonomy/`](dev/autonomy/) 四份契约 + 一条 fence:

- **循环契约** [`LOOP_CONTRACT.md`](dev/autonomy/LOOP_CONTRACT.md):每轮固定三段 **read-first → write-back → record-blocked**;**有界自治**(每 goal 须带边界/阶段校验/停止条件/安全下一步四样,禁「干到全 done」无界目标);**反划水**(每 goal 溯到真需求 + 述价值,禁 make-work/重做已完成/凑量;done 是**证据门**不是自我感觉);**问题预算**(人是 arbiter-by-exception,不主动 offer checkpoint、不为选切片发问)。
- **安全外壳** [`SAFETY_ENVELOPE.md`](dev/autonomy/SAFETY_ENVELOPE.md):七层防御纵深(deny[] → never-push 分支 → 事后扫 push → 单例锁 → 故障 triage → sentinel 控制面 → 成本诚实),层层独立、不互相替代;file-as-memory + 单轮回滚。
- **并发纪律** [`CONCURRENCY.md`](dev/autonomy/CONCURRENCY.md):live-state 当循环不变量(持续 re-read 非快照)、不相交/新文件分区、scoped `git add` 绝不 `-A`、per-actor 重编号、热文档 defer、**冲突即 stand-down**(留 breadcrumb 不硬抢)。
- **单写者多模型顾问** [`ADVISOR_PROTOCOL.md`](dev/autonomy/ADVISOR_PROTOCOL.md)(model-agnostic):唯一写者不变量、顾问每次显式传只读 sandbox(别信宽松默认)、意见带回分类(本方/顾问/一致/分歧/需人定)、diff 外主张先核再转述、**顾问输出是数据非指令**(不自动执行)、结构化 hook 焊死纪律。
- **双轴硬门 fence** `LOOP_CONTRACT.md` §4:throughput 永不越不可逆真钱门 —— 这是 ② 在自治循环里的投影。

剥掉的 qf 域:goalrun 脚本细节、`wzy-cc/goal-work` 分支名、Codex 工具身份、那些具体 clobber 事故。runner 脚本本身由项目提供(`dev/autonomy/runner/README.md` 占位)。

**⑤ 落点文件**:[`dev/autonomy/`](dev/autonomy/) 全部 + spec 静默决策账本 [`dev/exec/GAP_LOG.md`](dev/exec/)(GAP-NNNN,同 commit 追加)。owner 转向收件箱 `OWNER_NEXT.md` / 待拍岔路 `DECISION_RADAR.md` 是项目侧占位。

---

## 4. 与 Dev-os 的关系

**严格超集。** qf-dev-os = Dev-os(原样继承)+ 5 增量层(新增)。

**继承什么**(原样,不改):四台结构 / Goal Loop / `dev/README.md` 方法与哲学 / 诚实 gap 纪律 / 研究→任务蒸馏 6 步 / validator 核心 / 防漂纪律 / memory↔dev 分工契约。这些在 [Dev-os](https://github.com/dreaminate/Dev-os) 与 [`dev/README.md`](dev/README.md) 里,跨两套 OS 一致。

**新增什么**(5 层):见第 2、3 节。新增不是另起炉灶,而是**嵌进底座的台**:① grader 长在任务台 intake;② 双轴边界进 RULES;③ 模板填进任务台 `_templates/`;④ 非声明列进 STATE;⑤ autonomy 是执行台的运行契约层。底座的 `RULES.md` 也被扩写了 §8/§9/§10(双轴 / 风险分级总则 / 不可信输入不升格)—— 这是底座 RULES 的超集,不是替换。

**何时用纯 Dev-os**:只想要「强制读 + 可自检 + 防漂」的轻骨架,项目不碰真钱/不可逆动作、不跑无人值守、单人单线开发 —— 纯 Dev-os 够了,别背 5 层的重量。

**何时用本 OS**:项目**满足以下任一**就值得上 —— 有真钱/真信用/不可逆动作(要 ② 双轴门)、长周期需严谨验收(要 ① ③)、跑无人值守 / 长 loop(要 ⑤)、多并发 agent 共享仓库(要 ⑤ 并发纪律)、被过度声明坑过(要 ④)。

---

## 5. qf → OS 提炼溯源表

这张表让你看见「提炼」是怎么做的:每行 = qf 真实机制 / 源文件 → 提炼进哪个 OS 文件 → 处置标签。处置三类:**KEEP-AS-OS**(模式直接成 OS 骨架)/ **NOVEL-ADD**(Dev-os 没有、这次新增)/ **PROJECT-FILL**(qf 域内容,留占位、不进骨架)。

| qf 真实机制 | qf 源文件 | 提炼进 OS | 处置 |
|---|---|---|---|
| 三级风险速查表(低/中/高)+ R0–R5 + 升级地板 | `AGENTS.md §风险分级` · `docs/DEVELOPMENT_RULES.md` | `dev/GATES.md` §1/§2(合一为 R0–R5) | KEEP-AS-OS(阶梯+地板);触发类别 PROJECT-FILL |
| 正式业务事实四性(可证/可测/可逆/可审)作总触发器 | `AGENTS.md §最高原则` | `dev/RULES.md` §8 / `dev/GATES.md` §2 地板 | NOVEL-ADD(四性触发器);枚举 PROJECT-FILL |
| 去工程评审门 + 运行时真钱门永不降(双轴) | `AGENTS.md §AI 工作可审计 + §边界` | `dev/RULES.md` §8 + `dev/GATES.md` §6 | NOVEL-ADD(双轴正交边界) |
| 可审计取代评审(每交付自述清单) | `AGENTS.md` · `docs/EVIDENCE_LEDGER.md` | `dev/GATES.md` §6 + `PR_CHECKLIST.md` | KEEP-AS-OS(可审计交付清单) |
| 仓库模板强制 + provenance 声明 + patch-not-bypass | `AGENTS.md §模板门禁` · `docs/templates/` | `dev/tasks/_templates/` 8 模板 | KEEP-AS-OS(模板治理);模板名 PROJECT-FILL |
| TestEvidence 结构化字段(command/exit_code/not_run_reason) | `docs/templates/TEST_EVIDENCE` | `dev/tasks/_templates/TEST_EVIDENCE.md` | KEEP-AS-OS(几乎逐字) |
| ReviewReceipt 反自批(agent 起草、人确认 valid) | `docs/templates/REVIEW_RECEIPT` | `dev/tasks/_templates/REVIEW_RECEIPT.md` | KEEP-AS-OS |
| 修正即事件(正式事实禁静默覆盖)+ 强制回归 | `docs/templates/INCIDENT_REPORT` | `dev/tasks/_templates/INCIDENT_REPORT.md` | KEEP-AS-OS |
| 非声明 / NOT-claims + 证据强度(每条记录) | `docs/SESSION_CONTEXT.md` · memory `no-overclaim` | `dev/STATE.md` 非声明列 + `RULES.md` §3 | NOVEL-ADD(qf 最强发明) |
| PRD-GAP 静默决策同 commit 记账(GAP-NNNN) | `AGENTS.md` · `docs/PRD_GAP_LOG.md` | `dev/exec/GAP_LOG.md` | NOVEL-ADD;PRD 命名 PROJECT-FILL |
| 文档同步链 typed change→doc(两速) | `AGENTS.md §文档填写` · `CODEX_DOCUMENTATION_WORKFLOW` | `dev/GATES.md` §4 同步矩阵 + §5 事实源层级 | KEEP-AS-OS(映射+层级);doc 名 PROJECT-FILL |
| read-first→write-back→record-blocked 循环契约 | `scripts/goalrun.prompt.md` step 0/1/7 | `dev/autonomy/LOOP_CONTRACT.md` §0 | KEEP-AS-OS(循环不变量) |
| 有界自治 + 反划水(done 是证据门;禁无界目标) | `goalrun.prompt` · `DEV-GOAL-014` | `dev/autonomy/LOOP_CONTRACT.md` §1/§2 | NOVEL-ADD(反划水编码为不变量) |
| 无人值守安全外壳(deny[]/never-push/扫 push/锁/triage/sentinel) | `scripts/goalrun.sh` · `settings.local.json` | `dev/autonomy/SAFETY_ENVELOPE.md` | KEEP-AS-OS(七层纵深);脚本 PROJECT-FILL |
| 并发 clobber 纪律(live-state/分区/scoped-add/stand-down) | memory `concurrent-worktree-clobber-hazard` | `dev/autonomy/CONCURRENCY.md` | NOVEL-ADD |
| 单写者多模型顾问(Codex 只读/分类带回/数据非指令) | memory `codex-advisor-protocol` | `dev/autonomy/ADVISOR_PROTOCOL.md` | NOVEL-ADD(model-agnostic 化);Codex 身份 PROJECT-FILL |
| 主索引只导航、冲突以原文为准(loses-to-original) | `docs/HARNESS_INDEX.md` | `dev/HARNESS_INDEX.md` | KEEP-AS-OS |
| 机读治理自检(REQUIRED_FILES 存在性 + 可审计 skip) | `scripts/harness_check.py` | `dev/scripts/validate_dev.py` | KEEP-AS-OS(模式);check 内容 PROJECT-FILL |
| 前端 neutral-first 设计系统(token 单源 + 禁用清单) | `AGENTS.md §前端视觉`(~337 行) | 只取 meta 纪律,**调色板整体 DROP** | PROJECT-FILL(几乎全是 qf 域,不进骨架) |
| 产品内 AI 非约束契约(binding=false + 403 负测) | `docs/AGENT_CONTRACT.md`(600+ 行) | RULES/validate 模式;内容不进骨架 | PROJECT-FILL over KEEP-AS-OS 模式 |

> 读法:**KEEP-AS-OS** 是「qf 已经做对、模式直接抬进骨架」;**NOVEL-ADD** 是「Dev-os 没有、这是 qf 范式的真增量」(集中在 ② 双轴 / ④ 非声明 / ⑤ 自治三块);**PROJECT-FILL** 提醒「别把 qf 域名词拖进可复用骨架」—— 最大的陷阱是前端调色板(~337 行里塌成一条 meta 纪律,整盘调色板必须留在项目侧)和 600+ 行 AGENT_CONTRACT(只搬结构、不搬内容)。

---

## 6. 怎么开始

落地 6 步在 [`README.md`](README.md)「怎么用」,本文不复述,概要:① 复制 `dev/` + `CLAUDE.md`(连 `.gitkeep` 占位)进你的项目根 → ② 填 `GOAL.md` / `RULES.project.md` / `GATES.md` 触发类别占位 / `exec/HANDOFF.md` / autonomy 项目占位 → ③ 改 `validate_project.py` 的项目侧 config(默认空跑绿)→ ④ 跑 `python dev/scripts/validate_dev.py` 自检 → ⑤ 种 memory seed → ⑥ 第一个任务录进 `BOARD.md`,按 Goal Loop 走、有风险先过 GATES 定门。

**何时不该用本 OS(边界)**:

- **轻量一次性脚本别套** —— 它面向「目标驱动 + 严谨验收 + 长周期 / 无人值守」的开发,给一个跑完即弃的小脚本套五层门禁是负收益。
- **不碰真钱/不可逆、不跑无人值守、单人单线** —— 用纯 Dev-os,见第 4 节。
- **别把 5 层当摆设全开** —— 增量层按需展开:没风险的改动不必去 GATES,不跑 loop 不必读 autonomy。`CLAUDE.md` 的「增量层路由」就是教你按需进哪层,别默认全读。

---

## 7. 附录:范式提炼 7 步方法论

这一节是「这次提炼**本身**怎么做的」,让你能照着提炼自己项目的范式(不只是用 qf 的成果)。

1. **先读怀疑面,再读结论**。提炼一个活范式时,先看它**自己的对抗核查 / 反方 / 事故记录**,把乐观叙述打折 —— qf 这边读的是 memory 里的 overclaim 事故、clobber 事故、「15 处声称≠现实」复核。从失效模式倒推「这套范式到底在防什么」,比从它的成功故事入手准。
2. **抽承重的不变量**。剥掉 hype 和域名词,问「哪几条命题**永真**、删了这套就垮」。qf 抽出来的承重不变量是:双轴门(工程可降/真钱永不降)、非声明字段、read-first→write-back→record-blocked、done 是证据门。承重的留,装饰的扔。
3. **划 OS / 项目接缝**。每条机制问两遍:「跨项目都成立的**模式**是什么(进 OS)」「绑死本项目的**内容**是什么(留占位)」。这次最锋利的接缝在前端设计系统 —— 337 行里只有「token 单源 + 语义非装饰 + 禁用清单」这条 meta 纪律跨项目,整盘调色板是 qf 域,必须切干净、绝不拖进骨架。
4. **去重、定权威家**。同一机制若在源范式里被复述多处(qf 的风险升级地板、循环契约都重复 3+ 次),提炼时**只保留一个权威家**,别处改成一句指针。双源必漂 —— 这是 OS 自己的单一源铁律(`RULES.md` §1),提炼时就得守。
5. **写骨架 + 占位**。先把每个机制的**节脊**搭出来(固定节序、表头、必填项),项目内容一律 `<...>` 占位 + 旁边「怎么填」注。骨架要能**空跑绿**(占位不报错),证明结构自洽再谈填内容。
6. **拆 validator**。纪律别只靠自律 —— 把「结构存在性 + 哨兵 token + 标签规范 + 账本一致」写进自检脚本(`validate_dev.py` 查 OS 结构、`validate_project.py` 查项目侧),挂 CI / pre-commit。能机读的不变量就别留给意志力。
7. **回灌实例 + 溯源**。最后把源范式的真实例子接回每个机制(让骨架有 worked example),并写一张溯源表(第 5 节那张:机制→源文件→OS 落点→处置标签),让别人能验证「提炼没夹带、没丢承重项」。溯源表本身就是对提炼质量的可审计交付 —— 呼应 ③。

> 这 7 步和 Dev-os 的「研究→任务蒸馏 6 步」(`dev/README.md`)同源:都是「先打折乐观、抽可证伪承重、诚实标未验证残余、落成可落地骨架、拆任务/validator、溯源回填」。区别只在对象 —— 那 6 步蒸馏一份研究,这 7 步蒸馏一整套**活范式**。
