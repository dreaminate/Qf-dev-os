# GAP_LOG · spec 静默决策账本（append-only）【项目级别】

> spec 没明说、但实现时**不得不做的决策**,在**同一个 commit** 里追加一条 `GAP-NNNN` 记进这里。
> 把「隐式假设」变成「可追溯工件」—— 事后能查「这个默认值 / 算法 / schema / 流程 / 文案 当时为什么这么定」。

<!-- 格式·防跑偏 | 追加型(append-only,锁定不改既往,最新在末尾):新 gap 追加到末尾,不改既往条目。
怎么填:实现时引入任何 spec 未明确规定的 默认值/算法/schema/流程/UI文案/交互细节 → 同 commit 追一条 GAP-NNNN。
   琐碎改动(纯文案校对/空白/CSS 微调)豁免,不必记。
schema 每条必填:gap_id / created_at / source_commit / source_files / silent_section / decision / why / should_live_in / status。
status 状态机:待补 → 纳入 / 拒 / 废(见下「状态机」)。本文件 [项目级别]:条目内容随项目,机制(同-commit 追加 + 状态机)随 OS。 -->

> **status 状态机**：
> - `待补` —— 已记 gap,但「这决策该不该升进正式 spec」尚未定。
> - `纳入` —— owner / spec owner 认了,已把该决策回写进正式 spec（填 `should_live_in` 落点）。
> - `拒` —— 评估后认为不该进 spec（保持当前实现即可),记明理由。
> - `废` —— 该 gap 已不存在（相关代码删了 / 决策被另一条覆盖）。
>
> **字段说明**：`source_commit` 引入该决策的 commit;`source_files` 落在哪些文件;`silent_section` spec 里**本该规定却没规定**的那处（章节/条目 id 占位）;`decision` 实际怎么定的;`why` 依据;`should_live_in` 若纳入,该决策应回到 spec 的哪个权威家。

---

## GAP-<NNNN> · <一句话这个静默决策是什么>
- **gap_id**：GAP-<NNNN>
- **created_at**：<YYYY-MM-DD>
- **source_commit**：<引入该决策的 commit 短 sha>
- **source_files**：<落在哪些文件>
- **silent_section**：<spec 本该规定却没规定的那处 · 章节名/条目 id 占位>
- **decision**：<实现里实际怎么定的(默认值/算法/schema/流程/文案…)>
- **why**：<依据 · 为什么这么定而不是别的>
- **should_live_in**：<若纳入,该决策应回到 spec 的哪个权威家;暂未定填 `<待定>`>
- **status**：待补
