param([string]$Python = '')
$ErrorActionPreference = 'Stop'
$taskRoot = $PSScriptRoot
$buildRoot = Join-Path $taskRoot 'build'
New-Item -ItemType Directory -Path $buildRoot -Force | Out-Null
if ([string]::IsNullOrWhiteSpace($Python)) {
    $bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
    if (Test-Path -LiteralPath $bundledPython) { $Python = $bundledPython }
    else { $Python = 'python' }
}
Push-Location -LiteralPath $taskRoot
try {
    foreach ($texName in @('Revised_Manuscript_Clean', 'Revised_Manuscript_Marked')) {
        for ($pass = 1; $pass -le 3; $pass++) {
            & pdflatex '-interaction=nonstopmode' '-halt-on-error' '-file-line-error' "-output-directory=$buildRoot" "$texName.tex"
            if ($LASTEXITCODE -ne 0) { throw "pdfLaTeX failed: $texName, pass $pass" }
        }
    }
    for ($pass = 1; $pass -le 2; $pass++) {
        & xelatex '-interaction=nonstopmode' '-halt-on-error' '-file-line-error' "-output-directory=$buildRoot" 'Response_to_Reviewers_EN.tex'
        if ($LASTEXITCODE -ne 0) { throw "XeLaTeX failed: response, pass $pass" }
    }
    Copy-Item -LiteralPath (Join-Path $buildRoot 'Revised_Manuscript_Clean.pdf') -Destination (Join-Path $taskRoot 'Revised_Manuscript_Clean.pdf') -Force
    Copy-Item -LiteralPath (Join-Path $buildRoot 'Response_to_Reviewers_EN.pdf') -Destination (Join-Path $taskRoot 'Response_to_Reviewers_EN.pdf') -Force
    & $Python (Join-Path $taskRoot 'tools\add_reviewer_tags.py') (Join-Path $buildRoot 'Revised_Manuscript_Marked.pdf') (Join-Path $taskRoot 'Revised_Manuscript_Marked_Reviewers.pdf') (Join-Path $taskRoot 'Reviewer_Tag_Map.json')
    if ($LASTEXITCODE -ne 0) { throw 'Reviewer-tag generation failed. Python requires pypdf and reportlab; pdftotext must be on PATH.' }
}
finally { Pop-Location }
