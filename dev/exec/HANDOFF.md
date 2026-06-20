<!-- 格式·防跑偏 | 类型(结构型):入口提示词,慢变;进度/下一步在 BOARD/STATE 不写这里。
增量步骤(GATES/autonomy/可审计清单)是增量层入口,机制权威在各自文件、这里只串流程。 -->

# HANDOFF · 新 session 入口提示词【开发os级别】（结构随骨架走 · 含项目 `<填>` 占位）

> **慢变 · 怎么更新**:只在**入口/路由本身**变时改;进度、下一步全在 `BOARD`/`STATE`(实时源)、**不写进这里** —— 不需要 per-loop 刷新。

把下面整段复制给新 session 即可接上:

---
继续在本项目用 dev/ 开发 OS 干活。先读 dev/ 四台,再按 BOARD 接着建。

1. 读 `dev/GOAL.md`(终态) + `dev/STATE.md`(现状 gap) + `dev/tasks/BOARD.md`(下一步) + `dev/RULES.md`(OS 铁律) + `dev/RULES.project.md`(本项目红线) + `dev/DECISIONS.md`(已决,不重议)。不确定归属查 `dev/HARNESS_INDEX.md`;重资料 `dev/research/archive/` read-on-demand。
   - **无人值守 / 长跑**:先看 `dev/autonomy/`——**若 `OWNER_NEXT.md` 存在先读它**(owner 转向压过自设目标),再 `DECISION_RADAR.md`(待拍岔路) + `LOOP_CONTRACT`/`SAFETY_ENVELOPE`/`CONCURRENCY` 契约。
2. 按 BOARD 取**最高优先 `todo`**(以 BOARD 实时为准,**别在此写死 task id**——防漂)。读对应 `dev/research/findings/` 设计的接线 + 对抗测试要点。
3. **定门禁**:改动有风险(碰核心契约/状态机/权限/不可逆迁移/高破坏面 等)→ 先去 `dev/GATES.md` 按风险阶梯 R0–R5 定 **风险级 + 必备工件集(用 `tasks/_templates/` 模板)+ 必跑测试**;不打风险标不可进实现。
4. 复用现有模块(**<填:本项目可复用的模块/范式>**),写实现 + 对抗测试(「种已知 bug 门必抓」),跑绿测试(命令:**<填,如 `<项目测试命令>`>**),证据落 `TEST_EVIDENCE`(禁裸写「通过」)。
5. 完成(**可审计交付清单**):`tasks/active/<id>/` 落档到 `tasks/done/<id>/`、更新 `BOARD.md`、刷新 `STATE.md`(诚实标 ✅/🟡/⬜ + 非声明/provenance 列)、按 `GATES.md §可审计取代评审` 自述「改了啥 / 测了啥 / 决策」、跑 `python dev/scripts/validate_dev.py`。
6. 红线见 `RULES.md`(通用) + `RULES.project.md`(本项目);不擅自 commit;致命错误即停工。遇 `DECISIONS.md` 没覆盖的新岔路、**或 BOARD/卡标注的前置闸门(若有)**,停下问用户(无人值守按 `LOOP_CONTRACT` question-budget 处理)。

先用三五句复述你的理解 + 当前任务的设计要点,再动手。
---
