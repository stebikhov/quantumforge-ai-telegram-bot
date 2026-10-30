param(
    [string]$Time = "06:00",
    [string]$TaskName = "RAG Index Update",
    [switch]$Remove
)

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$scriptPath = Join-Path $projectRoot "src\update_index.py"

if ($Remove) {
    schtasks /Delete /TN $TaskName /F
    Write-Host "Задача '$TaskName' удалена." -ForegroundColor Yellow
    exit 0
}

if (-not (Test-Path $venvPython)) {
    Write-Error "Не найден Python в $venvPython. Сначала создайте venv: python -m venv .venv"
    exit 1
}

if (-not (Test-Path $scriptPath)) {
    Write-Error "Не найден скрипт $scriptPath"
    exit 1
}

$existing = schtasks /Query /TN $TaskName 2>$null
if ($LASTEXITCODE -eq 0) {
    schtasks /Delete /TN $TaskName /F | Out-Null
    Write-Host "Существующая задача '$TaskName' удалена, будет создана заново." -ForegroundColor Yellow
}

$wrapperPath = Join-Path $projectRoot "scripts\run_update_task.cmd"
@"
@echo off
set PYTHONPATH=%~dp0src
"$venvPython" "$scriptPath"
"@ | Set-Content -Path $wrapperPath -Encoding ASCII

schtasks /Create `
    /TN $TaskName `
    /TR "`"$wrapperPath`"" `
    /SC DAILY `
    /ST $Time `
    /RL HIGHEST `
    /F | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "Задача '$TaskName' создана. Ежедневный запуск update_index.py в $Time." -ForegroundColor Green
    Write-Host "Проверить: schtasks /Query /TN $TaskName /V /FO LIST" -ForegroundColor Cyan
} else {
    Write-Error "Не удалось создать задачу (код $LASTEXITCODE). Запустите PowerShell от имени администратора."
}