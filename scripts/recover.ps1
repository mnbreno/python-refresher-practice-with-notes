param(
    [Parameter()]
    [ValidatePattern('^v\d+\.\d+\.\d+$')]
    [string]$Version = 'v1.2.4',

    [Parameter(Mandatory = $true)]
    [string]$Destination
)

$ErrorActionPreference = 'Stop'
$repository = 'https://github.com/mnbreno/python-refresher-practice-with-notes.git'
$fullDestination = [System.IO.Path]::GetFullPath($Destination)

if (Test-Path $fullDestination) {
    throw "Destination already exists; choose a new folder to avoid overwriting data: $fullDestination"
}

# Clone the immutable release tag rather than relying on the latest working tree.
git clone --branch $Version --single-branch $repository $fullDestination
if ($LASTEXITCODE -ne 0) {
    throw "Recovery clone failed for $Version"
}

Write-Host "Recovered $Version to $fullDestination"
Write-Host "Run the calculator with: python `"$fullDestination\calculator.py`""
