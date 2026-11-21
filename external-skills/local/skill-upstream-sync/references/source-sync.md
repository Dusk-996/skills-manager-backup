# 已发布技能的源码比对

## 建立可信基线

分别记录技能发现入口、实际路径、所有者、官方仓库 URL、仓库内路径、跟踪策略和不可变的新旧提交。安装清单可能只记了用户的备份仓库。比如 `find-skills` 的一个官方候选可以从 Vercel 的项目定位到具体技能文件，仍须把本机正文和配套文件与该路径的历史比对。[发布者仓库](https://github.com/vercel-labs/skills) · [技能文件](https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md)

- **已知旧版**：同一发布者和子目录的安装回执、锁文件中的提交、已核实仓库的 HEAD、上次成功同步记录均可提供起点；确认该对象可读取，且当前发布策略允许由旧版前进到目标。分支改写、版本倒退或标签被重指向时单列异常。
- **首次接管备份或散装副本**：先比较已核实的当前官方树。若全树一致，可建立基线。若不同，可按安装时的版本、发行标签、原始技能特征或 Git 历史追溯，导出候选旧树核实。单个相同文件、备份库 HEAD、目录 mtime 不能替整棵树建立旧基线。已知是本地派生但找不到基线的，仍可按产品文档核对孤立用法，不以当前本地内容冒充官方旧版。
- **版本策略**：跟踪分支用刚抓取的远端 ref，检查 `git merge-base --is-ancestor OLD NEW` 的退出码；镜像只能传输已独立确认的对象。detached HEAD 先核查安装说明、tag 和锁定策略。项目明确使用 latest stable 时选官方稳定发行；显式固定版本时报告可选新版。

## 预览与应用

仓库仅需抓取 Git 对象。可在临时目录用 `git clone --bare <已核实的官方 URL> <临时仓库>`，已有可信本地对象库可复用。不要在安装目录运行远程安装器。以下命令从本技能目录运行，变量替换为这一项已核实的值。临时目录与备份应在所有技能发现根目录之外。备份仅本地保存。

```text
python -X utf8 scripts/git_snapshot.py --repo REPO --commit OLD_SHA --subpath SKILL_PATH --out OLD_TREE
python -X utf8 scripts/git_snapshot.py --repo REPO --commit NEW_SHA --subpath SKILL_PATH --out NEW_TREE
python -X utf8 scripts/tree_sync.py --local INSTALLED --base OLD_TREE --upstream NEW_TREE
```

按文件进行三方比对，覆盖 `SKILL.md`、脚本、引用及资源。保留只在本地更改的文件，新旧官方树中都没有的文件也是本地资产。同文件两边改成不同内容，整项暂停，其他技能继续。脚本使用原始字节；遇批量 CRLF/LF 或执行位差异，先查原安装器的转换规则，再用同一分发格式的正式新旧样本复核。先审阅改动文件并校验候选技能的元数据、引用和行为；能在临时副本做的验证先在那里完成。

预览结果看三个字段：`changes` 给出可应用的路径，`local_only` 给出将保留的本地定制，`local_matches_upstream` 才表示整棵文件树是否与目标一致。`unchanged` 表示没有待应用的上游差异，本地仍可能有定制。`conflict` 列出发生冲突的路径。

### 按安装所有者写入

- **独立目录或经核实的个人副本**：预览通过后，对同一组输入添加 `--apply --backup BACKUP` 执行。备份使用此前不存在的独立目录。验证后用相同旧树、新树再预览，确认已没有可应用的差异。需要恢复时运行下面的命令。恢复遇到后续编辑时保留备份并先核对差异。

  ```text
  python -X utf8 scripts/tree_sync.py --local INSTALLED --base OLD_TREE --upstream NEW_TREE --apply --backup BACKUP
  python -X utf8 scripts/tree_sync.py --restore BACKUP --local INSTALLED
  ```

  备份含受影响文件的原件和 `manifest.json`，保存到持久化目录；临时官方样本可以独立清理。若进程意外中断，检查实际技能目录旁独占锁中记录的主机、PID、备份路径。仅在确认该进程已退出后移除该次遗留锁，使用这份备份恢复并复验。

- **Skills Manager 直接跟踪已核实的官方源**：用本机受信任的 `skills-manager-cli[.exe]`，先查 `skills show ID --json`，确认实际目录、skill ID、源、subpath、ref 和所有部署目标。原生更新可能覆盖本地文件；仅在已核对本地等于旧版、真实内容有变化、目标提交已审阅且单项备份已校验时，运行 `skills check ID --force --json` 刷新状态，再 `skills update ID --json`。只读检查可直接查官方 Git ref。完成后重新读取记录，核对实际提交、中央目录整树及发现入口。若更新窗口内上游再次前移，按实际取得的提交重验；未通过前不要报成功。使用该版本的单项恢复入口；如只能恢复内容，先恢复已备份的单项文件，复核部署并明确记录管理器版本字段的实际状态。避免整库回滚。
- **Skills Manager 登记的是备份源或本地派生**：用追溯出的官方基线做三方预览。核实是个人可编辑的中央副本、部署入口均为指向同一目录的链接时，按独立目录方式同步中央单项，记录真实发布者和提交；管理器中原有备份源继续作为分发配置。若是复制分发，使用所有者支持的单项部署/保留定制流程，验证各指定入口。不要把外部作者提交写进管理器数据库，或因名称相同使用 `set-source --force`。
- **直接 Git 安装的整包**：在真实 checkout 查工作区、分支、跟踪远端、原 HEAD 和整个包的影响范围。安装确实以整个包为更新单位、跟踪分支且工作区干净时，先保留旧 HEAD 的本地恢复引用，再抓取并用 `git merge --ff-only <已审阅的目标提交>` 前进，复查原入口和所有受影响技能。若单项请求会改变额外组件，列出范围。恢复前核实 HEAD 及工作树仍是本次结果，用保存的旧提交恢复对应 checkout，保留之后的用户编辑。
- **宿主插件、内置组件或其他安装器**：从安装回执和本机帮助确认其升级和恢复粒度。仅在原生入口能精确维护请求的包时自动执行。保留插件版本缓存和系统技能的所有权。

## 回执与回滚

对缺少原生上游记录的个人副本，在个人状态目录（例如 `~/.local/state/skill-upstream-sync/`）按实际路径的哈希保存 JSON 回执，字段含 `real_path`、`publisher_url`、`subpath`、`channel`、`previous_commit`、`verified_commit`、`backup`。应用前暂存旧回执。单项备份生成后，将旧回执存为 `BACKUP/receipt.before.json`；此前没有回执时在该文件写 JSON `null`。首次完全匹配或更新验证完成后才原子替换当前回执。检查模式不写回执。

`tree_sync.py --restore` 恢复文件。给用户的回滚说明还应附上本项回执的实际路径：核对当前回执仍指向本次备份和提交，文件恢复验证通过后，以 `receipt.before.json` 原子恢复旧回执；其值为 `null` 则撤销本次首次建立的回执。已有更晚的回执时先复核版本链，保留后续修改。下次同步仍需验证真实目录、发布者和跟踪渠道。
