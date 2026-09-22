# BT0 — irc-skill structure validator (issue #1 P1)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$fail = 0

function Fail([string]$msg) {
    Write-Host "FAIL: $msg"
    $script:fail++
}

$skillPath = Join-Path $root '.grok\skills\irc-skill\SKILL.md'
if (-not (Test-Path -LiteralPath $skillPath)) {
    Fail "missing $skillPath"
} else {
    $skill = Get-Content -LiteralPath $skillPath -Raw
    if ($skill -notmatch '(?m)^name:\s*irc-skill\s*$') {
        Fail 'SKILL.md frontmatter must include name: irc-skill'
    }
    if ($skill -notmatch 'install') {
        Fail 'SKILL.md must describe install-as-skill'
    }
    if ($skill -notmatch '(?i)exe') {
        Fail 'SKILL.md must mention no exe-port install story'
    }
}

$installPy = Join-Path $root 'scripts\install_skill.py'
if (-not (Test-Path -LiteralPath $installPy)) {
    Fail "missing $installPy"
}

$spec = Join-Path $root 'docs\functional-spec.md'
$plan = Join-Path $root 'docs\build-and-test-plan.md'
if (-not (Test-Path -LiteralPath $spec)) { Fail "missing $spec" }
if (-not (Test-Path -LiteralPath $plan)) { Fail "missing $plan" }

$readme = Join-Path $root 'README.md'
if (-not (Test-Path -LiteralPath $readme)) {
    Fail "missing $readme"
} else {
    $readmeText = Get-Content -LiteralPath $readme -Raw
    if ($readmeText -notmatch 'functional-spec\.md') {
        Fail 'README must point at docs/functional-spec.md'
    }
    if ($readmeText -notmatch '(?i)install') {
        Fail 'README must document skill install'
    }
}

$forbidden = @(
    (Join-Path $root 'dist'),
    (Join-Path $root 'ports')
)
foreach ($dir in $forbidden) {
    if (Test-Path -LiteralPath $dir) {
        $exes = Get-ChildItem -LiteralPath $dir -Filter '*.exe' -Recurse -ErrorAction SilentlyContinue
        if ($exes) {
            Fail "forbidden exe kit under $dir"
        }
    }
}

foreach ($gp in @((Join-Path $root 'README.md'), $skillPath)) {
    if (-not (Test-Path -LiteralPath $gp)) { continue }
    $bad = Select-String -LiteralPath $gp -Pattern '(?i)(install|copy|run)\s+.*\b(dist[/\\]|ports[/\\])' -ErrorAction SilentlyContinue
    if ($bad) {
        Fail "$gp documents exe-port as install path"
    }
}

if ($fail -gt 0) {
    Write-Host "BT0: $fail check(s) failed"
    exit 1
}
Write-Host 'BT0: PASS'
exit 0
