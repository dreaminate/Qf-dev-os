# DECISION_RADAR · 两阶段拍板雷达【项目级别】

> loop 跑出来的**真岔路**汇集在这里等 owner 拍板。两阶段：**survey（列岔路 + 选项）→ ruling（owner 拍 + loop 重定向）**。
> 优先级**高于自设目标**（owner 拍完,loop 据 ruling 重定向）。和 `OWNER_NEXT.md` 的区别：那里是 owner **主动**投活,这里是 loop **反向**抛出需 owner 定的岔路。

<!-- 格式·防跑偏 | 结构型(【项目级别】填):每个雷达项两阶段—— survey(loop 写) → ruling(owner 写, loop 回填重定向)。
怎么填:① loop 遇到 human-only 岔路(经济/产品判断 / 不可逆或高破坏 / 二选一,见 LOOP_CONTRACT §3 question-budget),
   在「## 待拍」加一项 survey:列真岔路 + A/B/C 选项 + 每项 provenance 标签(溯到哪条研究/需求/约束);
② owner 在该项补 ruling:选了啥 + 含义/解锁 + 怎么重定向 loop + 砍掉的选项透明列出;
③ loop 读到 ruling 后据它重定向,并把该项搬到「## 已拍板」,做 stale-cleanup(被砍选项相关的自设目标一并清掉)。
机制(高于自设、loop 据 ruling 重定向)在 LOOP_CONTRACT §3;这里只填项目岔路内容。 -->

> **provenance 标签**(每个选项必带,证明不是凭空列)：`[研究:<结论/报告>]` / `[需求:<spec/PRD id>]` / `[约束:<红线/技术约束>]` / `[owner-曾述]`。

---

## 待拍（loop 写 survey · 等 owner ruling）

### RADAR-<NNN> · <一句话岔路标题>
- **岔路**：<这是个什么决策、为什么 loop 不能自决（落到经济/产品判断 / 不可逆或高破坏 / 二选一?）>
- **选项 A**：<方案 A> — <代价/含义> · provenance：<[研究:…] / [需求:…] / [约束:…]>
- **选项 B**：<方案 B> — <代价/含义> · provenance：<…>
- **选项 C**：<可选> — <…> · provenance：<…>
- **loop 倾向**：<可选,一句话 + 理由;但不替 owner 默认>
- **ruling**：⬜ 待 owner 拍 —— `<owner 在此写:选了哪个 + 含义/解锁了什么 + 怎么重定向 loop + 砍掉了哪些(透明)>`

---

## 已拍板（loop 据 ruling 重定向后回填 · 别删,留审计）
> 格式：`### RADAR-<NNN> · <标题> — 拍于 YYYY-MM-DD`,记 owner 选了啥 + loop 怎么重定向了 + 做了哪些 stale-cleanup。

### RADAR-<NNN> · <标题> — 拍于 YYYY-MM-DD
- **owner 拍**：<选了 A/B/C> · **含义/解锁**：<…>
- **loop 重定向**：<据此改了哪个 active goal / 开了哪个新 goal>
- **砍掉的(透明)**：<被 owner 否掉的选项 + 连带清理掉的自设目标/草稿>
