# SAFETY_ENVELOPE · 无人值守 writer 安全外壳【开发os级别】（勿改 · 跨项目一致）

> 让一个会**写代码**的 agent 整夜无人值守地跑,而**不出大事**的防御纵深。
> 这是「怎么让 agent 跑一晚上」的安全外壳 —— 模式与契约随 OS 走,具体脚本由项目提供（见 `runner/README.md`）。

<!-- 【开发os级别】勿改 · clone 自 qf-dev-os。本文件是 [权威]：无人值守安全外壳只在这里展开,别处只引。 -->
<!-- 格式·防跑偏 | 结构型(固定节序)：
§0 七层防御纵深总览 · §1 全模式 deny[] · §2 专用 never-push 分支 · §3 事后扫 push · §4 单例锁 ·
§5 限流/瞬时故障 triage · §6 sentinel 控制面 · §7 成本账诚实 · §8 file-as-memory + 回滚 · §9 上线前自检。
模式 + 占位;剥掉任何具体 runner 脚本细节。 -->

> **索引**(仅供定位)：§1 deny[] · §2 never-push 分支 · §3 push 事后扫 · §4 单例锁 · §5 故障 triage · §6 sentinel 控制面 · §7 成本诚实 · §8 file-as-memory · §9 自检。

---

## 0. 七层防御纵深（任何一层漏,还有下一层兜）
deny[]（§1）→ 专用 never-push 分支（§2）→ 事后扫 push（§3）→ 单例锁（§4）→ 故障 triage（§5）→ sentinel 控制面（§6）→ 成本诚实（§7）。**层层独立,不互相替代。**

## 1. 全 permission 模式 deny[]（硬阻断,不分模式）
在 harness 权限配置里**硬 deny 一组破坏性 / 远端动作,且在任何 permission 模式下都生效**（不因「auto 模式」松开）。典型 deny（项目按自己风险面补全）：
- `git push --force` / `--force-with-lease`、`merge`、`rebase`、`reset --hard`、`switch`/`checkout` 到主干分支、`rm -rf`、`sudo`、`<填:本项目其他不可逆/远端/特权命令>`。
- 还要 deny **破坏性 / 远端命令**（force-push / 删数据 / 部署 …具体清单由项目定）。

## 2. 专用 never-push 分支
- runner **只在一个专用工作分支**上干活（`<填:本项目专用无人值守工作分支名>`）—— **永不主干、永不别人的分支**。
- runner 自身**永不 push**：只 commit,push 留给人（防无人值守把半成品推上远端）。
> 注：若项目放开了「agent 可自 push」,push 仍须守 force-push 护栏,且本 §2「runner 不自 push」的默认假设要在 `RULES.project.md` 显式标注作废,否则按默认（不 push）。

## 3. 每轮事后扫 push（兜底权限层）
- 每轮跑完,**扫这一轮的命令输出**有没有出现 `git push`（即便 §1/§2 该挡住）—— 出现就**立刻 HALT 报警**。这是对权限层的 belt-and-suspenders 兜底。

## 4. 单例锁（防两个 runner 互相 cross-commit / 双花）
- 用**原子锁**（如 `mkdir` 锁目录 + 记 pid）保证**同时只有一个 runner 实例**在跑。
- 防两个 loop 同时改同一仓库导致交叉提交 / 重复消耗额度。

## 5. 限流 / 瞬时故障 triage（区分「等一下重试」vs「停下报警」）
失败轮要分类处理,**别带病空转**：
- **额度 / 限流**（quota / rate-limit 特征）→ **长冷却 + 重试到恢复**（额度自愈）。
- **瞬时错误**（网络抖动等）→ **短重试**。
- **其它非零退出** → **停下报警**,不 sick-spinning。
- **失败 / 限流 / 瞬时轮不计入「有效进度」**（见 §7 + `LOOP_CONTRACT` burst 计时）。

## 6. sentinel 文件控制面（另一终端控停 / 控启）
- 用 **sentinel 文件**做带外控制面：从另一个终端 `touch` 一个文件就能 **stop / kill / continue / status** 这个长跑 agent,**不必进它的会话**。
- 配套一个小 ctl 脚本封装这些 sentinel（占位：`<填:本项目 runner 控制脚本 + sentinel 文件名约定>`）。
- 强制 review 节奏也走 sentinel：跑满一个 burst（有效进度时长）→ 自动暂停、打印 review 清单、等 `continue` / `stop`（契约见 `LOOP_CONTRACT.md`,checkpoint 时长项目定）。

## 7. 成本账诚实（token 为准）
- 按轮累计 token in/out/cache + 成本 + 轮数,落一个 usage 账（占位：`<填:本项目 usage ledger 路径>`）。
- **只计真正出了结果（有 result 事件）的轮**;被打断 / 失败的轮**不写成误导性的 0**。
- 报成本以 **token 账为准**,别凭感觉说「跑了不多」。

## 8. file-as-memory + 单轮回滚
- 每轮是冷启动,**durable 状态全活在文件里**：一个**单一 live 交接文件**（`<填:本项目 SESSION_CONTEXT 式交接文件>`）—— 下一轮 agent **先读它恢复状态**（当前态 / 上轮干了啥 / 验证事实 / 非声明边界 / 下一步 / 待 owner 决策）。
- 每轮开工前**备份**该文件一份（占位：`<填:本项目交接文件的单轮备份路径>`）,支持**单轮回滚**。

## 9. 上线前自检（开跑前过一遍）
- ⬜ deny[] 在**所有** permission 模式下都挡住了 §1 那组破坏性 / 远端命令?
- ⬜ runner 锁死在专用 never-push 分支?自身不 push?
- ⬜ 每轮事后扫 push 接上了?
- ⬜ 单例锁在?两个 runner 起不来?
- ⬜ 故障 triage 区分了「等一下重试」vs「停下报警」?
- ⬜ sentinel 控制面（stop/kill/continue/status）能从另一终端控?
- ⬜ usage 账只计 result 轮、成本以 token 为准?
- ⬜ live 交接文件 + 单轮备份就位?
