# work-discipline

长期协作纪律与行为准则。把「怎么和人协作」固化成一套可执行的硬规则：开工前先复述与理清、扫技能要联网搜候选并加权、受阻先查资料、交活只认证据、高危先确认；线上变更与派活各有完整方法论。

中英双份，规则逐条对应。

## 能力

- **开工先复述理清**：动手前用自己的话复述目标与问题，拆出工作条目，把用户原话整理成明确的任务定义交用户确认；简单任务复述完直接做，不为流程而拖。
- **扫 skills 与 MCP**：联网搜真实候选（不局限于已安装的），按任务匹配度、环境兼容性、维护活跃度、引入成本四项加权判断；缺能力先问，不擅自安装。
- **受阻先查资料**：路径、接口、报错推进不下去时先查官方文档与社区方案，禁止凭记忆猜。
- **交活附证据**：前后对比 / 测试 / 回读值 / 链接，「我修好了」不算。
- **硬边界**：删除、发布、强推、迁移、上传外部、读取密钥与用户数据等先确认再动；凭据在任何输出里只以掩码形式出现。
- **执行层（做对）**：线上变更与批量作业七步法——备份分析 → 列工作条目 → 最小改动 → 小样测试 → 大批量 → 三轮 review → 复盘，每步必须有产出物。
- **委托层（交对）**：派活给 AI / 下属 / 自动化时按四时机动作——开工前复述、执行中消除瓶颈、交活只认证据、出错时改环境。

## 触发方式

- **显式触发词**：用户说「按记忆执行」「自检」「列出任务」「开工前确认」「self-check」「list tasks」「confirm before starting」时触发。
- **负边界**：日常闲聊、单句问答、纯信息查询不必触发；本 skill 的 description 不声明「任何开工场景均触发」。
- **「每次开工都调用」属宿主常驻指令职责**：写在客户端的常驻指令里（见下方安装第 2 步），不写进 skill 的 description——否则每个装了它的客户端都被强制每次开工加载，与客户端无关的使用场景无法关闭。
- 命中线上写操作 / 批量作业 / 派活 / 改记忆时，主文件会路由到 `references/` 下对应的细则文件——**这一步是硬要求，读不到文件必须停下报错，不许凭印象补齐**。

## 安装与恢复

**安装单位是一个目录，不是一个文件。** 一个 skill = 一个目录，目录里的 `SKILL.md` 是唯一入口，其余文件是随它走的附属资源。

1. **整目录拷贝**：把 `skills/work-discipline/` 整个目录放进用户级 skills 目录（常见形态：`~/.workbuddy/skills/`、`~/.claude/skills/`），最终形如：

   <!-- SLOT:install-tree -->
   <!-- BEGIN GENERATED:install-tree -->
   ```text
   <用户级 skills 目录>/
   └── work-discipline/
       ├── SKILL.md
       ├── SKILL.en.md
       └── references/
           ├── execution-layer.md
           ├── execution-layer.en.md
           ├── delegation-layer.md
           ├── delegation-layer.en.md
           ├── memory-maintenance.md
           ├── memory-maintenance.en.md
           ├── project-notes.md
           └── project-notes.en.md
   ```
   <!-- END GENERATED:install-tree -->

   ⚠️ **只拷 `SKILL.md` 会坏掉**：主文件里写着「涉及线上写操作、批量作业、派活时必须先读 `references/` 对应文件」，缺了这些文件，执行层与委托层的细则会整体失效，而且**是静默失效**——skill 照样能加载，只是规则被跳过。所以复制时务必带上整个目录。

2. **常驻钩子（是触发器，不是规则副本）**：在客户端的常驻指令设置里写一句「每次开工前调用 work-discipline skill；规则一律以该 skill 正文为准」。位置随客户端而异——WorkBuddy 对应设置面板里的「给 WorkBuddy 的指令」（本地落盘为 `~/.workbuddy/app/app-config.json` 的 `personalization.customPrompt`）。

   ⚠️ **不要把规则正文复制进去**。两份规则并存会互相冲突，而冲突的规则会被随机挑一条；更隐蔽的是，常驻指令长得像规则，agent 会以为规则已加载，**反而跳过 skill 调用**——这比没有钩子更糟。

3. **跨设备恢复（git 优先）**：`git clone https://github.com/shenghua520/work-discipline.git`，把 `skills/work-discipline/` 整目录覆盖到本地 skills 目录。拉取失败就用现有本地副本，禁止阻断工作。
4. **无 git 时的恢复路**（本机 git 不在 PATH 时实测可用，按可行性排序）：

   - **zip / tarball**：仓库首页 `Code` → `Download ZIP`，解压后把 `skills/work-discipline/` 整目录拷到用户级 skills 目录。
   - **逐文件 raw 下载（bash）**：

     <!-- SLOT:bash-download -->
     <!-- BEGIN GENERATED:bash-download -->
     ```bash
     BASE="https://raw.githubusercontent.com/shenghua520/work-discipline/main/skills/work-discipline"
     DEST="$HOME/.workbuddy/skills/work-discipline"   # 按客户端调整
     for f in SKILL.md SKILL.en.md references/execution-layer.md references/execution-layer.en.md \
       references/delegation-layer.md references/delegation-layer.en.md \
       references/memory-maintenance.md references/memory-maintenance.en.md \
       references/project-notes.md references/project-notes.en.md; do
       mkdir -p "$DEST/$(dirname "$f")"
       curl -fsSL "$BASE/$f" -o "$DEST/$f" || echo "FAILED: $f"
     done
     # 清单在仓库根，不在 skills 目录内——单独拉，否则无 Python 时无法核对
     curl -fsSL "https://raw.githubusercontent.com/shenghua520/work-discipline/main/manifest.json" \
       -o "$DEST/manifest.json" || echo "FAILED: manifest.json"
     # 语义自检脚本（可选：装了 Python 才用得上；不拉也能靠 manifest 做哈希自证）
     curl -fsSL "https://raw.githubusercontent.com/shenghua520/work-discipline/main/scripts/verify_skill.py" \
       -o "$DEST/verify_skill.py" || echo "FAILED: verify_skill.py"
     ```
     <!-- END GENERATED:bash-download -->

   - **逐文件 raw 下载（PowerShell）**：

     <!-- SLOT:ps-download -->
     <!-- BEGIN GENERATED:ps-download -->
     ```powershell
     $base = "https://raw.githubusercontent.com/shenghua520/work-discipline/main/skills/work-discipline"
     $dest = "$env:USERPROFILE\.workbuddy\skills\work-discipline"  # 按客户端调整
     $files = @("SKILL.md","SKILL.en.md",
       "references/execution-layer.md",
       "references/execution-layer.en.md",
       "references/delegation-layer.md",
       "references/delegation-layer.en.md",
       "references/memory-maintenance.md",
       "references/memory-maintenance.en.md",
       "references/project-notes.md",
       "references/project-notes.en.md"
     )
     foreach ($f in $files) {
       $out = Join-Path $dest ($f -replace '/', '\')
       New-Item -ItemType Directory -Force -Path (Split-Path $out) | Out-Null
       Invoke-WebRequest -Uri "$base/$f" -OutFile $out
     }
     # 清单在仓库根，不在 skills 目录内——单独拉
     Invoke-WebRequest -Uri "https://raw.githubusercontent.com/shenghua520/work-discipline/main/manifest.json" -OutFile (Join-Path $dest "manifest.json")
     # 语义自检脚本（可选）
     Invoke-WebRequest -Uri "https://raw.githubusercontent.com/shenghua520/work-discipline/main/scripts/verify_skill.py" -OutFile (Join-Path $dest "verify_skill.py")
     ```
     <!-- END GENERATED:ps-download -->

   拉完用 `manifest.json` 核对 SHA256（见下），别只看文件在不在。

   - **没有 Python / 没拉脚本**：直接哈希自证（`sha256sum` / `Get-FileHash`），这就是"完全离线"的验法。
   - **装了 Python 且拉了脚本**：语义自检。安装副本必须**显式指定清单**，否则脚本拒绝把仓库自带清单当成对你的安装副本的校验结果：

     ```bash
     python "$DEST/verify_skill.py" "$DEST" --manifest "$DEST/manifest.json"
     ```

5. **换客户端**：不同软件的 skill 目录、常驻指令落点、按需读能力都不一样。装之前先看 `docs/clients.md`（中）/ `docs/clients.en.md`（英）的映射表——表里每条都标了证据等级（本机实测 / 外部实测 / 未实测）。**只能读单文件的客户端请改用 `dist/` 扁平版，不要装目录版。**

## 仓库结构

<!-- SLOT:repo-tree -->
<!-- BEGIN GENERATED:repo-tree -->
```text
.
├── .github/workflows/verify.yml     # CI：双 job（有/无 PyYAML）× 双平台
├── LICENSE                          # MIT
├── README.md                        # 本说明（中文）
├── README.en.md                     # 本说明（英文）
├── docs/
│   ├── clients.md                   # 客户端适配表（中文，标证据等级）
│   └── clients.en.md                # 客户端适配表（英文）
├── dist/
│   ├── work-discipline.flat.md      # 扁平版（无 references，给单文件客户端）
│   └── work-discipline.flat.en.md
├── manifest.json                    # 全文件 SHA256 + 字节数（无 Python 也能验）
├── scripts/
│   ├── verify_skill.py              # 语义自检：frontmatter + 中英对齐 + 路由
│   └── build_dist.py                # 生成/校验扁平版与 manifest
└── skills/
    └── work-discipline/
        ├── SKILL.md                 # 规则主文件 · 中文 · 唯一入口
        ├── SKILL.en.md              # 规则主文件 · 英文
        └── references/
            ├── execution-layer.md      # 执行层七步法 + 三条铁律
            ├── execution-layer.en.md      # 执行层七步法 + 三条铁律
            ├── delegation-layer.md     # 委托层四时机
            ├── delegation-layer.en.md     # 委托层四时机
            ├── memory-maintenance.md   # 记忆维护规则
            ├── memory-maintenance.en.md   # 记忆维护规则
            ├── project-notes.md        # 特定后端的私有经验（换项目即作废）
            └── project-notes.en.md        # 特定后端的私有经验（换项目即作废）
```
<!-- END GENERATED:repo-tree -->

## 自检

```bash
python scripts/verify_skill.py              # 仓库内自检（目标在仓库布局内，自动用仓库清单）
python scripts/verify_skill.py <安装目录> --manifest <清单路径>   # 安装副本校验（必须显式给清单）
python scripts/build_dist.py --check        # 扁平版与 manifest 是否与源同步
```

`verify_skill.py` 检查 frontmatter 严格 YAML 解析、description 长度、中英结构指纹对齐（条目 / 标题 / 粗体 / 表格行 / 代码围栏 / 反引号）、路由双向闭合（既查指向的文件存在，也查本地文件都被索引）、无品牌字样、掩码规则未暴露前 4 位，并打印全部文件的 md5。`build_dist.py --check` 检查 `dist/` 扁平版和 `manifest.json` 是否与源文件一致——防止改了规则忘记重新生成分发产物。两者都不联网、不写文件。

**退出码语义**：`0` = 全部通过（fully verified）；`1` = 有 FAIL；`2` = 有 PARTIAL（如缺 PyYAML，语法未被验证）——**PARTIAL 不再伪报「全部通过」**。

**CI 覆盖两条分支**：`verify-full`（ubuntu + windows，装 PyYAML，断言 `exit=0`）+ `verify-no-deps`（`python -S` 无依赖，断言 `exit=2` 且输出含 `PARTIAL`）。之前 CI 只装了 PyYAML，导致 PARTIAL 这条分支永远测不到——现在它被单独断言。

**没有 Python 时的自证**：`manifest.json` 列了每个文件的 SHA256 与字节数，任何语言都能核对（`sha256sum` / PowerShell `Get-FileHash`）。Python 从「必需」降为「可选增强」。

## 设计取舍：为什么拆成 references

| 做法 | 常驻 token | 缺文件后果 | 本仓库选择 |
| --- | --- | --- | --- |
| 单文件全塞 | ≈3400 | 无 | ✗ 细则最容易被略读 |
| 拆 references | ≈1600（主文件） | 静默失效，已加防呆条款 | ✓ |
| 拆成三个独立 skill | 每次开工可能全加载 | 各装各的，易漏装 | ✗ 与「一个 skill 一个工作流」的初衷相悖 |

选拆 references 的原因：低频细则（委托层占全文 25%，且高度个人化）不该每次开工都进上下文；同时用「读不到就停下报错」的硬条款，把「缺文件 = 静默失效」这个风险变成可见错误。

## 优点

- **把隐性偏好变显式规则**：口头习惯写成可验证的动作，减少「凭印象」导致的漏做。
- **两层咬合**：执行层管「做对」、委托层管「交对」，每条规定都标出与另一层的对应关系，不打架。
- **按需加载**：常驻只留高频硬规则 + 路由索引，低频细则命中才读。
- **经过实测**：用「盲测是否输出动作」+「真实任务后独立路径回读」两招验证过，不是拍脑袋写的。

## 缺点 / 局限

- **启用 ≠ 每次调用**：skill 按需加载靠 AI 自己判断，实测出现过「已经读规则所以跳过调用」——行为合规但触发机制没跑。常驻钩子能把概率拉高，但不是硬保证。
- **提示词层，不是硬拦截**：要做到「绝不可能漏」得用 Hook / 脚本硬拦，而桌面端未必支持该机制。
- **拆分的代价**：安装必须整目录拷贝，只拷单个文件会静默失效。已经用「读不到就报错」的条款兜底，但本质上提高了安装门槛。
- **规则会稀释**：文件越长越容易被略读；反复写「禁止 X」反而让 X 更活跃，需要定期精简。
- **观点类任务不适用**：写作即思考，这类内容仍需人自己写，skill 只做找 / 整理 / 核实。

## 已知环境约束

以下是特定机器 / 仓库的状态，**不是规则**，所以不进 `SKILL.md` 正文：

- GitHub MCP 的写接口返回 `403 Resource not accessible by integration`（OAuth scope 缺 `repo`），读接口正常——该仓库的写操作走 `git push`。
- 本机 git 全局身份是占位符（`Your Name` / `your.email@example.com`），提交前必须按仓库设 `git config user.name` / `user.email`，否则提交无法归属。

## 变更记录

- **v11 落点归属 + 触发职责分离**：① 生成块清场重建的落点改为以 README 里手写的 `<!-- SLOT:key -->` 为唯一权威，不再采信孤儿标记出现在哪——修 v10 把块搬到错误章节（空壳章节）的 bug，孤儿标记在别处也照着 SLOT 归位；缺 SLOT 直接拒绝重建，不猜落点；重建块内容用生成器原文（`want`）逐字回填，不再叠加 SLOT 缩进——修自测发现的「whole 场景重建后块缩进翻倍、`--check` 永久失败」问题。② 公共 `description` 删去「任何开工场景均触发」，改为显式触发词 + 负边界（闲聊/单句问答/纯信息查询不触发）；「每次开工调用」归到宿主常驻指令职责——避免装了就强制每次开工加载、无法按场景关闭。CI 反向 job 补 SLOT 缺锚点自愈失败断言。
- **v10 自愈带删除语义**：修 v9 自愈的静默失败——只删一半标记（BEGIN/END 孤儿）时，旧逻辑追加新块、把残骸留原地，`--check` 重算 manifest 后反而给坏状态盖合法章。现在：① 每个 key 强制 `BEGIN 数 == END 数 == 1`，孤儿/重复直接 DIFF；② 修块改为「清场 → 原位置重建」——先删该 key 的所有标记与所有内容副本，不再 append 到文件末尾（落点从距安装章节 9789 字符回到节内）；③ 生成结束加幂等断言（渲染内容全篇只出现一次）；④ 报告改为按文件的清场重建列表，去掉恒空的 `[]`；⑤ VERSION 与 CHANGELOG 首条 vN 联动校验（v10 ↔ 10.0.0），常量只被自己校验的装饰问题再次收敛。CI 反向 job 补四类半标记自愈 + 落点断言。
- **v9 生成闭环**：修三条 v8 残留——① `generate` 缺块时曾打印「回填 4 个」实际只 3 个还报 PASS（写路径伪绿）；现在缺块按标记自动补插、如实报告，回填后再调一次块复检，仍有缺失则 exit 1。② `manifest.version` 收敛为 `build_dist.py` 的 `VERSION` 常量单一来源，`--check` 比对值（之前只查字段存在，篡改 9.9.9 仍 PASS）。③ 安装树与仓库结构树从分语言的 4 个 refs 改为列全 8 个（树描述目录，不是语言视图）——v7 修过、v8 生成时又退回半份的问题。CI 反向 job 补 version 篡改与 generate 自愈两组断言。
- **v8 文档 SSOT 生成**：把「分发文件清单」（10 个规则文件）收敛为 `build_dist.py` 里的 `RULE_FILES` 常量；README 的安装树、bash / PS 下载循环、仓库结构树全部改为脚本生成，用 `<!-- BEGIN/END GENERATED:x -->` 标记包裹，`--check` 只验生成块逐字同步——覆盖面从「猜哪些事实要验」变成「全部生成块」，v7 那三处盲区（manifest 行、脚本行、第二棵树）一起消失。CI 的 `verify-negative-docs` 改为对四个生成块 × 中英逐块注入垃圾，断言都能被抓到。`docs/clients.md` 的 token 估算标注为估算值、规则文件数标注由脚本核对。
- **v7 说明书一致性**：品牌检查去掉「目录名以 work-discipline 结尾」的过滤（安装目录一改名被检集合变空集、检查恒过——静默失效），改为以传入目录为根收集 md；README 安装树缩进修复（4 个文件曾掉回根层，照图拷会装错目录）；下载循环补拉 `scripts/verify_skill.py` 与 `manifest.json`，并把「自检命令」明确分成两条路（有 Python + 脚本跑语义自检；否则只做哈希自证）；`build_dist.py --check` 增加文档静态门禁——校验 README 安装树与实际 references 一致、下载循环覆盖全部规则文件（不联网、不执行 README 命令，避免 CI 依赖外部网络）；CI 加 `verify-negative-docs` job 覆盖树缩进错、下载清单漏、改名后品牌检查空转三类反向测试。
- **v6 校验闭环修复**：修复「装完后自检误报通过」——第 6 节原本用脚本所在仓库的清单校验仓库自己的文件，与传入的安装目录无关；现在目标在仓库布局内才自动用仓库清单，校验任意安装副本必须显式 `--manifest`，否则标记 PARTIAL（exit 2）拒绝伪绿；哈希比对基准从仓库路径改为被校验目录，只比对其中的 10 个规则文件。CI 加反向测试 job（故意污染一份安装副本断言失败）。README 安装树补齐 project-notes 两份、恢复循环补拉 `manifest.json`；术语统一为「客户端常驻指令」；未知客户端加三步判定流程；扁平版去掉重复分隔符。
- **v5 发行层改造**：加 `docs/clients.md` 客户端适配表（每条标本机实测 / 外部实测 / 未实测）；加 `dist/` 扁平版 + `manifest.json`（SHA256 无 Python 也能验），配 `scripts/build_dist.py` 生成与 `--check` 同步校验；CI 拆双 job（有/无 PyYAML）× 双平台，专门覆盖之前测不到的 PARTIAL 分支；安装说明补 zip 与逐文件 raw（bash + PowerShell）两条非 git 恢复路；「常驻钩子文件」硬引用改成「客户端常驻指令（落成独立文件时一并重读）」，扁平版文件头声明覆盖目录版专属条款，避免单文件客户端误触发「读不到 references 就报错」。
- **v4 复评修订**：主文件路由表补 `project-notes`（索引闭合）；自检脚本升级——缺 PyYAML 从 SKIP 改 PARTIAL 且退出码区分 `0/1/2`，中英对齐从"只比条目数"升级为结构指纹（当场抓出 project-notes 反引号 6 vs 8 的漂移），路由增加反向覆盖检查；加 `.github/workflows/verify.yml` CI 门禁；委托层注明单人单 agent 场景的适用边界，记忆维护注明与客户端偏好 / 记忆工具的双源边界。
- **v3 外部评审修订**：中英 description 改 `>-` 块标量（修复英文版严格 YAML 解析失败）；掩码从「前4+后4」收紧为仅后 4 位；API 重放条款加三条限定并禁止绕过受管网络策略；执行层的特定后端细节（`空 body POST` / `STATIC·VOLATILE` / `result:true+taskId`）移入 `references/project-notes.md`，规则层只留可迁移骨架；补 MIT LICENSE 与 `scripts/verify_skill.py` 自检脚本。
- **v2 结构重构**：主文件只留高频硬规则（≈55 行），执行层 / 委托层 / 记忆维护三章拆入 `references/`，路由索引改为真索引；新增「凭据不回显」「压缩或换实例后重读」两条规则；合并重复条目（任务清单与工作条目、扫技能与缺能力先问），消除自相矛盾；环境事实从规则正文移入本文件。
- **v1**：补 README → 改名 workbuddy-memory → work-discipline → 首次创建并上传 SKILL.md。
