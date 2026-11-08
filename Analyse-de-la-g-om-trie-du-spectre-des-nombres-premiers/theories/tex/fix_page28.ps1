$path = "Le-systeme-convolutif-Gabriel.tex"
$lines = Get-Content $path -Encoding UTF8
$startIdx = 2106
$endIdx = 2138
$nouveauContenu = @"
\subsubsection*{Page 28}
\subsection*{Systeme convolutif Savard}

\subsection*{3.8. Synthese statistique (k=10 a 111)}

\vspace{0.3cm}

Ce tableau recapitule la repartition des 102 rapports $1/k$ etudies pour $n=10$ et $k \in [10,111]$, selon le resultat de la reconstruction du premier $P$.

\begin{center}
\small
\begin{tabular}{@{}l c c@{}}
\toprule
\rowcolor{spectralgris}
\textbf{Etat} & \textbf{Nombre de $k$} & \textbf{\%} \
\midrule
P certifie unique & 38 & 37\% \\
C_MULTIPLE (>= 2 premiers) & 20 & 20\% \\
AUCUN P (regle standard) & 44 & 43\% \\
\bottomrule
\end{tabular}
\end{center}

\vspace{0.3cm}

\subsection*{3.9. Notes importantes pour la programmation de l agent}

\begin{boitealerte}[Cas AUCUN P (44 valeurs)]
Les 4 candidats standards sont tous composites. Deux strategies possibles selon votre HOL :
\begin{itemize}[nosep]
  \item Regle speciale cataloguee (comme $k=27$ : Digamma $= \SA - (2k^{8}-k^{6})$, $P = 14\,330\,707$) ;
  \item Mode creation d ancrage : l agent retourne C_NON_CERTIFIE et attend validation HOL externe.
\end{itemize}
\end{boitealerte}

\vspace{0.3cm}

\begin{boitenote}[Cas C_MULTIPLE (20 valeurs)]
Selon le contrat HOL : retourner tous les C/P possibles, aucune selection silencieuse. L agent doit les lister tous et attendre confirmation.
\end{boitenote}

\vspace{0.3cm}

\begin{boitealerte}[Cas particulier $k=11$}
$k=11$ est un cas forme speciale : $P = 1\,611\,851$ (rang 121 982) avec regle A7- documentee dans le PDF -- non reconstruit par les 4 essais standards a $n=10$.
\end{boitealerte}

\vspace{0.3cm}

\begin{boitealerte}[Arithmetique exacte requise]
Pour $k \ge 50$, les valeurs de $\SA$ et $\SB$ depassent $10^{15}$ -- l agent doit utiliser l arithmetique entiere Python (pas float) pour eviter les erreurs d arrondi Excel.
\end{boitealerte}
"@
$newLines = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($i -eq $startIdx) {
        $newLines += $nouveauContenu -split "`n"
    } elseif ($i -ge $startIdx -and $i -lt $endIdx) {
        # skip
    } else {
        $newLines += $lines[$i]
    }
}
Set-Content -Path $path -Value $newLines -Encoding UTF8
Write-Host "OK Page 28 remplacee"