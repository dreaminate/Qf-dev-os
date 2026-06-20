<!-- 格式·防跑偏 | 结构型(固定字段) | 【开发os级别·模板】勿改本文件。
     用法:任何「测过 / 通过 / 没跑」的声称都必须归到本档的可复现回执。validate_project 会查本档字段 token,
       字段名(command/cwd/exit_code/status/output_summary/not_run_reason)是硬约定,别改名。
     ⛔ 反过度声明:禁裸写「passed/通过/绿了」——passed 须同时给 command + cwd + exit_code + output_summary;
        没跑须写 not_run_reason + 回填 owner(谁、何时补)。🟡 声称 ≠ ✅ 验证(RULES §诚实纪律)。
     造件:复制到对应目录,删本注释头再填。开头声明 provenance:
       「来自仓库模板 dev/tasks/_templates/TEST_EVIDENCE.md」/「基于仓库模板扩展示例」/「非仓库规定模板,仅为说明」。 -->

# <TEST-NNNN> · <测了什么>

> provenance:<来自仓库模板 dev/tasks/_templates/TEST_EVIDENCE.md>

## Header（wiring）
| 字段 | 值 |
|---|---|
| task_id | `<TASK-NNNN>` |
| tsd_ref | `<TSD-NNNN —— 若验证某 INV-* / 状态机>` |
| risk_level | `<R0–R5>`（GATES.md §1 决定必跑测试类） |

## 运行记录（passed 须备齐 command+cwd+exit_code+output_summary）
| 字段 | 值 |
|---|---|
| **command** | `<完整命令,可原样复跑>` |
| **cwd** | `<执行目录>` |
| started / finished_at | `<时间>` |
| environment | `<环境/版本占位>` |
| **exit_code** | `<0 / 非0>` |
| **status** | `passed` \| `failed` \| `partial` \| `not_run` |
| **output_summary** | `<关键输出摘要,如「N passed / M failed」——别裸写「通过」>` |
| **not_run_reason** | `<status=not_run 必填:为何没跑 + 回填 owner(谁/何时补)>` |
| operator | `human` \| `agent` |

## Scope（验证覆盖面）
- changed_area:`<改了哪块>`
- code_paths_verified:`<实际被测到的路径>`
- risk_level 要求的测试类是否齐:`<对照 GATES §1;缺的列出 + not_run 原因>`
