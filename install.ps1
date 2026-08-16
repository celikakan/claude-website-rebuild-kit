# Claude Website-Rebuild Kit - Windows One-Click-Installer
# DER KI BERATER - der-ki-berater.at
#
# Usage (PowerShell, one command):
#   irm https://raw.githubusercontent.com/celikakan/claude-website-rebuild-kit/main/install.ps1 | iex
#
# Thin wrapper: ensures Git Bash exists (installs Git via winget if needed),
# then runs the canonical install.sh through it. All install logic stays in
# install.sh so the two entry points can never drift apart.

$ErrorActionPreference = "Stop"

function Find-GitBash {
    $candidates = @(
        "$env:ProgramFiles\Git\bin\bash.exe",
        "${env:ProgramFiles(x86)}\Git\bin\bash.exe",
        "$env:LOCALAPPDATA\Programs\Git\bin\bash.exe"
    )
    foreach ($c in $candidates) {
        if ($c -and (Test-Path $c)) { return $c }
    }
    $cmd = Get-Command bash.exe -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    return $null
}

Write-Host ""
Write-Host "=============================================="
Write-Host "  Claude Website-Rebuild Kit (Windows)"
Write-Host "  DER KI BERATER"
Write-Host "=============================================="
Write-Host ""

$bash = Find-GitBash
if (-not $bash) {
    Write-Host "Git für Windows fehlt, wird jetzt über winget installiert..."
    winget install --id Git.Git -e --silent --accept-package-agreements --accept-source-agreements
    $bash = Find-GitBash
}
if (-not $bash) {
    Write-Host "Git Bash wurde nicht gefunden."
    Write-Host "Bitte Git von https://git-scm.com installieren und dieses Script erneut ausführen."
    exit 1
}

Write-Host "Starte die Installation über Git Bash..."
& $bash -lc "curl -fsSL https://raw.githubusercontent.com/celikakan/claude-website-rebuild-kit/main/install.sh | bash"
exit $LASTEXITCODE
