#!/usr/bin/env python3
"""work-discipline skill 自检：frontmatter 严格 YAML + 中英条目对齐 + 路由完整性。

用法：
    python scripts/verify_skill.py [技能目录]

默认技能目录 = 脚本上级目录的 skills/work-discipline。
退出码 0 = 全部通过，1 = 有失败项。
不联网、不写文件、不需要第三方库（有 PyYAML 则额外做严格解析）。
"""
import hashlib
import io
import os
import re
import sys

FAILURES = []


def check(cond, label, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {label}" + (f"  {detail}" if detail else ""))
    if not cond:
        FAILURES.append(label)


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
                # 块标量：取后续缩进行，折成一行
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
        print(f"  [SKIP] {label}: 未装 PyYAML，跳过严格解析")
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


def count_items(text):
    dash = len(re.findall(r"^- ", text, re.M))
    numbered = len(re.findall(r"^\d+\. ", text, re.M))
    return dash + numbered


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
        # 块标量（>- / > / |- / |）会多占一行，折叠后再数字段
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

    print("\n=== 2. 中英条目对齐 ===")
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
        c = count_items(read(cn_path))
        e = count_items(read(en_path))
        check(c == e, f"{label} 条目数对齐", f"CN={c} EN={e}")

    print("\n=== 3. 路由完整性 ===")
    main_cn = read(os.path.join(skill_dir, "SKILL.md"))
    main_en = read(os.path.join(skill_dir, "SKILL.en.md"))
    for label, text in [("CN", main_cn), ("EN", main_en)]:
        refs = set(re.findall(r"`(references/[A-Za-z0-9_.-]+\.md)`", text))
        missing = [r for r in refs if "*" not in r and not os.path.exists(os.path.join(skill_dir, r))]
        check(not missing, f"{label} 路由指向的文件存在", f"引用 {len(refs)} 个，缺失 {missing}")

    print("\n=== 4. 品牌与凭据 ===")
    all_md = []
    for root, _, names in os.walk(skill_dir):
        for name in names:
            if name.endswith(".md"):
                all_md.append(os.path.join(root, name))
    # 品牌检查只覆盖 skill 规则目录；README 里提及客户端面板名是合法的说明性文字
    skill_md = [p for p in all_md if os.path.dirname(p).endswith("work-discipline")]
    branded = [p for p in skill_md if "WorkBuddy" in read(p)]
    check(not branded, "规则正文无 WorkBuddy 品牌字样", f"命中 {len(branded)} 个文件")
    # 掩码：只抓"正向暴露前4+后4"的句式，放过"禁止同时暴露"这类否定句与自检说明
    bad_mask = []
    for p in all_md:
        for line in read(p).split("\n"):
            if ("前 4 位" in line or "first 4" in line) and not any(
                neg in line for neg in ("禁止", "Never", "no longer", "未暴露")
            ):
                bad_mask.append(os.path.basename(p))
                break
    check(not bad_mask, "掩码规则未正向暴露前 4 位", f"命中 {bad_mask}")

    print("\n=== 5. 文件哈希（供远端比对）===")
    for path in sorted(all_md):
        digest = hashlib.md5(open(path, "rb").read()).hexdigest()
        print(f"  {digest}  {os.path.relpath(path, skill_dir).replace(os.sep, '/')}")

    print()
    if FAILURES:
        print(f"FAIL: {len(FAILURES)} 项未通过 -> " + "; ".join(FAILURES))
        sys.exit(1)
    print("PASS: 全部检查通过")


main()
