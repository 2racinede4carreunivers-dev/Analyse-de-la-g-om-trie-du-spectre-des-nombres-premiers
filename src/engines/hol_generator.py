"""
hol_generator.py  —  Générateur de fragments Isabelle/HOL
══════════════════════════════════════════════════════════
CORRECTIONS appliquées (DEF-05) :
  • theory_name encode k, n, p correctement (ex: verif_p1097_n23_ratio4)
  • SA_def et SB_def référencent le modèle k (ex: SA_k4_def)
  • Invariant asymétrique généré si k != 2
  • Valeurs numériques issues du SpectralResult reçu, pas de constantes 1/2
══════════════════════════════════════════════════════════
"""

import logging
from dataclasses import dataclass

logger = logging.getLogger("gabriel.hol_generator")

DIGAMMA_EXP = 6   # 4^6 = 4096


@dataclass
class HOLFragment:
    theory_name: str
    body:        str

    def __str__(self) -> str:
        return self.body


class HOLGenerator:
    """
    Génère un fragment Isabelle/HOL validant la reconstruction de p.
    CORRECTION DEF-05 : tous les identifiants encodent k ; valeurs issues de SpectralResult.
    """

    def generate(
        self,
        k:       int,
        n:       int,
        p:       int,
        SA:      float,
        SB:      float,
        digamma: float,
    ) -> HOLFragment:
        # ── Noms encodant k (CORRECTION DEF-05) ──────────
        theory_name = f"verif_p{p}_n{n}_ratio{k}"
        SA_def      = f"SA_k{k}_def"
        SB_def      = f"SB_k{k}_def"
        dg_def      = f"digamma_k{k}_def"

        logger.info("Génération HOL : theory=%s", theory_name)

        # ── Invariant selon symétrie ──────────────────────
        if k == 2:
            inv = (
                "(* Invariant symétrique k=2 *)\n"
                f"lemma position_invariant:\n"
                f'  \"position {p} = {n}\"\n'
                "  by simp"
            )
        else:
            inv = (
                "(* Invariant ASYMÉTRIQUE k!=2 — CORRECTION DEF-05 *)\n"
                "(* n = nombre_de_termes  !=  position du premier reconstruit *)\n"
                "lemma invariant_ratio_asymetrique:\n"
                f'  \"n_termes = {n} \\\\<and> position_{p} \\\\<noteq> {n}\"\n'
                f"  by (simp add: position_{p}_eq_def)"
            )

        # ── Corps HOL assemblé par .format() ─────────────
        tmpl = (
            "theory {tn}\n"
            "  imports methode_spectral\n"
            "begin\n\n"
            "(* Fragment corrigé — ratio 1/{k} *)\n"
            "(*\n"
            "   FORMULES k={k} :\n"
            "   SA(n) = (241/192) * {k}^n - 4/3\n"
            "   SB(n) = (964/192) * {k}^n - 12292/3\n"
            "   digamma(n,p) = SB(n) - p * 4^{de}\n"
            "   Reconstruction : (SB(n) - digamma) / 4^{de} = p\n"
            "*)\n\n"
            "section \"Verification p={p} via modele 1/{k}\"\n\n"
            "(* CORRECTION DEF-05 : SA_def encode k={k}, pas 2 *)\n"
            "lemma SA_n_{n}_ratio_{k}:\n"
            "  \"SA_k{k} {n} = {sa}\"\n"
            "  unfolding {SAD} by norm_num\n\n"
            "lemma SB_n_{n}_ratio_{k}:\n"
            "  \"SB_k{k} {n} = {sb}\"\n"
            "  unfolding {SBD} by norm_num\n\n"
            "lemma digamma_n{n}_p{p}:\n"
            "  \"digamma_k{k} {n} {p} = SB_k{k} {n} - {p} * 4^{de}\"\n"
            "  unfolding {dgD} by simp\n\n"
            "lemma verif_premier_{p}_n_{n}:\n"
            "  \"(SB_k{k} {n} - digamma_k{k} {n} {p}) / 4^{de} = {p}\"\n"
            "  by (simp add: SB_n_{n}_ratio_{k} digamma_n{n}_p{p})\n"
            "{inv}\n\n"
            "end"
        )
        body = tmpl.format(
            tn=theory_name, k=k, n=n, p=p, de=DIGAMMA_EXP,
            sa=int(round(SA)), sb=int(round(SB)),
            SAD=SA_def, SBD=SB_def, dgD=dg_def,
            inv=inv,
        )
        return HOLFragment(theory_name=theory_name, body=body)


# ─────────────────────────────────────────────────────────
#  TESTS UNITAIRES
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Tests hol_generator ===")
    gen  = HOLGenerator()
    frag = gen.generate(k=4, n=23, p=1097, SA=88327434098004.0, SB=353309736387924.0, digamma=0.0)

    assert "ratio4"    in frag.theory_name
    assert "SA_k4_def" in frag.body
    assert "SB_k4_def" in frag.body
    assert "ASYMÉTRIQUE" in frag.body or "asymetrique" in frag.body.lower()
    assert "13631486"  not in frag.body   # valeur k=2 absente
    print(f"  OK  theory_name = {frag.theory_name!r}")
    print("  OK  SA_k4_def présent")
    print("  OK  SB_k4_def présent")
    print("  OK  invariant asymétrique présent")
    print("  OK  valeurs k=2 absentes")
    print("\nTous les tests hol_generator : OK")
    print("\n--- Fragment HOL ---")
    print(frag)
