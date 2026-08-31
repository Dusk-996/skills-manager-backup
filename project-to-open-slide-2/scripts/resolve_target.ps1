[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Target,
    [Parameter(Mandatory = $true)][ValidatePattern('^[a-z0-9][a-z0-9-]*$')][string]$Id
)

$ErrorActionPreference = "Stop"
$resolved = [System.IO.Path]::GetFullPath($Target)
if (-not (Test-Path -LiteralPath $resolved)) {
    New-Item -ItemType Directory -Path $resolved | Out-Null
}
if (-not (Test-Path -LiteralPath $resolved -PathType Container)) {
    throw "目标不是目录: $resolved"
}

$items = @(Get-ChildItem -LiteralPath $resolved -Force)
if ($items.Count -eq 0) {
    [pscustomobject]@{ target = $resolved; id = $Id; action = "initialize" } |
        ConvertTo-Json -Compress
    exit 0
}

$packagePath = Join-Path $resolved "package.json"
$slidesPath = Join-Path $resolved "slides"
$isOpenSlide = $false
if ((Test-Path -LiteralPath $packagePath) -and (Test-Path -LiteralPath $slidesPath -PathType Container)) {
    try {
        $package = Get-Content -LiteralPath $packagePath -Raw | ConvertFrom-Json
        $version = $package.dependencies.'@open-slide/core'
        $isOpenSlide = [bool]$version
    } catch {
        $isOpenSlide = $false
    }
}

if (-not $isOpenSlide) {
    $conflicts = $items | Select-Object -First 20 -ExpandProperty Name
    throw "目标目录非空且不是 Open Slide 项目，禁止覆盖。冲突文件: $($conflicts -join ', ')"
}
if ($version -ne "1.12.1") {
    throw "Open Slide 版本不匹配：当前 $version，要求固定为 1.12.1"
}

$deckPath = Join-Path $slidesPath $Id
if (Test-Path -LiteralPath $deckPath) {
    throw "演示 ID 已存在，禁止覆盖: $deckPath"
}

[pscustomobject]@{ target = $resolved; id = $Id; action = "reuse" } |
    ConvertTo-Json -Compress
