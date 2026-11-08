$texPath = "Le-systeme-convolutif-Gabriel.tex"
$contentPath = "page28_content.txt"

# Read the LaTeX file
$lines = Get-Content $texPath -Encoding UTF8

# Find Page 28 start and Page 29 start
$startIdx = -1
$endIdx = -1
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -like "*Page 28*" -and $lines[$i] -like "*subsubsection*") {
        $startIdx = $i
    }
    if ($startIdx -ge 0 -and $lines[$i] -like "*Page 29*" -and $lines[$i] -like "*subsubsection*") {
        $endIdx = $i
        break
    }
}

Write-Host "startIdx=$startIdx endIdx=$endIdx"

# Read replacement content
$replacement = Get-Content $contentPath -Encoding UTF8

# Build new file
$newLines = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($i -lt $startIdx) {
        $newLines += $lines[$i]
    } elseif ($i -ge $startIdx -and $i -lt $endIdx) {
        if ($i -eq $startIdx) {
            $newLines += $replacement
        }
        # skip rest
    } else {
        $newLines += $lines[$i]
    }
}

Set-Content -Path $texPath -Value $newLines -Encoding UTF8
Write-Host "OK Page 28 finalisee"