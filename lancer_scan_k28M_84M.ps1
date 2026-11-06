<#
.SYNOPSIS
    Lancement parallele du scan convolutif 1/k — k = 28 000 000 → 84 000 000 (n=10)
.DESCRIPTION
    Utilise le pipeline cognitif Gabriel (pipeline_cognitif\generer_reconstruction_1k_tex.py)
    en parallelisant sur tous les cœurs logiques disponibles (Start-Process direct).

    Chaque job traite une sous-plage de k et genere :
      - Un fichier .tex  (rapport LaTeX par sous-plage)
      - Un fichier _detail.txt (rapports ancrés UNIQUE + AMBIGU seulement)

    Apres synchronisation, tous les _detail.txt sont concatenates en un seul
    fichier final : reconstruction_k28M_84M_detail.txt

    Aucune modification du pipeline source n'est requise.

.EXEMPLE
    .\lancer_scan_k28M_84M.ps1          # utilise tous les cœurs
    .\lancer_scan_k28M_84M.ps1 -Jobs 4  # limite a 4 jobs paralleaux
#>
param(
    [int]$Jobs   = $env:NUMBER_OF_PROCESSORS,
    [int]$KStart = 28000000,
    [int]$KEnd   = 84000000,
    [int]$N      = 10,
    [int]$Chunk  = 200000,
    [string]$OutDir = "reconstruction_k28M_84M_parts"
)

# --- Chemins ---
$ProjectRoot = "C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers"
$ScriptPath  = "$ProjectRoot\pipeline_cognitif\generer_reconstruction_1k_tex.py"
$TempDir     = "$ProjectRoot\$OutDir"
$FinalDetail = "$ProjectRoot\reconstruction_k28M_84M_detail.txt"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host (" SCAN CONVOLUTIF PARALLELE - k=" + $KStart + ".." + $KEnd + " (n=" + $N + ")") -ForegroundColor Cyan
Write-Host (" Pipeline : " + $ScriptPath) -ForegroundColor Cyan
Write-Host (" Jobs paralleux : " + $Jobs) -ForegroundColor Cyan
Write-Host (" Chunk interne   : " + $Chunk) -ForegroundColor Cyan
Write-Host (" Detail final   : " + $FinalDetail) -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

New-Item -ItemType Directory -Force -Path $TempDir | Out-Null

$TotalK = $KEnd - $KStart + 1
$PerJob = [Math]::Ceiling($TotalK / $Jobs)
Write-Host ("`n[" + $Jobs + " jobs x " + $PerJob + " k = " + $TotalK + " k totales]") -ForegroundColor Yellow

# --- Lancer les processus paralleux ---
$ProcessInfos = @()
for ($i = 0; $i -lt $Jobs; $i++) {
    $Debit = $KStart + ($i * $PerJob)
    $Fin = [Math]::Min($Debit + $PerJob - 1, $KEnd)
    if ($Debit -gt $KEnd) { break }

    $PartTex = "$TempDir\part_{0:D3}_{1}_{2}.tex" -f $i, $Debit, $Fin
    $PartDetail = "$TempDir\part_{0:D3}_{1}_{2}_detail.txt" -f $i, $Debit, $Fin

    $argList = @("--n", $N, "--k-debut", $Debit, "--k-fin", $Fin,
                  "--out", $PartTex, "--chunk", $Chunk,
                  "--detail", $PartDetail, "--ancres-seules")
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = "python"
    $psi.Arguments = "`"$ScriptPath`" " + ($argList -join " ")
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.CreateNoWindow = $true
    $p = [System.Diagnostics.Process]::Start($psi)

    $ProcessInfos += [PSCustomObject]@{
        Proc       = $p
        Index      = $i
        Debit      = $Debit
        Fin        = $Fin
        PartDetail = $PartDetail
    }
    $jobNum = $i + 1
    $nbK = $Fin - $Debit + 1
    Write-Host "  Job $jobNum / $Jobs : k=$Debit..$Fin ($nbK rapports)" -ForegroundColor Green
}

# --- Attendre la fin de tous les processus ---
Write-Host "`nAttente de la fin de tous les jobs..." -ForegroundColor Yellow
$AllOk = $true
foreach ($info in $ProcessInfos) {
    $info.Proc.WaitForExit() | Out-Null
    $stdout = $info.Proc.StandardOutput.ReadToEnd()
    $stderr = $info.Proc.StandardError.ReadToEnd()
    if ($info.Proc.ExitCode -ne 0) {
        Write-Host ("  ERREUR job " + $info.Index + " : " + $stderr.Substring(0, [Math]::Min($stderr.Length, 500))) -ForegroundColor Red
        $AllOk = $false
    } else {
        $lastLine = ($stdout -split "`n" | Where-Object { $_ -match "UNIQUE|AMBIGU|Total" })[-1]
        Write-Host ("  Job " + $info.Index + " OK : " + $lastLine) -ForegroundColor Green
    }
    $info.Proc.Dispose()
}

if (-not $AllOk) {
    Write-Host "`nERREURS detectees !" -ForegroundColor Red
    exit 1
}

# --- Concatenation des fichiers de detail ---
Write-Host "`nConcatenation des fichiers de detail..." -ForegroundColor Yellow
$First = $true
foreach ($info in $ProcessInfos) {
    $f = $info.PartDetail
    if (Test-Path $f) {
        if ($First) {
            Copy-Item -LiteralPath $f -Destination $FinalDetail -Force
            $First = $false
        } else {
            $content = Get-Content $f -ReadCount 10000
            $content | Select-Object -Skip 2 | Add-Content -Path $FinalDetail -Encoding UTF8
        }
        $lc = (Get-Item $f).Length
        $mb = [Math]::Round($lc / 1MB, 1)
        $fname = Split-Path $f -Leaf
        Write-Host "  Ajoute: $fname ($mb MB)" -ForegroundColor DarkGray
    }
}
$lineCount = (Get-Content $FinalDetail | Measure-Object -Line).Lines
Write-Host ("  Detail final : $lineCount lignes") -ForegroundColor Green

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host (" SCAN TERMINE - k=" + $KStart + ".." + $KEnd) -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host (" Fichier detail final : " + $FinalDetail) -ForegroundColor Cyan
Write-Host (" Fichiers .tex par parties : " + $TempDir + "\*.tex") -ForegroundColor Cyan
Write-Host "`nPour un rapport LaTeX combine, utilisez :" -ForegroundColor Yellow
Write-Host "  Get-Content $TempDir\part_*.tex | Out-File -Encoding UTF8 combined.tex" -ForegroundColor Yellow
Write-Host ("`nJobs lances : " + $Jobs + " | Plage : " + $KStart + ".." + $KEnd + " (" + $TotalK + " rapports)") -ForegroundColor Yellow