#!/usr/bin/env python3
# <!-- 【项目级别】填 | 类型(脚本·按项目改 config) : 默认全空 → 跑绿;每个 config 都附「怎么填」;空配置零报错 -->
"""项目专属检查（**【项目级别】填**）。`validate_dev.py` 会自动连带跑本文件的 `project_checks`。

这是把通用 harness（工程治理自检）泛化成**空配置占位**的项目侧校验器：
OS 结构由 `validate_dev.py` 管（勿改）；本文件管**你这个项目**的锚点 / 旧路径 / 冻结区 /
必含 token / 账本三向一致 / 活跃 goal 预览字段 / 脚本语法。**所有 config 默认空 → 跑绿**，
按项目逐个填即生效。别为了通过把检查删掉——空着就是中性的。

适配本项目就改下面 7 个 config（各带「怎么填」）：
  PROJECT_ANCHORS         项目关键文件存在性
  STALE_PREFIXES          活跃文档不该再出现的"迁移前旧路径"
  FREEZE_GLOBS            冻结区 glob（命中 → 提示走协商，非硬阻断）
  REQUIRED_TOKENS         file → 必含 token（如 TestEvidence schema / 运行时安全锚）
  LEDGER_CONSISTENCY      目录 ↔ 其 index README ↔ 中央 trace 三向一致（双向）
  ACTIVE_GOAL_PREVIEW_FIELD 活跃 goal 文件须带被 runner 消费的预览字段（done/archived 跳过）
  SYNTAX_LINT_SCRIPTS     对配置脚本跑 `bash -n`（无 bash 优雅跳过）

退出码由 `validate_dev.py` 统一汇报；本文件只回 (oks, fails)，签名 `project_checks(DEV, ROOT)` 勿动。
"""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

# ── 项目配置（填这里；默认全空 → 跑绿）────────────────────────────────

# PROJECT_ANCHORS：项目关键文件存在性检查（相对**仓库根** ROOT）。
# 怎么填：列你这项目"丢了就出大事"的低频核心文件——主入口 / 核心 schema / 关键契约。
#   例：["app/main.py", "app/models/__init__.py", "docs/API_SPEC.md"]
PROJECT_ANCHORS: list[str] = [
    # "<项目关键文件路径>",
]

# STALE_PREFIXES：活跃文档里不该再出现的"迁移前旧路径"（防悬空引用）。
# 怎么填：做完目录搬迁后，把**旧前缀**列进来，扫 LIVE_DOCS 里是否还残留旧链接。
#   例：["docs/old_location/", "src/legacy/"]
STALE_PREFIXES: list[str] = [
    # "<迁移前旧路径前缀>",
]

# 活跃文档集（被 STALE_PREFIXES 扫描；append-only 的 DECISIONS 不在内，旧路径可作历史保留）。
# 这是 OS 默认四台活跃面，一般不用改。
LIVE_DOCS: list[str] = [
    "GOAL.md", "STATE.md", "RULES.md", "RULES.project.md", "README.md", "ISSUES.md",
    "tasks/BOARD.md", "research/INDEX.md", "exec/HANDOFF.md", "exec/LOG.md",
]

# FREEZE_GLOBS：冻结区 glob（相对 ROOT）。命中存在的文件 → **提示走协商**（非硬阻断 FAIL；
# 真正"碰冻结区即停"的红线在 dev/RULES.project.md + dev/GATES.md §升级地板，这里只做可见性兜底）。
# 怎么填：把"改它须先和 owner 协商 / 须升 ≥R3"的区域 glob 列进来。
#   例：["app/payment/**", "app/governance/constitution/**", "migrations/**"]
FREEZE_GLOBS: list[str] = [
    # "<冻结区 glob>",
]

# REQUIRED_TOKENS：file（相对 DEV）→ 必含 token 列表。用于"契约文件的关键字段不准被静默删"。
# 怎么填：挑**结构字段**而非散文（散文一改名就误报）。两类典型：
#   ① 工件 schema 锚：TEST_EVIDENCE 模板须含 command/cwd/exit_code/status/output_summary/not_run_reason；
#   ② 运行时安全锚：你项目的"命令网关 / 禁自动执行不可逆动作"等边界字眼，确保它不被悄悄抹掉。
#   例：{
#       "tasks/_templates/TEST_EVIDENCE.md": ["command", "cwd", "exit_code", "status", "output_summary", "not_run_reason"],
#       "RULES.project.md": ["<不可逆动作须人审的边界字眼>"],
#   }
REQUIRED_TOKENS: dict[str, list[str]] = {
    # "<相对 dev/ 的文件>": ["<必含 token>", ...],
}

# LEDGER_CONSISTENCY：账本三向一致（managed_dir ↔ index README ↔ 中央 trace）。**双向**校验：
#   目录下每个被管理文件（除 README）须 ① 出现在该目录 index README ② 出现在中央 trace 文件。
# 怎么填：用于"明细清单 + 索引 + 全局 trace 三处必须同步"的场景。
#   - "managed_dir": 相对 ROOT 的被管理目录；扫其 *.<ext> 文件
#   - "index": 该目录内的索引文件名（相对 managed_dir，默认 "README.md"）
#   - "trace": 相对 ROOT 的中央追踪文件，须引用每个被管理文件
#   - "ext": 被管理文件后缀（默认 "md"）
#   - "trace_back_tokens"(可选): 反向——中央 PRD/总纲文件须含的指针 token（确保总纲指回明细体系）
#   例：[{
#       "managed_dir": "docs/product/frontend-requirements",
#       "index": "README.md",
#       "trace": "docs/product/PRD_DETAIL_REQUIREMENTS_TRACE.md",
#       "ext": "md",
#   }]
LEDGER_CONSISTENCY: list[dict] = [
    # {"managed_dir": "<被管理目录>", "index": "README.md", "trace": "<中央 trace 文件>", "ext": "md"},
]

# ACTIVE_GOAL_PREVIEW_FIELD：活跃 goal 文件须带被 runner（无人值守脚本）消费的"预览字段"。
# done/archived 的 goal 由自治循环归档，不强制保留（只看 metadata 头判，避免正文里 "status: done" 误判）。
# 怎么填：runner 在终端列 goal 时要显示一行预览，这里校验每个活跃 goal 都带得上。
#   - "dir": 相对 ROOT 的 goal 目录
#   - "glob": goal 文件名模式（如 "*_GOAL.md"）
#   - "preview_anchors": 任一命中即视为带了预览字段（与 runner 的取值锚保持一致！）
#   - "done_anchor"(可选): metadata 头里判 done/archived 的正则（默认覆盖 done/completed/archived/superseded）
#   - "head_lines"(可选): 只在前 N 行 metadata 区判 done（默认 25）
#   例：{
#       "dir": "docs/dev-goals",
#       "glob": "*_GOAL.md",
#       "preview_anchors": ["one_liner", "一句话目标", "使命"],
#   }
ACTIVE_GOAL_PREVIEW_FIELD: dict | None = None

# SYNTAX_LINT_SCRIPTS：对配置脚本跑 `bash -n`（语法体检；脚本是载荷时别等运行时才炸）。
# 无 bash → 优雅跳过（不报错）。怎么填：列你那些"坏了会拖垮无人值守 loop"的 bash 脚本（相对 ROOT）。
#   例：["scripts/runner.sh", "scripts/runner-ctl.sh"]
SYNTAX_LINT_SCRIPTS: list[str] = [
    # "<bash 脚本路径>",
]
# ────────────────────────────────────────────────────────────────────


def _check_anchors(ROOT: Path, oks: list[str], fails: list[str]) -> None:
    for rel in PROJECT_ANCHORS:
        if "<" in rel:  # 占位行跳过
            continue
        (oks if (ROOT / rel).is_file() else fails).append(f"项目锚点 {rel}")
    if not [r for r in PROJECT_ANCHORS if "<" not in r]:
        oks.append("（未配置项目锚点，跳过）")


def _check_stale(DEV: Path, oks: list[str], fails: list[str]) -> None:
    real_pre = [p for p in STALE_PREFIXES if "<" not in p]
    hits = 0
    for rel in LIVE_DOCS:
        p = DEV / rel
        if not p.is_file():
            continue
        text = p.read_text(encoding="utf-8")
        for pre in real_pre:
            if pre in text:
                fails.append(f"活跃文档 {rel} 含迁移前旧路径 `{pre}`（悬空引用）")
                hits += 1
    if not real_pre or hits == 0:
        oks.append("活跃文档无迁移前旧路径悬空引用")


def _check_freeze(ROOT: Path, oks: list[str], fails: list[str], warns: list[str]) -> None:
    """冻结区：命中存在文件 → WARN（提示走协商），不 FAIL。真硬门在 RULES.project + GATES §升级地板。"""
    real = [g for g in FREEZE_GLOBS if "<" not in g]
    if not real:
        oks.append("（未配置冻结区 glob，跳过）")
        return
    touched = []
    for g in real:
        if any(ROOT.glob(g)):
            touched.append(g)
    if touched:
        warns.append(f"冻结区 glob 有文件 {touched} —— 改动须走协商 / 按 GATES §升级地板升 ≥R3（可见性提示，非阻断）")
    else:
        oks.append("冻结区 glob 当前无文件")


def _check_required_tokens(DEV: Path, oks: list[str], fails: list[str]) -> None:
    real = {f: toks for f, toks in REQUIRED_TOKENS.items() if "<" not in f}
    if not real:
        oks.append("（未配置 REQUIRED_TOKENS，跳过）")
        return
    for rel, tokens in real.items():
        p = DEV / rel
        if not p.is_file():
            fails.append(f"REQUIRED_TOKENS 目标文件缺失 {rel}")
            continue
        text = p.read_text(encoding="utf-8")
        missing = [t for t in tokens if "<" not in t and t not in text]
        if missing:
            fails.append(f"{rel}: 缺必含 token {missing}（契约关键字段被静默删？）")
        else:
            oks.append(f"必含 token 齐全 {rel}")


def _check_ledger(ROOT: Path, oks: list[str], fails: list[str]) -> None:
    """三向一致（双向）：managed_dir 每个文件 ↔ 出现在 index README ↔ 出现在中央 trace。"""
    real = [c for c in LEDGER_CONSISTENCY if "<" not in str(c)]
    if not real:
        oks.append("（未配置 LEDGER_CONSISTENCY，跳过）")
        return
    for cfg in real:
        mdir = cfg.get("managed_dir", "")
        ext = cfg.get("ext", "md")
        index_name = cfg.get("index", "README.md")
        trace_rel = cfg.get("trace", "")
        dir_path = ROOT / mdir
        index_path = dir_path / index_name
        trace_path = ROOT / trace_rel if trace_rel else None
        if not dir_path.is_dir():
            fails.append(f"账本一致：被管理目录缺失 {mdir}")
            continue
        if not index_path.is_file():
            fails.append(f"账本一致：索引缺失 {mdir}/{index_name}")
            continue
        index_text = index_path.read_text(encoding="utf-8")
        trace_text = trace_path.read_text(encoding="utf-8") if (trace_path and trace_path.is_file()) else None
        if trace_rel and trace_text is None:
            fails.append(f"账本一致：中央 trace 缺失 {trace_rel}")
        ok_count = 0
        for f in sorted(dir_path.glob(f"*.{ext}")):
            if f.name == index_name:
                continue
            rel_path = f.relative_to(ROOT).as_posix()
            if f.name not in index_text:
                fails.append(f"{mdir}/{index_name}: 漏登被管理文件 `{f.name}`")
            elif trace_text is not None and rel_path not in trace_text:
                fails.append(f"{trace_rel}: 漏登被管理文件 `{rel_path}`")
            else:
                ok_count += 1
        # 反向：中央总纲须含指回明细体系的指针 token
        for tok in cfg.get("trace_back_tokens", []):
            if "<" in tok or trace_text is None:
                continue
            if tok not in trace_text:
                fails.append(f"{trace_rel}: 缺指回明细体系的指针 token `{tok}`")
        if ok_count:
            oks.append(f"账本三向一致 {mdir}（{ok_count} 项 ↔ index ↔ trace）")


def _check_goal_preview(ROOT: Path, oks: list[str], fails: list[str]) -> None:
    cfg = ACTIVE_GOAL_PREVIEW_FIELD
    if not cfg or "<" in str(cfg):
        oks.append("（未配置 ACTIVE_GOAL_PREVIEW_FIELD，跳过）")
        return
    goals_dir = ROOT / cfg.get("dir", "")
    if not goals_dir.is_dir():
        oks.append(f"（goal 目录 {cfg.get('dir','')} 不存在，跳过预览字段检查）")
        return
    glob = cfg.get("glob", "*_GOAL.md")
    anchors = [a for a in cfg.get("preview_anchors", []) if "<" not in a]
    if not anchors:
        oks.append("（ACTIVE_GOAL_PREVIEW_FIELD 未给 preview_anchors，跳过）")
        return
    head_lines = int(cfg.get("head_lines", 25))
    done_re = re.compile(
        cfg.get("done_anchor", r"status\**\s*[:：|]\s*\**\s*(done|completed|archived|superseded)"),
        re.I,
    )
    preview_re = re.compile("|".join(re.escape(a) for a in anchors), re.I)
    checked = 0
    for gf in sorted(goals_dir.glob(glob)):
        try:
            text = gf.read_text(encoding="utf-8", errors="replace")
        except Exception as exc:
            fails.append(f"{gf.relative_to(ROOT).as_posix()}: 读取失败 {exc}")
            continue
        # done 只在 metadata 头判，避免正文 "status: done" 误判而漏校
        head = "\n".join(text.splitlines()[:head_lines])
        if done_re.search(head):
            continue
        checked += 1
        if not preview_re.search(text):
            rel = gf.relative_to(ROOT).as_posix()
            fails.append(f"{rel}: 缺 goal 预览字段（需含 {anchors} 任一，供 runner 终端选择预览）")
    if checked and not any("goal 预览字段" in f for f in fails):
        oks.append(f"活跃 goal 均带 runner 预览字段（{checked} 个）")


def _check_syntax_lint(ROOT: Path, oks: list[str], fails: list[str]) -> None:
    real = [s for s in SYNTAX_LINT_SCRIPTS if "<" not in s]
    if not real:
        oks.append("（未配置 SYNTAX_LINT_SCRIPTS，跳过）")
        return
    bash = shutil.which("bash")
    if not bash:
        oks.append("（系统无 bash，跳过脚本语法检查）")
        return
    for rel in real:
        path = ROOT / rel
        if not path.is_file():
            continue  # 脚本不存在不算项目侧错（存在性归 PROJECT_ANCHORS）
        try:
            result = subprocess.run(
                [bash, "-n", str(path)], capture_output=True, text=True, timeout=20
            )
        except Exception as exc:  # pragma: no cover - defensive
            fails.append(f"{rel}: bash -n 无法运行 ({exc})")
            continue
        if result.returncode != 0:
            fails.append(f"{rel}: bash 语法错误 — {result.stderr.strip()[:200]}")
        else:
            oks.append(f"脚本语法 OK {rel}")


def project_checks(DEV: Path, ROOT: Path) -> tuple[list[str], list[str]]:
    """返回 (oks, fails)。所有 config 默认空 → 全部走"跳过"分支，零 FAIL。
    注：本签名被 validate_dev.py import，勿改。冻结区是 WARN，并入 oks 文案不阻断退出码。"""
    oks: list[str] = []
    fails: list[str] = []
    warns: list[str] = []

    _check_anchors(ROOT, oks, fails)
    _check_stale(DEV, oks, fails)
    _check_freeze(ROOT, oks, fails, warns)
    _check_required_tokens(DEV, oks, fails)
    _check_ledger(ROOT, oks, fails)
    _check_goal_preview(ROOT, oks, fails)
    _check_syntax_lint(ROOT, oks, fails)

    # WARN 并入 oks 文案前缀，让 validate_dev 的报告能看到、但不计入 FAIL 退出码。
    for w in warns:
        oks.append(f"⚠️ {w}")

    return oks, fails
