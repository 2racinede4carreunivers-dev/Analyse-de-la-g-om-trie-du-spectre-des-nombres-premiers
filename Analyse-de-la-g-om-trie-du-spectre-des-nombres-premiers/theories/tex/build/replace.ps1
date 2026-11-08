$src = 'C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\theories\tex\build\Le-systeme-convolutif-Gabriel.pdf'
$target = 'C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\theories\tex\Le-systeme-convolutif-Gabriel.pdf'
$log = 'C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\theories\tex\build\replace.log'
for ($i = 0; $i -lt 900; $i++) {
  try {
    Copy-Item -LiteralPath $src -Destination $target -Force -ErrorAction Stop
    "OK $(Get-Date -Format o)" | Out-File -LiteralPath $log -Encoding utf8
    exit 0
  } catch {
    Start-Sleep -Seconds 2
  }
}
"TIMEOUT $(Get-Date -Format o)" | Out-File -LiteralPath $log -Encoding utf8
exit 1
