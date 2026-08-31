[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Target,
    [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"
$skillRoot = Split-Path -Parent $PSScriptRoot
$config = Get-Content -LiteralPath (Join-Path $skillRoot "config\template.json") -Raw |
    ConvertFrom-Json
$template = [System.IO.Path]::GetFullPath([string]$config.template_home)
$targetPath = [System.IO.Path]::GetFullPath($Target)

if (-not (Test-Path -LiteralPath $template -PathType Container)) {
    throw "固定模板不存在: $template"
}
$templatePackage = Get-Content -LiteralPath (Join-Path $template "package.json") -Raw |
    ConvertFrom-Json
if ($templatePackage.dependencies.'@open-slide/core' -ne $config.open_slide_version) {
    throw "模板版本不匹配，期望 $($config.open_slide_version)"
}

if (-not (Test-Path -LiteralPath $targetPath)) {
    New-Item -ItemType Directory -Path $targetPath | Out-Null
}
if (@(Get-ChildItem -LiteralPath $targetPath -Force).Count -ne 0) {
    throw "初始化目标必须为空目录: $targetPath"
}

foreach ($name in @("package.json", "pnpm-lock.yaml", "open-slide.config.ts", "tsconfig.json")) {
    Copy-Item -LiteralPath (Join-Path $template $name) -Destination (Join-Path $targetPath $name)
}
New-Item -ItemType Directory -Path (Join-Path $targetPath "slides") | Out-Null

$templateSkills = Join-Path $template ".agents\skills"
if (Test-Path -LiteralPath $templateSkills) {
    New-Item -ItemType Directory -Path (Join-Path $targetPath ".agents") | Out-Null
    Copy-Item -LiteralPath $templateSkills -Destination (Join-Path $targetPath ".agents\skills") -Recurse
}

if (-not $SkipInstall) {
    Push-Location $targetPath
    try {
        & corepack pnpm install --frozen-lockfile
        if ($LASTEXITCODE -ne 0) { throw "pnpm install 失败" }
    } finally {
        Pop-Location
    }
}

[pscustomobject]@{
    target = $targetPath
    version = $config.open_slide_version
    installed = -not $SkipInstall
} | ConvertTo-Json -Compress
