Write-Host ""
Write-Host "====================================="
Write-Host "      Ollama Installation Check"
Write-Host "====================================="
Write-Host ""

$ModelRoot = "E:\Ollama\models"

# Check model folder
if (Test-Path $ModelRoot) {
    Write-Host "[OK] Model folder found"
}
else {
    Write-Host "[ERROR] Model folder missing!"
    exit
}

# Check environment variable
$EnvPath = [Environment]::GetEnvironmentVariable("OLLAMA_MODELS","User")

if ($EnvPath -eq $ModelRoot) {
    Write-Host "[OK] OLLAMA_MODELS is configured"
}
else {
    Write-Host "[WARNING] OLLAMA_MODELS is set to:"
    Write-Host "    $EnvPath"
}

Write-Host ""

Write-Host "Installed Models"
Write-Host "----------------"

ollama list

Write-Host ""

$BlobCount = (Get-ChildItem "$ModelRoot\blobs" -File).Count
$ManifestCount = (Get-ChildItem "$ModelRoot\manifests" -Recurse -File).Count

Write-Host "Blob files      : $BlobCount"
Write-Host "Manifest files  : $ManifestCount"

Write-Host ""
Write-Host "Verification Complete."