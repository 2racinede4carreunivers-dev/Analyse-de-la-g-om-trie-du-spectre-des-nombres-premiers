# GUIDE DE REDEMARRAGE - Gabriel v4.1 Corrige

Apres les corrections appliquees pour les deux problemes (logs Ollama + pytest), voici comment redemarrer votre agent Gabriel.

## Etape 1 : Arreter l'agent actuel

```bash
docker-compose down
```

Cela arrete tous les conteneurs (Gabriel, Ollama, Ollama-init).

## Etape 2 : Reconstruire l'image Docker

IMPORTANT : Les modifications au `docker-compose.yml` et `main_cli.py` doivent etre recompilees dans l'image.

```bash
docker-compose build --no-cache llm-agent-multiloop
```

Le flag `--no-cache` force la recompilation complete (necessaire pour les changements).

### Alternative : Reconstruction de tous les services

```bash
docker-compose build --no-cache
```

## Etape 3 : Relancer Gabriel

```bash
docker-compose up
```

Ou en mode detache :

```bash
docker-compose up -d
docker-compose logs -f llm-agent-multiloop-run
```

## Etape 4 : Verifier les corrections

### A) Interface CLI propre (sans logs Ollama)

Vous devez voir :

```
+============================================================+
|     MULTI-LOOP MATH AGENT  -  Philippe Thomas Savard       |
|       Methode Spectrale  *  Isabelle/HOL  *  Multi-Loop    |
+============================================================+

[... panels de banner ...]

╭─ Statut technique ───────────────────────────────────────╮
│ [OK] Container    : llm-agent-multiloop-run              │
│ [OK] Mode         : Multi-Loop (Ollama + Claude + OpenAI) │
│ ... (sans logs Ollama parasites) ...
╰───────────────────────────────────────────────────────────╯

  Verification de la suite de tests (pytest local)...
  Statut CI Gabriel : 161/161 OK (pytest local, 9.58s - tapez 'ci' pour le rapport detaille)
```

✓ CORRECT : Interface propre, pytest affiche un nombre reel de tests.

### B) Pytest fonctionne correctement

Une fois dans Gabriel, tapez :

```
Philippe > ci
```

Vous devez voir le rapport complet des tests (236 tests environ), PAS un message d'erreur.

### C) Si vous voyez encore les logs Ollama

Les logs Ollama peuvent apparaitre AVANT que Gabriel demarrage. C'est normal et prevu.
Cela vient du conteneur Ollama qui demarrage en parallele.

Mais l'interface CLI de Gabriel elle-meme doit etre PROPRE (sans logs rediriges).

Si vous voyez les logs dans le sortie du conteneur Gabriel, c'est un signe que le volume tests n'est pas monte correctement.

## Debogage

### A) Verifier le volume tests monte

```bash
docker-compose exec llm-agent-multiloop-run ls -la /home/agent/app/tests
```

Vous devez voir les fichiers `.py` de test.

### B) Verifier la variable d'environnement GABRIEL_TESTS_DIR

```bash
docker-compose exec llm-agent-multiloop-run env | grep GABRIEL_TESTS_DIR
```

Vous devez voir :
```
GABRIEL_TESTS_DIR=/home/agent/app/tests
```

### C) Voir les logs du conteneur (avec les logs Ollama rediriges)

Les logs Ollama sont maintenant dans les fichiers docker (`json-file` driver) :

```bash
docker logs ollama | tail -20
docker logs ollama-init | tail -20
```

### D) Tester pytest directement

Depuis le conteneur :

```bash
docker-compose exec llm-agent-multiloop-run python -m pytest tests/ -q --tb=no
```

Vous devez voir :
```
161 passed in 9.58s
```

Pas d'erreur.

## Fichiers cles modifies

Si vous voulez verifier les modifications :

1. **docker-compose.yml** - Configuration des logging drivers + montage tests + env var
2. **main_cli.py** - Ajout delai au demarrage + logging GABRIEL_TESTS_DIR
3. **src/ui/ci_status.py** - Amelioration detection repertoire tests

Voir le fichier `CORRECTIONS_v4.1.md` pour les details techniques complets.

## Questions frequemment posees

### Q1: Pourquoi il y a encore des logs au demarrage ?

R: C'est normal. Les logs peuvent apparaitre AVANT que Gabriel prenne le controle du terminal.
Mais l'interface CLI elle-meme doit etre propre apres le demarrage.

### Q2: Pytest affiche toujours 0/8 err ?

R: Verifiez que :
1. Le volume `./tests:/home/agent/app/tests:ro` est dans docker-compose.yml
2. La variable `GABRIEL_TESTS_DIR=/home/agent/app/tests` est set
3. Vous avez fait `docker-compose build --no-cache` (recompilation obligatoire)
4. Vous avez fait `docker-compose down` avant `up` (nettoyage)

### Q3: Comment voir les logs Ollama maintenant ?

R: Ils sont rediriges vers les fichiers Docker :

```bash
docker logs ollama
docker logs ollama-init
docker logs llm-agent-multiloop-run
```

Ces fichiers sont aussi visible via Docker Desktop sous l'onglet "Logs" de chaque conteneur.

## Rollback (si probleme)

Pour revenir a la version precedente (avant v4.1) :

```bash
git checkout HEAD -- docker-compose.yml main_cli.py src/ui/ci_status.py
docker-compose build --no-cache
docker-compose up
```

(Necessite que vous ayez commit les changements dans git, ou un backup de ces fichiers)

---

**Besoin d'aide ?**

Consultez le fichier `CORRECTIONS_v4.1.md` pour une analyse technique complete des deux problemes et leurs solutions.
