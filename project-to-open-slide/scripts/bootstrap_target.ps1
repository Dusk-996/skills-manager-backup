[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$Target,
    [string]$TemplateHome,
    [switch]$InstallDependencies,
    [switch]$Offline,
    [switch]$SkipInstall
)
$ErrorActionPreference = 'Stop'
$skillRoot = Split-Path -Parent $PSScriptRoot
$config = Get-Content -LiteralPath (Join-Path $skillRoot 'config\template.json') -Raw | ConvertFrom-Json
# 路径优先级：明确参数、环境覆盖、随技能携带的相对模板。
if (-not $TemplateHome) { $TemplateHome = $env:OPEN_SLIDE_TEMPLATE_HOME }
if (-not $TemplateHome) {
    $TemplateHome = [string]$config.template_home
    if (-not [IO.Path]::IsPathRooted($TemplateHome)) { $TemplateHome = Join-Path $skillRoot $TemplateHome }
}
$template = [IO.Path]::GetFullPath($TemplateHome)
$targetPath = [IO.Path]::GetFullPath($Target)
if ($InstallDependencies -and $SkipInstall) { throw 'InstallDependencies 与 SkipInstall 不能同时使用' }
if (-not (Test-Path -LiteralPath $template -PathType Container)) { throw "模板不存在: $template" }
$package = Get-Content -LiteralPath (Join-Path $template 'package.json') -Raw | ConvertFrom-Json
if ($package.dependencies.'@open-slide/core' -ne $config.open_slide_version) { throw "模板版本不匹配，要求 $($config.open_slide_version)" }
foreach ($name in @('package.json','pnpm-lock.yaml','open-slide.config.ts','tsconfig.json')) {
    if (-not (Test-Path -LiteralPath (Join-Path $template $name) -PathType Leaf)) { throw "模板缺少 $name" }
}
if (-not (Test-Path -LiteralPath $targetPath)) { New-Item -ItemType Directory -Path $targetPath | Out-Null }
if (-not (Test-Path -LiteralPath $targetPath -PathType Container)) { throw "目标不是目录: $targetPath" }
if (@(Get-ChildItem -LiteralPath $targetPath -Force).Count -ne 0) { throw "初始化目标必须为空目录: $targetPath" }
foreach ($name in @('package.json','pnpm-lock.yaml','open-slide.config.ts','tsconfig.json','.npmrc')) {
    $source = Join-Path $template $name
    if (Test-Path -LiteralPath $source -PathType Leaf) { Copy-Item -LiteralPath $source -Destination (Join-Path $targetPath $name) }
}
New-Item -ItemType Directory -Path (Join-Path $targetPath 'slides') | Out-Null
$installed = $false
# 默认初始化不下载依赖；明确指定安装后才运行 pnpm，离线模式只使用本地缓存。
if ($InstallDependencies -and -not $SkipInstall) {
    $pnpm = Get-Command pnpm.cmd -ErrorAction SilentlyContinue
    if (-not $pnpm) { $pnpm = Get-Command pnpm -ErrorAction SilentlyContinue }
    if (-not $pnpm) { throw '未找到 pnpm；请先安装 package.json 声明的版本，或使用 SkipInstall 仅初始化' }
    Push-Location $targetPath
    try {
        $arguments = @('install','--frozen-lockfile')
        if ($Offline) { $arguments += '--offline' }
        & $pnpm.Source @arguments
        if ($LASTEXITCODE -ne 0) { throw 'pnpm install 失败；请检查国内源、代理或离线缓存' }
        $installed = $true
    } finally { Pop-Location }
}
[pscustomobject]@{ target=$targetPath; template=$template; version=$config.open_slide_version; installed=$installed } | ConvertTo-Json -Compress
