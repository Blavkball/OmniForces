Write-Host ""
Write-Host "====================================="
Write-Host "      Ollama Model Updater"
Write-Host "====================================="
Write-Host ""

$Models = @(
    "llama3.2:latest",
    "qwen2.5-coder:7b",
    "deepseek-r1:7b",
    "deepseek-r1:1.5b"
)

foreach ($Model in $Models) {
    Write-Host ""
    Write-Host "Updating $Model ..."
    ollama pull $Model
}

Write-Host ""
Write-Host "====================================="
Write-Host "All models updated."
Write-Host "====================================="
Write-Host ""

ollama list