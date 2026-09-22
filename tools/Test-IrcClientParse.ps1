# No-network parse/dry-run check (P2 BT)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$client = Join-Path $root 'scripts\irc_client.py'
$fail = 0

function Fail([string]$msg) {
    Write-Host "FAIL: $msg"
    $script:fail++
}

$dry = & python $client --dry-run --host example.test --port 6697 2>&1
$dryText = ($dry | Out-String)
if ($LASTEXITCODE -ne 0) {
    Fail "dry-run exit code expected 0 got $LASTEXITCODE"
}
if ($dryText -notmatch 'example\.test:6697') {
    Fail "dry-run output missing target host:port"
}
if ($dryText -notmatch 'tls') {
    Fail "dry-run should show tls for port 6697"
}
if ($dryText -match '(?i)PASSWORD') {
    Fail "dry-run output must not contain PASSWORD"
}

$ErrorActionPreference = 'Continue'
python $client --dry-run 2>&1 | Out-Null
$ErrorActionPreference = 'Stop'
if ($LASTEXITCODE -ne 2) {
    Fail "missing host/port should exit 2 got $LASTEXITCODE"
}

if ($fail -gt 0) {
    Write-Host "Parse test: $fail check(s) failed"
    exit 1
}
Write-Host 'Parse test: PASS'
exit 0
