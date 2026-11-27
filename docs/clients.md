# 客户端适配表

规则的正文是客户端无关的：纯祈使句、无品牌字样、不调用任何客户端 API。**绑定具体工具链的是外围三件事——装到哪、怎么唤起、怎么自证。** 这张表只说这三件事。

**数字说明**：文中的 token 数（≈1.6k / ≈3.4k）是**字符量折算的估算值**，不是任何客户端的实际计量；实际占用随分词器和实现而变，只作量级参考。「10 个规则文件」是硬事实，由 `build_dist.py` 的 `RULE_FILES` 定义并受 `--check` 门禁约束。

**证据等级**（每条都标，不留白）：

- `本机实测` — 在本仓库维护机上验证过，可复现。
- `外部实测` — 来自 2026-11-26 外部评审，在另一台机器上验证过；本机未复现，按"待复核"对待。
- `未实测` — 按该客户端通行约定填写，**安装前请先确认**，不要当成已验证事实。

## 映射表

| 客户端 / 家族 | 用户级 skill 目录 | 常驻指令落点 | 按需读文件 | 推荐形态 | 证据 |
|---|---|---|---|---|---|
| **WorkBuddy** | `~/.workbuddy/skills/` | 设置面板「给 WorkBuddy 的指令」→ `~/.workbuddy/app/app-config.json` 的 `personalization.customPrompt`（注入变量 `UserCustomPrompt`） | 支持（`Read` / `Skill` 等工具） | **目录版**：整目录 `work-discipline/` | 本机实测 |
| **Claude / Anthropic 系** | `~/.claude/skills/` | `CLAUDE.md`（用户级或项目级） | 支持 | **目录版**：整目录 + `CLAUDE.md` 里只写一行触发语 | 未实测（通行约定） |
| **豆包 / 类 Codex 桌面端** | `.user_skills`（用户级）；内置 `.skills` 会被客户端对账清理 | 客户端偏好 / 记忆设置面板 | 视实现而定 | **目录版优先**；不支持按需读时改用 `dist/` 扁平版 | 外部实测（2026-11-26 评审）；本机未复现 |
| **AGENTS.md 系**（Cursor / Cline / Codex CLI 等） | 无统一 skill 目录；通常按项目放 `AGENTS.md` | 项目根 `AGENTS.md`（用户级位置各家不同） | 通常只读单文件 | **扁平版**：把 `dist/work-discipline.flat.md` 内容并入 `AGENTS.md` | 未实测（通行约定） |
| **rules 系**（`.cursor/rules/`、`.github/copilot-instructions.md` 等） | 规则目录本身就是入口，无独立 skill 目录 | 对应的 rules 文件 | 通常只读单文件 | **扁平版**：把扁平版放入规则目录，保留 `.mdc` / 前端元数据要求时按其格式套壳 | 未实测（通行约定） |
| **Gemini CLI** | 无统一 skill 目录 | `GEMINI.md` | 视实现而定 | **扁平版**并入 `GEMINI.md` | 未实测（通行约定） |

## 三种形态怎么选

1. **目录版（默认）**：`skills/work-discipline/` 整目录。主文件只留高频规则 + 路由，细则按需读。优点：常驻 token 约 1.6k；缺点：只拷 `SKILL.md` 会静默失效。**只在客户端支持按需读文件时选这个。**
2. **扁平版（兜底）**：`dist/work-discipline.flat.md`（或 `.flat.en.md`）。全部规则内联，无路由、无外部依赖。优点：拷一个文件就完整；缺点：常驻 token 约同单文件全塞（≈3.4k），且规则顺序即优先级。**客户端只能读单文件时选这个。**
3. **英文版**：所有 `*.en.md` 是同一规则的英文翻译，不是第二个 skill。本地安装只装中文主文件即可；英文版供跨语言团队 / 对外分发。

## 常驻指令的通用写法（与客户端无关）

```
每次开工前调用 work-discipline skill（长期协作纪律）；规则一律以该 skill 正文为准，不要凭记忆复述或改写。
```

**只写两件事：什么时候调、规则在哪。** 不要复制规则正文——两份规则会冲突，且会让 agent 误以为规则已加载而跳过 skill 调用。没有 skill 机制、只能用扁平版的客户端，把上面这句改成「开工前先通读 AGENTS.md 中的纪律章节」，同样不要摘抄规则。

**职责边界**：「每次开工都调用」写在这里（宿主常驻指令），不写进 skill 的 `description`——后者只声明显式触发词，供模型判断何时相关。description 里写「任何开工场景均触发」会让所有安装它的客户端被迫每次开工加载、无法按场景关闭。

## 自证：没有 Python 也能验

仓库根的 `manifest.json` 列出每个文件的 SHA256 与字节数。**任何语言、任何系统都能只靠哈希核对**，Python 只是可选增强：

```bash
# Linux / macOS / Git Bash
sha256sum skills/work-discipline/SKILL.md
# Windows PowerShell
Get-FileHash -Algorithm SHA256 skills\work-discipline\SKILL.md
```

语义自检脚本 `scripts/verify_skill.py` **不在安装副本（10 个规则文件）里**，需从仓库另取；仓库内可用 `python scripts/verify_skill.py`，校验安装副本则要显式给清单：`python <脚本路径> <安装目录> --manifest <清单路径>`。`build_dist.py --check` 校验扁平版与 manifest 是否与源同步，同样只在仓库内有。没有 Python / 没拉脚本时，用 manifest 做哈希自证（`sha256sum` / `Get-FileHash`），这条完全离线。

## 未知客户端怎么判断（表追不上时就走这三步）

表是快照，客户端会一直变。新客户端不必等补表，现场问三个问题：

1. **能不能按需读文件？** 能 → 目录版；只能读一个文件（AGENTS.md / rules 文件）→ `dist/` 扁平版。**这条最关键，选错就是把纪律变成报错源。**
2. **用户级 skill 目录在哪？** 看该客户端有没有「用户级 skills / 全局 rules」目录；有就放进去，没有就退回项目级目录或扁平版。不确定时先查它的官方文档，别猜。
3. **常驻指令写在哪？** 找该客户端的「自定义指令 / 偏好 / CLAUDE.md / AGENTS.md / GEMINI.md」这类入口，只写一行触发语，不复制规则。找不到就先手动在开工时说一句「调用 work-discipline」，别为了触发去改配置文件。

三步都答完再装；答不出第 1 步就不要装目录版。

## 一条硬边界

**「读不到 references 就停下报错」是目录版的条款。** 扁平版已经在文件头覆盖了它——扁平版本来就没有 `references/`，照那条字面执行会每次开工报一次错，比不装还糟。给不支持按需读的客户端装目录版，等于把纪律变成报错源；装机前先确认这一栏。
