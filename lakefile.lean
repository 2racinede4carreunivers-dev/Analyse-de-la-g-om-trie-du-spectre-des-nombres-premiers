import Lake
open Lake DSL

package «methode-spectrale» where
  -- Options du package
  leanOptions := #[
    ⟨`pp.unicode.fun, true⟩,
    ⟨`autoImplicit, false⟩
  ]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.14.0"

@[default_target]
lean_lib «MethodeSpectrale» where
  -- Bibliotheque principale : theories/MethodeSpectrale.lean
  srcDir := "theories"
  roots := #[`MethodeSpectrale]
