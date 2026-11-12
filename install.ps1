# ==============================================================================
# Script d'installation automatique en 1 ligne pour GemmAI sous Windows
# Usage : irm https://.../install.ps1 | iex
# ==============================================================================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "    ██████╗ ███████╗███╗   ███╗███╗   ███╗ █████╗ ██╗" -ForegroundColor Cyan
Write-Host "   ██╔════╝ ██╔════╝████╗ ████║████╗ ████║██╔══██╗██║" -ForegroundColor Cyan
Write-Host "   ██║  ███╗█████╗  ██╔████╔██║██╔████╔██║███████║██║" -ForegroundColor Cyan
Write-Host "   ██║   ██║██╔══╝  ██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║" -ForegroundColor Cyan
Write-Host "   ╚██████╔╝███████╗██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║" -ForegroundColor Cyan
Write-Host "    ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "   Installateur Automatique GemmAI (Windows PowerShell)" -ForegroundColor Green
Write-Host "   Agent Developpeur Autonome - Local & Offline" -ForegroundColor Gray
Write-Host ""

# 1. Verification de Python
Write-Host "➜ Verification de Python..." -ForegroundColor Yellow
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python3 -ErrorAction SilentlyContinue
}

if (-not $python) {
    Write-Host "✖ Erreur : Python n'est pas installe ou pas dans le PATH." -ForegroundColor Red
    Write-Host "Installez Python depuis https://www.python.org/downloads/ ou via : winget install Python.Python.3.11" -ForegroundColor Yellow
    exit 1
}

Write-Host "  ✔ Python detecte." -ForegroundColor Green

# 2. Dossier d'installation
$installDir = Join-Path $env:USERPROFILE ".gemmai"
if (-not (Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir | Out-Null
}

$agentPath = Join-Path $installDir "agent.py"
$url = "https://raw.githubusercontent.com/Max-Adis/gemma-bot/main/agent.py"

Write-Host "➜ Telechargement de GemmAI dans $installDir..." -ForegroundColor Yellow
Invoke-RestMethod -Uri $url -OutFile $agentPath
Write-Host "  ✔ Fichier telecharge." -ForegroundColor Green

# 3. Creation du lanceur gemmai.cmd dans un dossier accessible du PATH
$binDir = Join-Path $env:LOCALAPPDATA "Microsoft\WindowsApps"
$launcherPath = Join-Path $binDir "gemmai.cmd"

$launcherContent = "@echo off`r`npython `"$agentPath`" %*"
Set-Content -Path $launcherPath -Value $launcherContent -Encoding ASCII

Write-Host "➜ Configuration de la commande globale 'gemmai'..." -ForegroundColor Yellow
Write-Host "  ✔ Lanceur configure dans $launcherPath" -ForegroundColor Green

# 4. Verification d'Ollama
Write-Host "➜ Verification d'Ollama..." -ForegroundColor Yellow
$ollama = Get-Command ollama -ErrorAction SilentlyContinue
if (-not $ollama) {
    Write-Host "  Ollama n'est pas detecte. Vous pouvez l'installer via :" -ForegroundColor Yellow
    Write-Host "  winget install Ollama.Ollama" -ForegroundColor Cyan
    Write-Host "  ou sur https://ollama.com/download/windows" -ForegroundColor Gray
} else {
    Write-Host "  ✔ Ollama est disponible." -ForegroundColor Green
    Write-Host "  Verification du modele 'gemma:2b'..." -ForegroundColor Gray
    try {
        & ollama pull gemma:2b
    } catch {
        Write-Host "  Note : Lancez 'ollama pull gemma:2b' des que le service Ollama est actif." -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
Write-Host "🎉 GemmAI a ete installe avec succes sous Windows !" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
Write-Host ""
Write-Host "Pour lancer l'agent, ouvrez un nouveau terminal et tapez :"
Write-Host "  gemmai" -ForegroundColor Cyan
Write-Host ""
