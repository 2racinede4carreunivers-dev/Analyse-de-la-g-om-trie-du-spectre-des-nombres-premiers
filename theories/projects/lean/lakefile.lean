/- ============================================================
   Lakefile racine pour les slots Lean 4 pre-provisionnes.
   Univers au Carre / Methode Spectrale Savard.

   Compilation manuelle :
     cd theories/projects/lean
     lake update
     lake build

   NOTE : ce fichier n'est PAS reference par la CI GitHub
   Actions (workflow build.yml ne compile que Isabelle).
   Il sera activable le jour ou tu voudras relancer Lean 4.
   ============================================================ -/
import Lake
open Lake DSL

package «savard_slots» where
  -- add package configuration options here

-- require mathlib from git
--   "https://github.com/leanprover-community/mathlib4.git"

@[default_target]
lean_lib «Savard_Slots» where
  -- add library configuration options here
