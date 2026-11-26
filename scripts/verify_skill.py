#!/usr/bin/env python3
"""work-discipline skill 自检：frontmatter / 中英对齐 / 路由闭合 / 品牌与掩码。

用法：
    python scripts/verify_skill.py [技能目录] [--manifest <清单路径>]

默认技能目录 = 脚本上级目录的 skills/work-discipline。
manifest 来源：显式 --manifest 优先；未指定时仅在「目标位于脚本所在仓库内」时自动用仓库清单。
校验任意安装副本必须显式传 --manifest，否则哈希校验标记 PARTIAL，拒绝用仓库自身清单冒充。
退出码：0 = 全部通过；1 = 有 FAIL；2 = 有 PARTIAL（缺依赖或未验哈希，不 fully verified）。
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
    args = sys.argv[1:]
    manifest_arg = None
    if "--manifest" in args:
        idx = args.index("--manifest")
        if idx + 1 >= len(args):
            print("FAIL: --manifest 后必须跟清单路径")
            sys.exit(1)
        manifest_arg = os.path.abspath(args[idx + 1])
        del args[idx:idx + 2]
    skill_dir = os.path.abspath(args[0]) if args else os.path.join(here, "..", "skills", "work-discipline")
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
    # all_md 已由 os.walk(skill_dir) 收集，天然限定在被校验目录内。
    # 不要再按目录名过滤——安装目录一改名，被检集合会变空集，检查恒过（静默失效）。
    branded = [p for p in all_md if "WorkBuddy" in read(p)]
    check(not branded, "规则正文无 WorkBuddy 品牌字样",
          f"检查 {len(all_md)} 个 md，命中 {len(branded)} 个")
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

    print("\n=== 6. manifest 哈希校验（必须校验你指向的目录）===")
    repo = os.path.dirname(here)
    default_mpath = os.path.join(repo, "manifest.json")
    is_repo_layout = os.path.normcase(os.path.abspath(
        os.path.join(skill_dir, "..", ".."))) == os.path.normcase(os.path.abspath(repo))

    # 清单来源判定：显式 --manifest 优先；否则仅在仓库布局下用仓库自带清单。
    # 绝不能用「脚本所在仓库」的清单去校验一个任意安装目录——那是自我验证，不是验证目标。
    mpath = manifest_arg or (default_mpath if is_repo_layout else None)
    if not mpath:
        partial("安装副本哈希校验", "未指定 --manifest，且目标不在仓库布局内；"
                "仓库自带清单不覆盖任意安装目录，拒绝用它冒充校验结果")
    elif not os.path.exists(mpath):
        check(False, "manifest 存在", mpath)
    else:
        mode = "显式清单" if manifest_arg else "仓库自带清单"
        print(f"  清单来源: {mpath}（{mode}）")
        try:
            manifest = json.loads(read(mpath))
        except Exception as exc:
            check(False, "manifest 可解析", str(exc))
            manifest = {}
        entries = manifest.get("files", {})
        mismatch = []
        checked = 0
        for rel, meta in entries.items():
            # 清单里的路径是仓库相对路径；只对落到被校验目录内的条目做哈希比对。
            if rel.startswith("skills/work-discipline/"):
                local_rel = rel[len("skills/work-discipline/"):]
                candidate = os.path.join(skill_dir, local_rel.replace("/", os.sep))
            elif rel.startswith(("docs/", "dist/", "scripts/", ".github/")) or rel in ("README.md", "README.en.md", "LICENSE"):
                continue  # 仓库外围文件不属于安装副本，不参与 install 模式校验
            else:
                candidate = os.path.join(skill_dir, rel.replace("/", os.sep))
            if not os.path.exists(candidate):
                mismatch.append(f"{rel}(缺失)")
                continue
            h = hashlib.sha256()
            with open(candidate, "rb") as fh:
                for chunk in iter(lambda: fh.read(65536), b""):
                    h.update(chunk)
            checked += 1
            if h.hexdigest() != meta.get("sha256"):
                mismatch.append(f"{rel}(哈希不符)")
        check(not mismatch, "目标目录与 manifest SHA256 一致",
              f"核对 {checked} 个" + (f" 异常 {mismatch[:4]}" if mismatch else ""))
        check(bool(manifest.get("version")), "manifest 版本字段存在",
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
