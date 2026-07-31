$BackupRoot = "E:\Ollama\backups"
$ModelRoot = "E:\Ollama\models"

$Timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$RunFolder = Join-Path $BackupRoot $Timestamp

New-Item -ItemType Directory -Path $RunFolder -Force | Out-Null

Copy-Item "$ModelRoot\manifests" "$RunFolder\manifests" -Recurse -Force

ollama list | Out-File "$RunFolder\models.txt"
ollama --version | Out-File "$RunFolder\version.txt"

"OLLAMA_MODELS=$env:OLLAMA_MODELS" |
    Out-File "$RunFolder\environment.txt"

Write-Host ""
Write-Host "====================================="
Write-Host "Ollama backup completed successfully."
Write-Host "Backup: $RunFolder"
Write-Host "====================================="