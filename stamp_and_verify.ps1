# Stamp and verify everything in canonical_with_pdf/
param(
  [string]$Dir = "canonical_with_pdf"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Push-Location $Dir
try {
  Write-Host "Stamping..."
  ots stamp *.canonical.md *.pdf

  Write-Host "Verifying timestamps..."
  Get-ChildItem *.ots | ForEach-Object { ots verify $_.Name }

  Write-Host "Verifying signatures..."
  Get-ChildItem *.asc | ForEach-Object {
    $sig = $_.Name
    $target = $_.BaseName -replace '\.asc$',''
    if (Test-Path $target) {
      gpg --verify $sig $target | Out-Host
    } else {
      Write-Warning "Missing artifact for signature: $sig"
    }
  }
} finally {
  Pop-Location
}
