$path = "c:/Analyse-de-la-geometrie-du-spectre-des-nombres-premiers/Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers/theories/tex/Le-systeme-convolution-Gabriel.tex"
$content = Get-Content $path
# page 29: lines 1-103 (0..102)
# page 30 content: lines 213-240 (212..239)
# page 31 content: lines 105-211 (104..210)
$new = $content[0..102] + $content[212..239] + $content[104..210]
Set-Content $path $new
Write-Host "Reorganized: $($new.Count) lines"