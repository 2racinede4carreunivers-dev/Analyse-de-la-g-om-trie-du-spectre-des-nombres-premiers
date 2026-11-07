# CHECKLIST DE VERIFICATION - Gabriel v4.1

Utilisez cette checklist pour verifier que les deux problemes sont bien resolus.

## ✓ Problem 1 : Logs Ollama a l'entete - RESOLU

### Verification immediate

Lancez Gabriel :
```bash
docker-compose down && docker-compose build --no-cache && docker-compose up
```

Observez l'affichage terminal :

- [ ] Pas de lignes `ollama | time=2026-09-05T07:02:58.132Z level=INFO ...`
- [ ] Pas de logs de type `msg="server config" env=...`
- [ ] L'interface CLI de Gabriel s'affiche PROPRE et lisible
- [ ] Les panels de banner s'affichent correctement

### Verification technique

Fichiers modifies :

- [ ] `docker-compose.yml` - Service `ollama` contient `logging: driver: json-file`
- [ ] `docker-compose.yml` - Service `ollama-init` contient `logging: driver: json-file`
- [ ] `docker-compose.yml` - Service `llm-agent-multiloop` contient `logging: driver: json-file`
- [ ] `docker-compose.yml` - Service `ollama` contient `environment: OLLAMA_DEBUG=false`
- [ ] `main_cli.py` - Contient `time.sleep(0.5)` avant le banner

### Verification des logs rediriges

```bash
docker logs ollama | tail -20
```

- [ ] Vous voyez les logs Ollama (rediriges, pas en terminal)
- [ ] Les logs sont dans les fichiers json-file de Docker

---

## ✓ Problem 2 : Pytest ne s'execute pas - RESOLU

### Verification immediate

Une fois Gabriel lance, tapez :

```
Philippe > ci
```

Observez le resultat :

- [ ] Vous voyez "161/161 OK" (ou nombre eleve de tests reussis)
- [ ] Pas de message "0/8 (0 fail, 8 err)"
- [ ] Pas de message d'erreur "Tests directory introuvable"
- [ ] Le rapport de tests s'affiche correctement

### Verification au demarrage

Regardez les logs de demarrage de Gabriel :

```bash
docker-compose logs llm-agent-multiloop-run | grep -i "pytest\|statut ci"
```

- [ ] Vous voyez "Statut CI Gabriel : X/X OK" (avec un nombre reel)
- [ ] Les tests s'affichent, pas des erreurs

### Verification technique

Fichiers modifies :

- [ ] `docker-compose.yml` - Service `llm-agent-multiloop` contient le volume `./tests:/home/agent/app/tests:ro`
- [ ] `docker-compose.yml` - Service `llm-agent-multiloop` contient `GABRIEL_TESTS_DIR=/home/agent/app/tests` dans `environment`
- [ ] `src/ui/ci_status.py` - Fonction `_find_tests_dir()` amelioree (avec logging)
- [ ] `main_cli.py` - Logging de verification de GABRIEL_TESTS_DIR au demarrage

### Verification du volume monte

```bash
docker-compose exec llm-agent-multiloop-run ls -la /home/agent/app/tests | head -10
```

- [ ] Vous voyez les fichiers `.py` de test
- [ ] Pas de message "No such file or directory"

### Verification de la variable d'environnement

```bash
docker-compose exec llm-agent-multiloop-run env | grep GABRIEL_TESTS_DIR
```

- [ ] Vous voyez `GABRIEL_TESTS_DIR=/home/agent/app/tests`

### Test pytest manuel

```bash
docker-compose exec llm-agent-multiloop-run python -m pytest tests/ -q --tb=no
```

- [ ] Vous voyez "161 passed in X.XXs"
- [ ] Pas de message "error" ou "ERROR"
- [ ] Exit code = 0 (succes)

---

## ✓ Integration globale

### Affichage global au demarrage

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

Ecran attendu :

```
+============================================================+
|     MULTI-LOOP MATH AGENT  -  Philippe Thomas Savard       |
|       Methode Spectrale  *  Isabelle/HOL  *  Multi-Loop    |
+============================================================+

[... banner panels ...]

╭─ Statut technique ───────────────────────────────────────╮
│ [OK] Container    : llm-agent-multiloop-run              │
│ [OK] Mode         : Multi-Loop (...)                     │
│ [OK] Validation   : Isabelle/HOL + Debugger + RAG        │
│ [OK] Capacite     : 1000 premiers indexes                │
╰───────────────────────────────────────────────────────────╯

╭─ Citation historique du jour ───────────────────────────╮
│ "Il existe une infinite de zeros sur la droite ..."     │
│ — Godfrey Harold Hardy (1914)                            │
╰─────────────────────────────────────────────────────────╯

  Verification de la suite de tests (pytest local)...
  Statut CI Gabriel : 161/161 OK (pytest local, 9.58s - tapez 'ci' pour le rapport detaille)
  Raccourcis clavier actifs (Tab=completion, Ctrl+R=recherche, Up/Down=historique).

╭──────────────────────────────────────────────────────────────────────────────────╮
│    Agent pret  -  Bonjour Philippe !                                             │
│    Tapez 'aide' pour le menu rapide, 'commandes' pour tout voir, 'quitter' pour │
│    Decouverte guidee : ask / ask type / ask rules                                │
╰──────────────────────────────────────────────────────────────────────────────────╯
```

- [ ] Interface PROPRE sans logs Ollama parasites
- [ ] Statut CI affiche un nombre reel de tests OK
- [ ] Pas de messages d'erreur au demarrage

### Fonctionnement dans Gabriel

```
Philippe > ask Quel est l'ecart spectral entre les positions 5 et 10 ?
```

- [ ] Gabriel repond normalement
- [ ] Pas de ralentissement ou d'erreur
- [ ] Les resultats s'affichent correctement

### Commandes de test dans Gabriel

```
Philippe > ci
```

- [ ] Affiche le rapport de 161 tests avec details

```
Philippe > prime 26
```

- [ ] Affiche "101" (le 26e nombre premier)

```
Philippe > gap 5 10
```

- [ ] Affiche l'ecart spectral entre positions 5 et 10

---

## ✓ Recapitulatif

| Aspect | Avant (Probleme) | Apres (v4.1) | Status |
|--------|------------------|--------------|--------|
| Logs Ollama au demarrage | Pollue le terminal | Rediriges vers fichiers JSON | ✓ |
| Interface CLI propre | Non | Oui | ✓ |
| Pytest au demarrage | 0/8 err | 161/161 OK | ✓ |
| Rapport pytest (cmd `ci`) | Echoue | Fonctionne | ✓ |
| Reconstruction image | Pas necessaire | Oui, `--no-cache` | ✓ |
| Montage du volume tests | Non | Oui, automatique | ✓ |
| Variable GABRIEL_TESTS_DIR | Non | Oui, auto-set | ✓ |

---

## ✓ Support et debogage

Si une verification ECHOUE, consultez :

1. **CORRECTIONS_v4.1.md** - Analyse technique complete
2. **REDEMARRAGE_v4.1.md** - Guide de redemarrage detaille
3. **Logs Docker** - `docker logs <service>`

En cas de probleme persistant :

```bash
# Nettoyage complet
docker-compose down -v
docker system prune -a

# Reconstruction entiere
docker-compose build --no-cache

# Redemarrage propre
docker-compose up
```

---

**Version :** v4.1 (2026-09-05)
**Statut :** Correction des 2 problemes apliquees et validees
