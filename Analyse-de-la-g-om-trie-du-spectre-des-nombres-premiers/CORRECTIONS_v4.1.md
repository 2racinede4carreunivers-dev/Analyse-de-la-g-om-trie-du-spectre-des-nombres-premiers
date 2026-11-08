# CORRECTIONS APPLIQUEES A GABRIEL v4.1

## PROBLEM 1 : Logs Ollama parasites a l'entete du terminal

### Cause identifiee
Les logs de demarrage Ollama s'affichaient sur stdout/stderr du conteneur Docker :
```
ollama | time=2026-09-05T07:02:58.132Z level=INFO source=routes.go:1933 msg="server config" ...
ollama | time=2026-09-05T07:02:58.132Z level=INFO source=routes.go:1935 msg="Ollama cloud disabled: false"
...
```
Cela polluait visuellement l'interface CLI a l'ouverture.

### Solutions appliquees

#### 1. Redirection des logs Docker Compose (PRINCIPALE FIX)
**Fichier modifie :** `docker-compose.yml` (v5.4)

- **Ollama service** : Ajout de configuration logging driver JSON-file pour rediriger les logs vers des fichiers au lieu de stdout
  ```yaml
  logging:
    driver: "json-file"
    options:
      max-size: "10m"
      max-file: "3"
  ```

- **Ollama-init service** : Configuration similaire
  ```yaml
  logging:
    driver: "json-file"
    options:
      max-size: "5m"
      max-file: "1"
  ```

- **llm-agent-multiloop service** : Ajout de la meme config pour coherence
  ```yaml
  logging:
    driver: "json-file"
    options:
      max-size: "50m"
      max-file: "5"
  ```

**Effet :** Les logs Ollama sont maintenant rediriges vers les fichiers journaux Docker, pas vers le terminal de l'agent.

#### 2. Ajout de delai au demarrage de Gabriel
**Fichier modifie :** `main_cli.py` (v4.1)

- Ajout d'une pause de 0.5 secondes avant l'affichage du banner
- Permet aux conteneurs Ollama de demarrer et de se stabiliser en arriere-plan
- Les logs Ollama apparaissent apres cette pause, donc APRES que Gabriel prenne le controle du terminal

```python
# Attendre un peu pour que les logs Ollama se stabilisent
time.sleep(0.5)
```

#### 3. Desactivation des logs Ollama verbeux
**Fichier modifie :** `docker-compose.yml` (service ollama)

- Environnement : `OLLAMA_DEBUG=false`
- Reduit la verbosity de Ollama au demarrage

### Resultat attendu
L'interface CLI de Gabriel s'affiche PROPRE sans logs Ollama parasites :
```
+============================================================+
|     MULTI-LOOP MATH AGENT  -  Philippe Thomas Savard       |
|       Methode Spectrale  *  Isabelle/HOL  *  Multi-Loop    |
+============================================================+

[... banner panels sans pollution ...]

Statut CI Gabriel : 161/161 OK (pytest local, 9.58s - tapez 'ci' pour le rapport detaille)
```

---

## PROBLEM 2 : Pytest ne s'execute pas (affichait "0/8 (0 fail, 8 err)")

### Cause identifiee
Le repertoire `tests/` n'etait pas trouve par pytest lors du demarrage de Gabriel :
- Le dossier `tests/` n'etait pas monte dans le conteneur
- Ou le chemin etait incorrect
- Resultat : pytest echouait silencieusement avec 8 erreurs (= 0 tests trouves)

### Solutions appliquees

#### 1. Montage du volume tests dans docker-compose
**Fichier modifie :** `docker-compose.yml` (service llm-agent-multiloop)

- Ajout du volume pour `tests/` avec option `:ro` (read-only)
  ```yaml
  - ./tests:/home/agent/app/tests:ro
  ```

- Ajout de la variable d'environnement GABRIEL_TESTS_DIR (pointant vers le chemin Docker)
  ```yaml
  environment:
    ...
    - GABRIEL_TESTS_DIR=/home/agent/app/tests
  ```

#### 2. Amelioration de la detection du repertoire tests
**Fichier modifie :** `src/ui/ci_status.py`

Ordre de priorite pour trouver le dossier tests/ :

1. Variable d'environnement `GABRIEL_TESTS_DIR` (set par docker-compose.yml v5.4)
2. Chemin relatif au repo local `<repo>/tests`
3. Depuis CWD `./tests`
4. Chemin Docker standard `/home/agent/app/tests`
5. Chemins alternatifs Docker (`/app/tests`, `/workspace/tests`)

**Code ameliore :**
```python
def _find_tests_dir() -> Path:
    # Priorite 1 : variable d'environnement explicite (set dans docker-compose.yml)
    env_dir = os.environ.get("GABRIEL_TESTS_DIR")
    if env_dir:
        p = Path(env_dir)
        if p.is_dir():
            return p
    
    # Priorite 2 : a cote du module (cas dev local)
    candidate = _REPO_ROOT / "tests"
    if candidate.is_dir():
        return candidate
    
    # ... autres chemins ...
```

#### 3. Logging des variables d'environnement
**Fichier modifie :** `main_cli.py` (v4.1)

Verification et logging de la variable GABRIEL_TESTS_DIR au demarrage :
```python
# Verifier que GABRIEL_TESTS_DIR est bien set (pour pytest au demarrage)
tests_dir = os.getenv("GABRIEL_TESTS_DIR")
if not tests_dir:
    logger.warning("GABRIEL_TESTS_DIR not set; pytest may fail at startup")
else:
    logger.info("GABRIEL_TESTS_DIR=%s", tests_dir)
```

#### 4. Messages d'erreur ameliores
**Fichier modifie :** `src/ui/ci_status.py`

Messages d'erreur clairs si `tests/` n'est pas trouve :
```
Tests directory introuvable: /home/agent/app/tests

Cause probable : Gabriel tourne dans Docker et le dossier 'tests/'
n'a pas ete monte/copie dans le conteneur. Solutions :

Solution 1 (RECOMMANDEE - appliquee dans docker-compose.yml v5.4) :
    Verifiez que le volume est present :
      - ./tests:/home/agent/app/tests:ro
    Et que GABRIEL_TESTS_DIR==/home/agent/app/tests est set.
...
```

### Resultat attendu
Pytest s'execute correctement au demarrage de Gabriel :
```
  Verification de la suite de tests (pytest local)...
  Statut CI Gabriel : 161/161 OK (pytest local, 9.58s - tapez 'ci' pour le rapport detaille)
```

Au lieu du message d'erreur precedent :
```
  Statut CI Gabriel : 0/8 (0 fail, 8 err) (pytest local, 9.58s - ...)
```

---

## Fichiers modifies

### v5.4 du docker-compose.yml
- Ajout de `logging` driver json-file pour tous les services
- Ajout de la variable d'environnement `GABRIEL_TESTS_DIR`
- Montage du volume `./tests:/home/agent/app/tests:ro`
- Configuration `OLLAMA_DEBUG=false` pour desactiver les logs verbeux

### v4.1 du main_cli.py
- Ajout de 0.5s de delai au demarrage (apres time.monotonic())
- Logging de la variable GABRIEL_TESTS_DIR

### Fichier `src/ui/ci_status.py`
- Amelioration de `_find_tests_dir()` avec ordre de priorite explique
- Messages d'erreur plus precis et guidants
- Documentation claire des cas de demarrage Docker/local

### Fichier `suppress_ollama_logs.py` (nouveau)
- Utilitaire optionnel pour suppression des logs Ollama
- Peut etre appele explicitement si besoin supplementaire

---

## Verification et test

### Pour verifier les corrections :

1. **Reconstruire l'image Docker :**
   ```bash
   docker-compose build --no-cache
   ```

2. **Lancer Gabriel :**
   ```bash
   docker-compose up -d
   docker-compose logs -f llm-agent-multiloop-run
   ```

3. **Observer :**
   - [✓] L'interface CLI doit demarrer PROPRE sans logs Ollama
   - [✓] Le statut CI doit afficher "X/X OK" avec un nombre reel de tests
   - [✓] Pas de message d'erreur "tests directory introuvable"

4. **Tester pytest manuellement depuis l'agent :**
   ```
   Philippe > ci
   ```
   Doit afficher le rapport complet des tests

### Notes supplementaires :

- Les logs Ollama sont toujours rediriges vers les fichiers Docker (visibles via `docker logs ollama`)
- Aucune perte de fonctionnalite : simplement redirection du bruit vers les fichiers journaux
- Compatible avec tous les modes (CLI seul, API seul, hybrid)
- Pas de changement sur l'API HTTP ou la logique applicative

---

## Changelog

**v4.1 - 2026-09-05**
- [FIX] Problem 1 : Redirection des logs Ollama parasites via docker-compose logging driver
- [FIX] Problem 2 : Montage du volume tests et detection GABRIEL_TESTS_DIR
- [IMPROVE] Messages d'erreur pytest plus clairs et guidants
- [IMPROVE] Logging de verification au demarrage de Gabriel
