# 配置层级与检查

核对日期：2026-11-15。使用时读取当前安装版本，并查阅官方 [配置基础](https://learn.chatgpt.com/docs/config-file/config-basic) 和 [配置参考](https://learn.chatgpt.com/docs/config-file/config-reference)。

## 不能机械映射的层级

个人默认位于 `$CODEX_HOME/config.toml`，项目覆盖位于可信项目的 `.codex/config.toml`。调用参数、环境、配置 profile 和组织策略可能改变最终行为；按当前客户端的官方层级诊断，不仅查看一份文件。

当前项目配置不会覆盖机器级提供商、认证、通知、遥测或配置 profile 选择等设置。官方列出的个人层字段包括 `model_provider`、`model_providers`、`notify`、`profile`、`profiles`、`otel` 等；这不是永不过期的完整白名单。用户把这些键指定到项目层时先指出限制，不悄悄写入个人文件。

保留目标文件中不属于本次任务的未知字段。**保留未知字段不代表允许新增未知字段**：待改目标键必须另行核对支持性。已无法解析的原文件应先做局部诊断，不能借修复语法重置整份配置。

## 只读语法检查

有 Python 3.11+ 时，可用标准库检查 UTF-8 TOML；在可信脚本或正确转义的调用中传入路径，避免拼接执行用户字符串：

```python
from pathlib import Path
import tomllib

candidate = Path("candidate.config.toml")
data = tomllib.loads(candidate.read_text(encoding="utf-8-sig"))
print("TOML 语法通过")
```

这个检查只解析文件，不识别所有 Codex 字段、账号可用模型、受管理策略或最终加载值。不能把解析通过当成已生效。

如果本机 `codex --help` 确认提供 `--strict-config`，可配合已确认安全的诊断入口检查未知配置字段；先读该版本帮助，不假设不同版本都有这一选项。不要为了校验而启动真实业务任务，也不要把参数存在当成候选文件已通过校验。

## 隔离验证例

在临时目录中创建带注释的项目候选文件，已有 `[agents]` 表中把用户请求的并发限制从 4 调整为 2。保留其他表、注释和未知字段；保存原文，生成差异，重新解析并核对只有该目标值变化。

另测以下情况：重复键导致解析失败；用户要求项目层设置个人专用字段；用户要求未确认的界面字段；已有要求限制审批/权限。前两项报告具体原因，不自动改配置层；后两项不生成虚构键、不降低现有控制。

备份与候选文件可能含私密配置，不提交公共仓库，不在报告中打印令牌；只给脱敏差异和准确的恢复位置。
