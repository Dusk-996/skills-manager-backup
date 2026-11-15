[CmdletBinding()]
param(
    [Parameter(Position=0)][ValidateSet('accept','report')][string]$Action = 'accept',
    [string]$ProjectPath = (Get-Location).Path,
    [string]$OutputPath,
    [string]$PythonExecutable = 'python'
)
$ErrorActionPreference = 'Stop'
# 只执行同目录下的静态检查工具；不连接或修改任何生产资源。
$helper = Join-Path $PSScriptRoot 'devops_accept.py'
if (-not (Test-Path -LiteralPath $helper -PathType Leaf)) { throw "验收脚本不存在: $helper" }
$arguments = @('-X', 'utf8', $helper, $Action, '--project', $ProjectPath)
if ($OutputPath) { $arguments += @('--output', $OutputPath) }
& $PythonExecutable @arguments
exit $LASTEXITCODE
