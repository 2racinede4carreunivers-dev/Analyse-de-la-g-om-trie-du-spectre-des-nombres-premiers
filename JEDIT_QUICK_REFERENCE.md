# Commandes Jed it + Gabriel - Référence Rapide

## Tes trois commandes (corrigées)

```bash
# 1. Lancer les services
docker-compose --profile isabelle up -d

# 2. Accéder au conteneur Gabriel (pour vérifier/débugger)
docker exec -it llm-agent-multiloop-run bash

# 3. Lancer Isabelle Jed it (interactive)
docker exec -it isabelle bash
# Puis à l'intérieur du conteneur:
isabelle jedit /theories/example.thy
```

---

## Différence: Mode Jed it GUI vs CLI

### Mode 1: Jed it GUI (Interactive) ← Ce que tu décris

```bash
docker exec -it isabelle bash
isabelle jedit /theories/file.thy
```

**Quand l'utiliser:**
- Vérification manuelle de théorèmes
- Édition interactive des preuves
- Debugging complexe

**Pré-requis Windows:**
- VcXsrv (X11 server)
- Configuration DISPLAY

---

### Mode 2: CLI Batch (Automatique) ← RECOMMANDÉ pour Windows

```bash
docker-compose --profile isabelle up -d
# C'est tout! Le script tourne en background
```

**Quand l'utiliser:**
- Gabriel vérifie automatiquement ses réponses
- www.universestaucarre.com accède via HTTP API
- Pas d'interaction manuelle nécessaire

**Avantages:**
- ✓ Fonctionne sur Windows
- ✓ Gabriel + Isabelle communiquent automatiquement
- ✓ Résultats stockés dans `/theories/generated/`

---

## Workflow complet: Gabriel → Jed it → Gabriel

### Étape 1: Gabriel pose une question

```bash
# Depuis www.universestaucarre.com
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Quel est le 26eme nombre premier?"}'
```

### Étape 2: Gabriel génère une théorie Isabelle

```python
# À l'intérieur de Gabriel
theory_content = """
theory Verify_P26
  imports Main
begin

theorem p_26_is_101: "nth_prime 26 = 101"
proof
  (* Vérification *)
  sorry
qed

end
"""
# Écrit dans: /theories/generated_1234567890.thy
```

### Étape 3: Isabelle vérifie (automatique)

```bash
# Mode CLI (automatique)
docker logs isabelle | grep "generated_1234567890.thy"
# Output: "✓ Succes: /theories/generated_1234567890.thy"

# OU Mode GUI (manuel si tu veux)
docker exec -it isabelle bash
isabelle jedit /theories/generated_1234567890.thy
# L'utilisateur peut voir la preuve et l'éditer
```

### Étape 4: Gabriel récupère le résultat

```python
# Gabriel lit:
result = {
    "theory_file": "/theories/generated_1234567890.thy",
    "valid": True,
    "output": "Verification complete"
}

# Gabriel affiche:
print("✓ Réponse vérifiée par Isabelle!")
```

### Étape 5: Retourner au site

```bash
# HTTP Response à www.universestaucarre.com
{
  "answer": "Le 26ème nombre premier est 101",
  "isabelle_verified": true,
  "theory_file": "/theories/generated_1234567890.thy"
}
```

---

## Commandes rapides pour chaque scenario

### Scenario 1: Tu veux juste lancer Gabriel

```bash
docker-compose up -d
curl http://localhost:8000/health
```

---

### Scenario 2: Tu veux Gabriel + Isabelle CLI (batch)

```bash
docker-compose --profile isabelle up -d
# Isabelle tourne en background, traite les fichiers automatiquement
curl http://localhost:8000/health
```

---

### Scenario 3: Tu veux accéder à Jed it interactif

**Option A: Avec VcXsrv (Windows)**

```bash
# 1. Installer VcXsrv
# https://sourceforge.net/projects/vcxsrv/

# 2. Lancer VcXsrv (avant docker)
# Windows: Menu Start → VcXsrv

# 3. Lancer Docker
docker-compose --profile isabelle up -d

# 4. Accéder à Jed it
docker exec -it isabelle bash
isabelle jedit /theories/example.thy
```

**Option B: Sans X11 - Utilise mode CLI**

```bash
# Fonctionne partout (recommandé)
docker-compose --profile isabelle up -d
# Pas de GUI, tout automatique
```

---

### Scenario 4: Tu veux parler à Gabriel directement

```bash
# Accéder au conteneur Gabriel
docker exec -it llm-agent-multiloop-run bash

# Lancer le CLI interactif
python3 main_cli.py

# Ou utiliser l'API HTTP
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Ta question ici"}'
```

---

## Logs et debugging

### Voir ce que Gabriel fait

```bash
docker logs llm-agent-multiloop-run -f
```

### Voir ce que Isabelle CLI traite

```bash
docker logs isabelle -f
```

### Voir les fichiers générés

```bash
# Depuis Windows
ls C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local\theories\generated\

# Depuis le conteneur Gabriel
docker exec llm-agent-multiloop-run ls -la /theories/generated/
```

### Vérifier le port 8000

```bash
# Gabriel écoute?
docker exec llm-agent-multiloop-run curl http://0.0.0.0:8000/health

# Depuis Windows
curl http://localhost:8000/health
```

---

## Résumé: Ce que Gabriel fait dans Jed it

**Gabriel ne "fait rien" dans Jed it. Voici ce qui se passe:**

1. **Gabriel génère** un fichier `.thy` (théorie Isabelle)
2. **Isabelle CLI** traite le fichier automatiquement (batch)
3. **Gabriel récupère** le résultat et l'utilise

**Alternativement:**

1. **Gabriel génère** un fichier `.thy`
2. **Tu ouvres manuellement** le fichier dans Jed it
3. **Tu le modifies/vérifies** interactif ement
4. **Gabriel récupère** le fichier modifié

**Avec www.universestaucarre.com:**

1. **www.universestaucarre.com** envoie une question à Gabriel (HTTP POST)
2. **Gabriel répond** via l'API HTTP
3. **Optionnel:** Gabriel vérifie sa réponse avec Isabelle
4. **www.universestaucarre.com** affiche la réponse (éventuellement vérifiée)

---

## Fichiers clés

| Fichier | Rôle |
|---------|------|
| `docker-compose.yml` | Définit les services (Gabriel, Ollama, Isabelle) |
| `src/adapters/gabriel_isabelle_bridge.py` | Bridge Gabriel ↔ Isabelle (génère + vérifie) |
| `scripts/isabelle-integration.sh` | CLI batch Isabelle (surveille /theories) |
| `src/api/gabriel_http_api.py` | Endpoints HTTP pour www.universestaucarre.com |
| `main_cli.py` | Lancement CLI + API simultanément |

---

## Checkliste: Tes 3 commandes

```bash
✓ 1. docker-compose --profile isabelle up -d
✓ 2. docker exec -it llm-agent-multiloop-run bash
✓ 3. isabelle jedit /theories/example.thy
   (Ou juste laisser le mode CLI batch tourner automatiquement)
```

C'est ça! 🎯

---

**Version:** 4.0  
**Last updated:** 2025-01-15  
**Status:** Ready for production
