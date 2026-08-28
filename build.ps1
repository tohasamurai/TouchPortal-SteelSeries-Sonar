param(
    [string]$Version = "1.0.7"
)

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$python = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python312\python.exe'
$src = Join-Path $root 'src'
$stage = Join-Path $root 'dist_build\SteelSeriesSonar'
$build = Join-Path $root 'build'
$tpp = Join-Path $root "SteelSeriesSonar-v$Version.tpp"

if (-not (Test-Path $python)) {
    throw "Python 3.12 was not found: $python"
}

New-Item -ItemType Directory -Path $stage -Force | Out-Null
& $python (Join-Path $src 'gen_icon.py') (Join-Path $stage 'icon.png')
& $python (Join-Path $src 'gen_entry.py') (Join-Path $stage 'entry.tp')

Push-Location $src
try {
    & $python -m PyInstaller --onefile --noconsole --name SteelSeriesSonarPlugin `
        --paths $src --hidden-import defs --noconfirm `
        --distpath $stage --workpath $build --specpath $build (Join-Path $src 'plugin.py')
} finally {
    Pop-Location
}

$zip = [System.IO.Path]::ChangeExtension($tpp, '.zip')
Remove-Item -LiteralPath $zip -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $tpp -Force -ErrorAction SilentlyContinue
Compress-Archive -Path $stage -DestinationPath $zip -CompressionLevel Optimal
Move-Item -LiteralPath $zip -Destination $tpp
Write-Host "Built: $tpp"
