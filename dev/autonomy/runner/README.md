# runner · 无人值守 runner 说明【项目级别】

> **OS 给契约,项目给脚本。** 本 OS 已定义无人值守的全部**契约**（`../LOOP_CONTRACT.md` 循环边界 / `../SAFETY_ENVELOPE.md` 安全外壳 / `../CONCURRENCY.md` 并发 / `../ADVISOR_PROTOCOL.md` 顾问）;
> **驱动这些契约的 runner 脚本由项目自己提供**（每个项目的 agent CLI / 唤起方式 / 验收命令不同,无法通用）。
> 本文件给一段**伪码级最小参考骨架**,说明 runner 该怎么把契约串起来 —— **照抄思路、别照抄任何具体项目的脚本**。

<!-- 格式·防跑偏 | 结构型(【项目级别】说明文):固定—— §0 OS/项目分工 · §1 runner 该做什么(对照契约) · §2 伪码骨架 · §3 项目要填的槽。
怎么填:把 §2 伪码用本项目的 agent CLI / 验收命令 / 路径实现成真脚本,放在项目里(不必放进 dev/);
本目录只留这份说明 + 契约指针,不放真脚本(真脚本含项目特定命令,属项目代码)。 -->

---

## 0. OS / 项目分工
| 谁 | 给什么 |
|---|---|
| **OS（本目录上层 `autonomy/`）** | 循环契约、安全外壳、并发纪律、顾问协议 —— **机制权威** |
| **项目** | 真 runner 脚本（唤起 agent CLI、装配 prompt、解析用量、强制 review checkpoint）+ 验收命令 + 路径/分支/sentinel 约定 |

## 1. runner 该做什么（每条对应一个契约,别自创）
- **每轮唤起一个冷启动 agent**,让它读 live 交接文件恢复状态、做一个有界增量、回写 —— 契约：`LOOP_CONTRACT.md §0`。
- **锁死专用 never-push 分支 + 单例锁 + 每轮事后扫 push** —— 契约：`SAFETY_ENVELOPE.md §2/§3/§4`。
- **故障 triage**（限流→长冷却重试 / 瞬时→短重试 / 其它→停下报警） —— 契约：`SAFETY_ENVELOPE.md §5`。
- **burst 计时 + 强制 review checkpoint**（只计有效进度轮,跑满就暂停等 sentinel） —— 契约：`SAFETY_ENVELOPE.md §6` + `LOOP_CONTRACT` burst。
- **per-goal 用量账**（只计 result 轮) —— 契约：`SAFETY_ENVELOPE.md §7`。
- **sentinel 控制面**（另一终端 stop/kill/continue/status） —— 契约：`SAFETY_ENVELOPE.md §6`。

## 2. 伪码骨架（思路级,非任何项目的真脚本）

```text
acquire_singleton_lock()                 # §4 单例锁,拿不到就退出
ensure_on_dedicated_work_branch()        # §2 切到专用 never-push 分支
active_secs = 0
loop forever:
    if sentinel("stop") exists: break
    backup(live_handoff_file)            # §8 单轮回滚备份

    result = invoke_agent_one_shot(
        prompt = assemble(LOOP_CONTRACT,  # 注入「冷启动·读 live·做一个有界增量·回写·别假装干到全完成」
                          goal_hint),
        permission = locked_down,         # §1 deny[] 全模式生效
        max_turns = <项目定>,
    )

    scan_output_for_push(result)         # §3 事后扫 push,中招就 HALT 报警
    record_usage(result)                 # §7 只在有 result 事件时计账

    case classify(result):
        ok:        active_secs += result.active_time   # 只有真出活的轮计入 burst
        quota:     long_cooldown(); continue           # §5 限流→长冷却重试
        transient: short_retry();   continue           # §5 瞬时→短重试
        other:     alert_and_stop()                    # §5 其它→停下报警

    if active_secs >= CHECKPOINT:        # §6 跑满 burst→强制 review
        human_checkpoint()               #   打印 review 清单,阻塞等 continue/stop sentinel
        active_secs = 0

release_lock()
```

## 3. 项目要填的槽
- `<本项目的 agent CLI 唤起命令 + 单次 headless 参数>`
- `<专用无人值守工作分支名>`（never-push）
- `<live 交接文件路径>` + `<单轮备份路径>` + `<usage ledger 路径>`
- `<sentinel 文件名约定 + ctl 脚本>`（stop/kill/continue/status）
- `<验收命令>`（构建 / 测试 / lint / 契约检查 —— 给 agent 当每轮收口判据,见 `GATES.md`）
- `<CHECKPOINT 时长>`（一个 burst 多久强制 review）
