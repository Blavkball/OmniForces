Write-Host ""
Write-Host "====================================="
Write-Host "      Ollama Restore Assistant"
Write-Host "====================================="
Write-Host ""

$ModelRoot = "E:\Ollama\models"

if (!(Test-Path $ModelRoot)) {
    Write-Host "[ERROR] Model folder not found:"
    Write-Host $ModelRoot
    exit
}

[Environment]::SetEnvironmentVariable(
    "OLLAMA_MODELS",
    $ModelRoot,
    "User"
)

Write-Host "[OK] Environment variable restored."

Write-Host ""
Write-Host "Installed models:"
ollama list

Write-Host ""
Write-Host "Restore complete."
Write-Host ""
Write-Host "If Ollama is already running,"
Write-Host "restart it once before using the models."