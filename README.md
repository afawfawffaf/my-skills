# my-skills

我的 AI 编程助手技能清单（DeepSeek Harness / Claude Code 通用）。
**本会话实际可调用 30 个 skill**，来源分三处；这里记录它们是什么、什么时候触发、从哪来、怎么装回来。

> `skills/` 目录**已收录 `~/.dsh/skills` 全部 21 个 skill 的完整正文**（含 `ppt-master` 的 12110 个文件）。
> 本机 skill 目录可以直接删，从本仓库 `git clone` 即可完整恢复。
> 仓库带 `.gitattributes`（`* -text`）关闭行尾转换，保证 `.sh` / `.js` / `.svg` 逐字节保真。

> 更新于 2026-10-26 · 主机 `E:\deepseek` · DSH 0.2.1

---

## 一、总表

### A. `~/.dsh/skills/` — 21 个（主力）

21 个里有 **17 个是指向 `E:\skill\skills\` 的符号链接**，实体只有 `architect`、`claude-vision`、`grill`、`lemo-opuscar` 四个目录。

#### ① superpowers 全家桶（14 个，第三方）

一套完整的软件开发方法论，从「先问清楚要做什么」到「收尾合并」。

| skill | 什么时候触发 | 内容 |
|---|---|---|
| `using-superpowers` | 会话开头 | 规定「先查 skill 再动手」，含 `references/` |
| `brainstorming` | 任何创造性工作前 | 先挖需求、意图、设计，再写代码（含 `scripts/`） |
| `writing-plans` | 有 spec、多步任务 | 先写实施计划，别急着碰代码 |
| `executing-plans` | 有现成计划 | 分阶段执行，带 review 检查点 |
| `subagent-driven-development` | 在当前会话跑计划 | 用子 agent 逐任务执行 |
| `dispatching-parallel-agents` | ≥2 个互不依赖的任务 | 并行分发，无共享状态才可用 |
| `test-driven-development` | 写任何功能/修 bug | 先写测试（真 red/green） |
| `systematic-debugging` | 遇到 bug、测试失败、行为异常 | 先定位再改（11 个文件，最厚） |
| `requesting-code-review` | 完成任务、合并前 | 发起评审，验证符合需求 |
| `receiving-code-review` | 收到评审意见 | 别盲从，先质疑再验证 |
| `verification-before-completion` | 要说「做完了」之前 | 必须跑命令验证，证据先于断言 |
| `using-git-worktrees` | 需要隔离工作区 | 建 worktree，不污染当前分支 |
| `finishing-a-development-branch` | 实现完成、测试通过 | 收尾：merge / PR / 清理 |
| `writing-skills` | 写/改/验证 skill 本身 | 含 `examples/` |

上游：[obra/superpowers](https://github.com/obra/superpowers)（MIT）

#### ② 单个方法论（1 个，第三方）

| skill | 什么时候触发 | 内容 |
|---|---|---|
| `karpathy-guidelines` | 写/审/重构代码时 | 防过度设计、做外科手术式改动、暴露假设、定义可验证的成功标准 |

上游：[multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)

#### ③ 中文 / 垂直场景（4 个，第三方）

| skill | 什么时候触发 | 内容 |
|---|---|---|
| `grill` | 「拷打我」「追问我」「帮我想清楚」「有什么没想到的」「grill me」「stress-test this」「poke holes in this」 | 分 5 档强度分轮追问，直到重要未知暴露；可选 decision log |
| `architect` | 「用什么技术做」「怎么部署」「which stack」「how to host」 | 需求清楚后比 2-3 套方案并推荐一套；先读 `docs/decisions-*.md` |
| `claude-vision` | 需要看图/OCR，但模型看不到或 `read_image` 失败 | 调外部 OpenAI 兼容 vision 接口转成文字描述 |
| `lemo-opuscar` | 「做个视频/短片/动画/宣传片」+ 指定风格 | 纯代码短片：油画厚涂、水彩、浮世绘、卫星简报、产品拆解、显微叙事 |

- `grill` / `architect` 上游：[nagi-studio/skills](https://github.com/nagi-studio/skills) 的 `skills/pondering/`（MIT，Nagi Studio）
- `claude-vision` 上游：[asuojun/claude-vision-skill](https://github.com/asuojun/claude-vision-skill)（本机版去掉了 `node_modules`，脚本仍在 `E:\skill\skills\claude-vision-skill\vision.js`）
- `lemo-opuscar` 上游：[lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) 的 `plugin/skills/lemo-opuscar/`（MIT，LemoLab）

#### ④ 重家伙（2 个）

| skill | 什么时候触发 | 内容 |
|---|---|---|
| `ppt-master` | 「做个 PPT」「生成PPT」「制作演示文稿」 | PDF/DOCX/URL/MD → SVG 页 → PPTX 全流水线。**41 KB SKILL.md + 26 个子目录**，75 MB / 1.2 万文件 |
| `latex-to-word-paper` | 写中文学术论文 | ctex 写 LaTeX → xelatex 出 PDF → python-docx 转 docx（图、表、脚注全带上） |

`ppt-master` 上游：[hugohe3/ppt-master](https://github.com/hugohe3/ppt-master)（MIT，Hugo He）。本仓库**全文收录** 12109 个文件 + 补入上游 `LICENSE`（解压时漏掉了）。
`latex-to-word-paper` 未找到公开上游，全文收录在 `skills/latex-to-word-paper/`。

### B. 插件自带 — 9 个

| skill | 用途 |
|---|---|
| `dsh-comfyui-workflows` | ComfyUI 出图/视频/音频的入口；也管工作流区分（图工作流 vs API 工作流）与音色库 |
| `diagnose-windows-sandbox-acl` | Windows 上 DSH 沙箱莫名拒绝访问时，一条命令查路径+所有祖先并修 ACL |
| `office` | Office 总入口，按需分流到下面 6 个 |
| `office-docx` | 创建/读取/编辑/校验 Word |
| `office-pptx` | 创建/读取/编辑/校验 PowerPoint |
| `office-xlsx` | 创建/读取/编辑/校验 Excel（含公式） |
| `office-export-pdf` | 用 LibreOffice Kit 转 PDF |
| `office-recalculate` | 刷新表格公式缓存并验证计算结果 |
| `office-render` | 渲染文档图片 / 检查视觉排版 |

### C. `~/.claude/skills/` — 12 个，**DSH 没扫这个目录**

这是 **Claude Code 的 skill 目录**（本机装了 `winget` 版 Claude Code），DSH 扫描的是 `~/.dsh/skills/`，两套目录互不相通 —— 所以这里的 skill **DSH 一个都调不到**。

其中 8 个与 `~/.dsh/skills` 重名，且内容**逐个 md5 完全一致**（属重复存放，不是两个版本）：brainstorming、executing-plans、karpathy-guidelines、requesting-code-review、systematic-debugging、test-driven-development、verification-before-completion、writing-plans。

真正只在 claude 那边、DSH 调不到的 4 个 —— **已收录在本仓库 `skills-claude/`**：

| skill | 触发名 | 用途 | 上游 | 许可 |
|---|---|---|---|---|
| `academic-skills-main` | `academic-research` | 学术研究全流程：读论文（带讲故事）、想方向、设计实验与 ablation/baseline、写数学证明与 LaTeX 定理、写论文到 camera-ready（NeurIPS/ICLR/ACL）、四步结构化审稿打分、导师匹配分析与 cold email | [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | MIT |
| `research-writing-skill-main` | `research-writing-assistant` | 论文/学位论文/文献综述写作：头脑风暴、分章写作、LaTeX 输出 | [Norman-bury/research-writing-skill](https://github.com/Norman-bury/research-writing-skill) | MIT（旬常） |
| `dotenv` | `dotenv` | Node.js 从 `.env` 加载环境变量；含加密 key、变量展开、命令替换等坑 | npm `dotenv` 作者 motdotla | BSD-2-Clause |
| `dotenvx` | `dotenvx` | dotenvx 多环境管理、变量展开、加密 `.env` 供 CI/CD 提交 | npm `dotenvx` 作者 motdotla | BSD-3-Clause |

> `academic-skills-main` / `research-writing-skill-main` 名字带 `-main`，是 GitHub 默认分支 zip 解压出来的（不是 git clone），所以没有 git 历史。

---

## 二、统计

```
~/.dsh/skills        21 个   其中 17 个是指向 E:\skill\skills\ 的符号链接
插件自带              9 个
~/.claude/skills     12 个   8 个与 dsh 重名（内容一致）+ 4 个 DSH 不可见
─────────────────────────────
DSH 实际可调用        30 个
```

本仓库收录：

| 目录 | 内容 | 文件数 | 体积 |
|---|---|---|---|
| `skills/` | `~/.dsh/skills` 全量 21 个 | 12167 | 75 MB |
| `skills-claude/` | `~/.claude/skills` 独有的 4 个 | 134 | 1.2 MB |

验证方式：从 GitHub 全新 `git clone` 下来，与两个源目录逐个文件 md5 比对 —— **0 缺失、0 内容不同**，唯一多出的是补入的 `ppt-master/LICENSE`。

## 三、装回来

本机两个 skill 目录删掉都能恢复：

```bash
git clone git@github.com:afawfawffaf/my-skills.git E:\my-skills

# 恢复到 DSH
cp -r E:\my-skills\skills\*         %USERPROFILE%\.dsh\skills\

# 恢复到 Claude Code（4 个独有件；另 8 个可从 skills\ 里一并拷）
cp -r E:\my-skills\skills-claude\*  %USERPROFILE%\.claude\skills\
```

> 方式 B：从各上游重新克隆（体积更小，但 claude-vision 的脚本路径要自己改）
```bash
git clone https://github.com/obra/superpowers.git              E:\skill\skills\superpowers-main
git clone https://github.com/nagi-studio/skills.git            E:\skill\skills\nagi-skills
git clone https://github.com/lemomo-ai/lemo-opuscar.git        E:\skill\skills\lemo-opuscar
git clone https://github.com/hugohe3/ppt-master.git            E:\skill\skills\ppt-master
git clone https://github.com/asuojun/claude-vision-skill.git   E:\skill\skills\claude-vision-skill
git clone https://github.com/multica-ai/andrej-karpathy-skills.git E:\skill\skills\andrej-karpathy-skills-main
```

> 方式 A 拷进去的是**实体目录**，不再是符号链接——所以 `E:\skill\skills` 那个下载暂存区可以放心删。

## 四、注意

- `E:\skill\skills\ppt-master-main.zip` 是 603 MB 的旧下载包，**已解压且与解压目录 12109 文件 md5 全一致**，可以删。但 zip 里另有未解压的 `examples/`(1250)、`docs/`(38)、`README`，删 zip 会丢这些（skill 本身不受影响）。
- `claude-vision/SKILL.md` 里写死了脚本路径 `E:\skill\skills\claude-vision-skill\vision.js`，换机器要同步改。
- `E:\skill\skills\` 这个下载暂存区一旦删掉，17 个符号链接会全部断掉。**用「方式 A」把本仓库的实体目录拷进 `~/.dsh/skills` 之后就可以删了。**
- `~/.claude/skills/` 里那 12 个：**4 个独有件已备份在本仓库 `skills-claude/`**，可以删；另 8 个与 `skills/` 内容一致，删了也能从本仓库恢复。

## License

- 本仓库自有部分（README、整理）：MIT
- 收录的第三方 skill 各自保留原许可：
  - superpowers 14 个 → MIT（obra/superpowers）
  - `karpathy-guidelines` → 见上游 multica-ai/andrej-karpathy-skills
  - `grill` / `architect` → MIT, Nagi Studio（见 `skills/grill/LICENSE`）
  - `lemo-opuscar` → MIT, LemoLab
  - `ppt-master` → MIT, Hugo He（见 `skills/ppt-master/LICENSE`）
  - `claude-vision` → 上游未标许可
  - `latex-to-word-paper` → 未找到公开上游
  - `academic-skills-main` → MIT（见 `skills-claude/academic-skills-main/LICENSE`）
  - `research-writing-skill-main` → MIT, 旬常（见 `skills-claude/research-writing-skill-main/LICENSE`）
  - `dotenv` → BSD-2-Clause, motdotla
  - `dotenvx` → BSD-3-Clause, motdotla
