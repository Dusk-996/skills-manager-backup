# 服务不通，从主机、K8s 还是应用查起？

[返回场景目录](README.md) · 值班排障与观测

**已有材料**　主机日志、Pod 状态或可复现的异常

**结束产物**　有证据支持的定位、修复和验证路径

![服务不通，从主机、K8s 还是应用查起？](incident.svg)

[打开交互图](https://dusk-996.github.io/skills-manager-backup/atlas/incident.html) · [查看原尺寸 SVG](incident.svg)

## 技能怎么用

| 技能 | 何时使用 | 得到什么 |
|---|---|---|
| [ssh-remote-ops](../../ssh-remote-ops/SKILL.md) | 问题落在获授权的 Linux 主机上 | 核对进程、日志、网络和磁盘证据 |
| [k8s-troubleshoot](../../k8s-troubleshoot/SKILL.md) | 问题指向 Pod、Service 或 Ingress | 沿 Kubernetes 访问链定位故障层级 |
| [diagnosing-bugs](../../diagnosing-bugs/SKILL.md) | 有难复现或回归问题且能建立反馈循环 | 形成最小复现、根因和回归验证 |
| [systematic-debugging](../../external-skills/superpowers/skills/systematic-debugging/SKILL.md) | 需要按 Superpowers 流程调查根因时 | 得到假设、验证结果和修复证据 |

## 可以接着做

- [定位瓶颈后，怎么做成 Grafana 看板？](observability.md)　从「已确认的数据源、指标、标签与查询目标」开始。
