#!/usr/bin/env python3
"""work-discipline skill 自检：frontmatter / 中英对齐 / 路由闭合 / 品牌与掩码。

用法：
    python scripts/verify_skill.py [技能目录]

默认技能目录 = 脚本上级目录的 skills/work-discipline。
退出码：0 = 全部通过；1 = 有 FAIL；2 = 有 PARTIAL（缺依赖，未 fully 验证）。
不联网、不写文件。PyYAML 缺失时严格 YAML 解析标记为 PARTIAL，不再伪报「全部通过」。
"""
import hashlib
import io
import json
import os
import re
import sys

FAILURES = []
PARTIALS = []


def check(cond, label, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {label}" + (f"  {detail}" if detail else ""))
    if not cond:
        FAILURES.append(label)


def partial(label, reason):
    print(f"  [PARTIAL] {label}  {reason}")
    PARTIALS.append(label)


def read(path):
    return io.open(path, encoding="utf-8").read()


def frontmatter(text):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, "首行不是 ---"
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None, "frontmatter 未闭合"
    return lines[1:end], None


def description(fm):
    for i, line in enumerate(fm):
        if line.startswith("description:"):
            val = line[len("description:"):].strip()
            if val in (">-", ">", "|-", "|"):
                parts = []
                for following in fm[i + 1:]:
                    if following.startswith((" ", "\t")):
                        parts.append(following.strip())
                return " ".join(parts)
            return val
    return ""


def yaml_check(fm, label):
    try:
        import yaml
    except ImportError:
        # 关键：不再静默 SKIP 后报「全部通过」——升级为 PARTIAL 并影响退出码
        partial(f"{label} 严格 YAML 解析", "未装 PyYAML，语法未被验证（pip install pyyaml）")
        return
    body = "\n".join(fm)
    try:
        parsed = yaml.safe_load(body)
        check(isinstance(parsed, dict) and "name" in parsed and "description" in parsed,
              f"{label} 严格 YAML 解析",
              f"keys={list(parsed) if isinstance(parsed, dict) else type(parsed).__name__}")
    except Exception as exc:
        first = str(exc).splitlines()[0]
        mark = getattr(exc, "problem_mark", None)
        loc = f" line={mark.line + 1} col={mark.column + 1}" if mark else ""
        check(False, f"{label} 严格 YAML 解析", f"{type(exc).__name__}: {first}{loc}")


def structural_fingerprint(text):
    """结构指纹：比条目数之外的骨架特征，能抓出数量相同但内容错配/漂移。"""
    headings = len(re.findall(r"^#{1,6} ", text, re.M))
    items = len(re.findall(r"^- ", text, re.M)) + len(re.findall(r"^\d+\. ", text, re.M))
    bold_pairs = text.count("**") // 2
    table_rows = len(re.findall(r"^\|", text, re.M))
    code_fences = text.count("```")
    backtick_spans = text.count("`") - code_fences * 2
    return {"条目": items, "标题": headings, "粗体": bold_pairs,
            "表格行": table_rows, "代码围栏": code_fences, "反引号": backtick_spans}


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    skill_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "skills", "work-discipline")
    skill_dir = os.path.abspath(skill_dir)
    print(f"技能目录: {skill_dir}\n")

    print("=== 1. frontmatter ===")
    pair = [("CN", "SKILL.md"), ("EN", "SKILL.en.md")]
    for label, filename in pair:
        path = os.path.join(skill_dir, filename)
        if not os.path.exists(path):
            check(False, f"{label} 文件存在", path)
            continue
        text = read(path)
        fm, err = frontmatter(text)
        if err:
            check(False, f"{label} frontmatter", err)
            continue
        logical = []
        skip_cont = False
        for line in fm:
            if skip_cont and line.startswith((" ", "\t")):
                continue
            skip_cont = False
            if line.startswith(("description:", "name:")) and line.split(":", 1)[1].strip() in (">-", ">", "|-", "|"):
                skip_cont = True
            logical.append(line)
        check(len(logical) == 2, f"{label} frontmatter 仅 name + description", f"折叠后 {len(logical)} 字段")
        desc = description(fm)
        check(0 < len(desc) <= 1024, f"{label} description 长度", f"{len(desc)} / 1024")
        yaml_check(fm, f"{label}")

    print("\n=== 2. 中英结构对齐（数量 + 骨架指纹）===")
    files = [
        ("主文件", "SKILL.md", "SKILL.en.md"),
        ("执行层", "references/execution-layer.md", "references/execution-layer.en.md"),
        ("委托层", "references/delegation-layer.md", "references/delegation-layer.en.md"),
        ("记忆维护", "references/memory-maintenance.md", "references/memory-maintenance.en.md"),
        ("项目笔记", "references/project-notes.md", "references/project-notes.en.md"),
    ]
    for label, cn_rel, en_rel in files:
        cn_path = os.path.join(skill_dir, cn_rel)
        en_path = os.path.join(skill_dir, en_rel)
        if not (os.path.exists(cn_path) and os.path.exists(en_path)):
            check(False, f"{label} 中英文件齐备")
            continue
        c = structural_fingerprint(read(cn_path))
        e = structural_fingerprint(read(en_path))
        drift = {k: (c[k], e[k]) for k in c if c[k] != e[k]}
        check(not drift, f"{label} 中英结构对齐", "全部一致" if not drift else f"漂移 {drift}")

    print("\n=== 3. 路由闭合（正向存在 + 反向覆盖）===")
    main_cn = read(os.path.join(skill_dir, "SKILL.md"))
    main_en = read(os.path.join(skill_dir, "SKILL.en.md"))
    refs_dir = os.path.join(skill_dir, "references")
    disk_files = sorted(
        f for f in os.listdir(refs_dir)
        if f.endswith(".md") and os.path.isfile(os.path.join(refs_dir, f))
    ) if os.path.isdir(refs_dir) else []
    for label, text, want_suffix in [("CN", main_cn, ".md"), ("EN", main_en, ".en.md")]:
        refs = set(re.findall(r"`(references/[A-Za-z0-9_.-]+\.md)`", text))
        missing = [r for r in refs if "*" not in r and not os.path.exists(os.path.join(skill_dir, r))]
        check(not missing, f"{label} 路由指向的文件存在", f"引用 {len(refs)} 个，缺失 {missing}")
        wildcards = [t for t in re.findall(r"`([^`]+)`", text) if "*" in t]
        unindexed = []
        for f in disk_files:
            if want_suffix == ".md" and f.endswith(".en.md"):
                continue
            rel = f"references/{f}"
            covered_wildcard = any(
                (w == "references/*.en.md" and f.endswith(".en.md")) or
                (w == "references/*.md" and not f.endswith(".en.md"))
                for w in wildcards
            )
            if rel in refs or covered_wildcard:
                continue
            unindexed.append(rel)
        check(not unindexed, f"{label} 所有 references 文件已被索引", f"漏索引 {unindexed}")

    print("\n=== 4. 品牌与凭据 ===")
    all_md = []
    for root, _, names in os.walk(skill_dir):
        for name in names:
            if name.endswith(".md"):
                all_md.append(os.path.join(root, name))
    skill_md = [p for p in all_md if os.path.dirname(p).endswith("work-discipline")]
    branded = [p for p in skill_md if "WorkBuddy" in read(p)]
    check(not branded, "规则正文无 WorkBuddy 品牌字样", f"命中 {len(branded)} 个文件")
    bad_mask = []
    for p in all_md:
        for line in read(p).split("\n"):
            if ("前 4 位" in line or "first 4" in line) and not any(
                neg in line for neg in ("禁止", "Never", "no longer", "未暴露", "收紧", "tighten")
            ):
                bad_mask.append(os.path.basename(p))
                break
    check(not bad_mask, "掩码规则未正向暴露前 4 位", f"命中 {bad_mask}")

    print("\n=== 5. 文件哈希（供远端比对）===")
    for path in sorted(all_md):
        digest = hashlib.md5(open(path, "rb").read()).hexdigest()
        print(f"  {digest}  {os.path.relpath(path, skill_dir).replace(os.sep, '/')}")

    print("\n=== 6. manifest 与分发产物 ===")
    repo = os.path.dirname(here)
    mpath = os.path.join(repo, "manifest.json")
    if not os.path.exists(mpath):
        partial("manifest 存在", "仓库根缺 manifest.json（无 Python 时无法做哈希自检）")
    else:
        try:
            manifest = json.loads(read(mpath))
        except Exception as exc:
            check(False, "manifest 可解析", str(exc))
            manifest = {}
        entries = manifest.get("files", {})
        mismatch = []
        for rel, meta in entries.items():
            candidate = os.path.join(repo, rel)
            if not os.path.exists(candidate) and rel.startswith("skills/work-discipline/"):
                candidate = os.path.join(repo, rel[len("skills/work-discipline/"):])
            if not os.path.exists(candidate):
                mismatch.append(f"{rel}(缺失)")
                continue
            h = hashlib.sha256()
            with open(candidate, "rb") as fh:
                for chunk in iter(lambda: fh.read(65536), b""):
                    h.update(chunk)
            if h.hexdigest() != meta.get("sha256"):
                mismatch.append(f"{rel}(哈希不符)")
        check(not mismatch, "manifest 全部文件 SHA256 一致",
              f"核对 {len(entries)} 个" + (f" 异常 {mismatch[:4]}" if mismatch else ""))
        check(manifest.get("version") == "5.0.0", "manifest 版本",
              f"实际 {manifest.get('version')}")

    print()
    if FAILURES:
        print(f"FAIL: {len(FAILURES)} 项未通过 -> " + "; ".join(FAILURES))
        sys.exit(1)
    if PARTIALS:
        print(f"PARTIAL: {len(PARTIALS)} 项未验证 -> " + "; ".join(PARTIALS))
        print("（未 Fully 验证，不可宣称全部通过）")
        sys.exit(2)
    print("PASS: 全部检查通过（fully verified）")


main()
