# CONCURRENCY · 并行 agent 并发纪律【开发os级别】（勿改 · 跨项目一致）

> 多个 agent / 会话 / 长跑 loop **共享同一 repo + branch + memory** 时,怎么不互相踩。
> 不是「禁止并行」,是「并行时各自守这套,别 clobber 别人」。

<!-- 【开发os级别】勿改 · clone 自 qf-dev-os。本文件是 [权威]：并发纪律只在这里展开,别处只引。 -->
<!-- 格式·防跑偏 | 结构型(固定节序)：
§0 前提 · §1 live-state 当循环不变量 · §2 不相交/新文件分区 · §3 scoped-add 绝不 -A · §4 per-actor 重编号 · §5 热文档 defer · §6 冲突 stand-down · §7 交接/patch lane · §8 自检。
改内容别动节骨架。 -->

> **索引**(仅供定位)：§0 前提 · §1 live-state 不变量 · §2 分区 · §3 scoped-add · §4 重编号 · §5 热文档 defer · §6 stand-down · §7 patch lane · §8 自检。

---

## 0. 前提：共享态是「活的、会被别人改的」,不是快照
多 actor 并行的真实事故（qf 实测）：① 另一进程任务中途 commit,把你没提交的文件 clobber 了;② 并行会话让 owner 推翻了某决策、重写了一个测试文件;③ 另一条线的修复缠进了别人对同一文件的 commit。**根因都是把共享态当快照。** 下面每条都是为防这三类。

## 1. live-state 当循环不变量（持续 re-read,不只开头读一次）
- 编辑共享文件**前 AND 中**,反复读 live 状态：`git status` / `git diff` / `git reflog` + 项目的 live 任务交接文件（`<填:本项目的 .ai/current_task 式 live 任务/owner 决策单一真相文件>`）。
- 那个 live 任务文件 = owner **当前**决策的真相源,**当可变,不当快照**。开头读到的,提交前要再确认 HEAD 没动、文件没被别人改。

## 2. 不相交 / 新文件分区（避免编辑战）
- 各 actor 认领**不相交的文件集**;**优先新建文件 / 文件夹**,挑一个不撞的域做。
- 能开新文件就别去改公共热文件;非改不可的公共文件 → 走 §5 defer。

## 3. scoped `git add`：绝不 `-A` / `-a`
- 只 `git add` **你这一片**的文件,**绝不** `git add -A` / `git commit -a`。
- 每次提交前**核对无泄漏**：排除别人的改动 / owner 的编辑 / 共享文档 / `.DS_Store` 等噪声。
- **频繁小提交**;每次提交后**复查 HEAD 没被并发 commit 移走**。

## 4. per-actor id / 号 重编号（防 ≥2 actor 从同一基底自增撞号）
- 两个以上 actor 从同一基底各自递增（证据 id / migration 号 / 任务号 / `TYPE-NNNN`）→ **必然撞号**。
- 落地前**重新编号**到不冲突的值;`CONCURRENCY` 下「号」从来不是你一个人在发。

## 5. 热文档 defer —— 不 race
- 高频争用的共享文档（`<填:本项目的 SPEC / PROGRESS / BOARD 等热文档>`）→ **defer**：把你的改动**攒着 / 单独记**,别和别人 race 着改同一段。
- 宁可晚一步合,别抢着 land 把别人的覆盖掉。

## 6. 冲突即 stand-down（留 breadcrumb,不硬抢）
- 遇真冲突,或读到「这文件刚被改过 / 别 revert」这类信号 → **stand down**：**不覆盖**别人的改动,**不硬抢着 land**。
- 在 live 任务文件留**交接 breadcrumb**（我本想做啥 / 停在哪 / 为什么让路）,把这片让出去,自己换一片能自治推进的活（呼应 `LOOP_CONTRACT.md §0 record-blocked`）。

## 7. gitignored 交接 / patch lane
- in-progress 的补丁存到**gitignored 的 patch 目录**（`<填:本项目的 .ai/patches 式 gitignored 暂存区>`）—— 它能扛过 `reset` / `checkout`,不随分支动作丢。
- 给 advisor 的上下文**在 prompt 里传**,别经共享黑板文件传（共享黑板会被并发写花;见 `ADVISOR_PROTOCOL.md`）。

## 8. 一次并发提交自检
- ⬜ 提交前重读了 `git status/diff/reflog` + live 任务文件?HEAD 没被别人移走?
- ⬜ `git add` 只加了**我这一片**?没 `-A`?核对过无泄漏（别人改动 / owner 编辑 / 噪声文件）?
- ⬜ 我发的 id / 号和并发 actor 不撞?撞了重编号了?
- ⬜ 热文档我是 defer 而不是 race?
- ⬜ 遇冲突 / 「别 revert」信号时 stand-down 了、留了 breadcrumb,而不是硬覆盖?
