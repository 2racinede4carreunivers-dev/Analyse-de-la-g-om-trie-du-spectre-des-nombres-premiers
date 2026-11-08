# Configurer les fournisseurs LLM de Gabriel

## Configuration locale

Le fichier utilise par Docker est `Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers/.env`.
Il est ignore par Git. Ne copiez jamais son contenu dans un ticket, un journal ou
une conversation.

La configuration par defaut est :

```dotenv
OLLAMA_HOST=http://host.docker.internal:11434
OLLAMA_MODEL=qwen2.5-coder:7b
OLLAMA_ONLY=false
GROQ_MODEL=llama-3.3-70b-versatile
COMPUTATIONAL_LLM_ENABLED=false
```

Le fichier `.env` local contient deja `GROQ_API_KEY`. Conservez cette cle dans
ce fichier uniquement. Le lanceur ne l'affiche pas et ne teste pas l'API Groq.

## Ordre de routage

Gabriel essaie les fournisseurs dans cet ordre :

1. **Ollama local** (`OLLAMA_HOST` et `OLLAMA_MODEL`).
2. **Groq** (`GROQ_API_KEY` et `GROQ_MODEL`) si Ollama est indisponible ou
   renvoie une reponse vide.
3. Claude puis OpenAI, s'ils sont configures.

`OLLAMA_ONLY=true` desactive les fournisseurs cloud. La valeur par defaut
`false` autorise Groq comme fallback.

Groq utilise l'API compatible OpenAI a `https://api.groq.com/openai/v1`.
Le modele est configurable dans `.env`; une erreur de modele ou d'API est
consignee sans exposer la cle.

## Demarrage sous Windows

Ollama doit etre lance sur Windows. Verifiez son etat et le modele depuis
PowerShell :

```powershell
ollama list
Invoke-RestMethod http://localhost:11434/api/tags
```

Le modele configure doit etre present localement. Le lanceur verifie Ollama
avant le demarrage; s'il est indisponible, il affiche un avertissement et
Gabriel peut utiliser Groq.

Les reponses spectrales locales peuvent etre longues : le delai Ollama est
configure a 360 secondes. Qwen 2.5 Coder 7B a necessite environ 281 secondes
pour une reponse avec le prompt d'ancrage complet lors du test local. Ollama
charge Qwen a la demande; il n'est pas necessaire de lancer une commande Qwen
interactive en parallele.

Depuis le dossier parent ou le dossier du projet :

```powershell
.\start-agent.ps1
```

Le lanceur utilise l'Ollama Windows via `host.docker.internal` et ne demarre
pas son propre conteneur Ollama ni ne telecharge un second modele.

## Pipeline computationnel

Le code de `pythonLLM_computationnel.py` et du repertoire `pythonLLM/` est
monte en lecture seule dans le conteneur pour preparer une integration future.
Il n'est pas appele par le routage, la CLI ou le pipeline principal de Gabriel;
aucune reponse n'est actuellement pretraitee par ce moteur. Le drapeau
`COMPUTATIONAL_LLM_ENABLED=false` documente explicitement cet etat.

## Verification sans divulguer les secrets

Dans Gabriel, utilisez `env-check` pour voir quel fichier de configuration
est charge. Ne copiez pas les valeurs des variables sensibles dans un rapport.
Les tests de routage utilisent des clients simules et ne font aucun appel
facturable a Groq.
