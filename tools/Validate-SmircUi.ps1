# BT0 — SMIRC UI scaffold (#20)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$fail = 0

function Fail([string]$msg) {
    Write-Host "FAIL: $msg"
    $script:fail++
}

$layoutDoc = Join-Path $root 'docs\smirc-ui-layout.md'
if (-not (Test-Path -LiteralPath $layoutDoc)) {
    Fail "missing $layoutDoc"
}

$serve = Join-Path $root 'scripts\smirc_ui_serve.py'
if (-not (Test-Path -LiteralPath $serve)) {
    Fail "missing $serve"
} else {
    $py = Get-Command python -ErrorAction SilentlyContinue
    if (-not $py) { $py = Get-Command py -ErrorAction SilentlyContinue }
    if (-not $py) {
        Fail 'python not found; cannot run smirc_ui_serve.py --check-only'
    } else {
        $prevEap = $ErrorActionPreference
        $ErrorActionPreference = 'SilentlyContinue'
        & $py.Source $serve --check-only *> $null
        $checkCode = $LASTEXITCODE
        $ErrorActionPreference = $prevEap
        if ($checkCode -ne 0) {
            Fail 'smirc_ui_serve.py --check-only failed (exit ' + $checkCode + ')'
        }
    }
}

$index = Join-Path $root 'ui\smirc\index.html'
if (-not (Test-Path -LiteralPath $index)) {
    Fail "missing $index"
} else {
    $html = Get-Content -LiteralPath $index -Raw
    foreach ($hook in @(
            'smirc-channel-list',
            'smirc-chat-pane',
            'smirc-user-list',
            'smirc-chat-tabs',
            'smirc-image-drop'
        )) {
        if ($html -notmatch "data-testid=`"$hook`"") {
            Fail "index.html missing data-testid=$hook"
        }
    }
}

$readme = Join-Path $root 'README.md'
if (Test-Path -LiteralPath $readme) {
    $readmeText = Get-Content -LiteralPath $readme -Raw
    if ($readmeText -notmatch 'smirc_ui_serve') {
        Fail 'README must reference smirc_ui_serve.py (#20)'
    }
}

if ($fail -gt 0) {
    Write-Host "SMIRC BT0: $fail check(s) failed"
    exit 1
}
Write-Host 'SMIRC BT0: PASS'
exit 0
