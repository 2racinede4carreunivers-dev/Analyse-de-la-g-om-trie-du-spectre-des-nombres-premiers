# Security Policy — Gabriel Multi-Loop

> 🇫🇷 Une version française de ce document est disponible : [`declaration_securite.md`](./declaration_securite.md)

**Project author:** Philippe Thomas Savard
**Repository:** `agent-multiloop-Gabriel-local`
**Last revision:** July 25, 2026
**Covered versions:** v3.35 → v3.38 and above

---

## 1. Scope of this policy

This document describes the responsible way to **report**, **triage**, and **disclose** any security vulnerability, software defect, or behavioural anomaly affecting:

- The agent's Python source code (`src/`, `scripts/`, `tests/`)
- The Isabelle/HOL theory files (`theories/methode_spectral*.thy` and its 7 translations)
- The Docker container (`Dockerfile`, `docker-compose.yml`, `start-agent.ps1`)
- Third-party integrations (Anthropic Claude, OpenAI, Emergent Universal Key, Ollama)
- Proof artefacts (signed JSON audit trails, generated PNGs, cognitive RAG)
- Public documentation (`README.md`, `docs/`, GitHub Pages)

---

## 2. Supported versions

| Version | Security support | Active fixes |
|--------|:-:|:-:|
| v3.38.x (current) | ✅ | ✅ |
| v3.37.x | ✅ | ✅ |
| v3.36.x | ✅ | Critical fixes only |
| v3.35.x and earlier | ⚠️ | Recommendation: upgrade to v3.38.x |

The `stable` and `main` branches are officially supported. Other branches (`Authentique-non-modifiable`, `Clonflit-*`, `conflict_*`, `secour`, `mise_jour_E1_*`) are experimental and receive no fix commitment.

---

## 3. Accepted issue categories

We accept reports for:

### 3.1 Application security
- Unintended code execution via user input (CLI, RAG, unsanitized prompt injection)
- Leakage of an API key (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `EMERGENT_LLM_KEY`) in logs, PNGs, or audit trails
- Bypass of the `PreReasoner` allowing external LLM calls without guardrails
- Corruption or forgery of a signed `audit_trail_*.json`
- Bypass of `docker-compose` isolation (privilege escalation, arbitrary volume mounts)

### 3.2 Mathematical integrity
- Incorrect spectral result or non-deterministic numerical reproduction
- Divergence between `theories/methode_spectral.thy` (source of truth) and the Python implementation
- Regression of any of the 1732 Pytest cases without an immediate fix
- Inconsistency between the 8 linguistic versions of the `.thy` (the HOL code MUST remain **bit-for-bit identical** across FR/EN/ES/DE/PT/RU/ZH/JA)

### 3.3 Build chain
- Isabelle build failure on `main` (`isabelle build -D theories/` must succeed)
- Failure of the `build.yml` GitHub Actions workflow
- Regression in Docker image generation (`docker compose build --no-cache`)

### 3.4 Privacy and compliance
- Leakage of the author's personal information not disclosed in the README
- Use of code or libraries in violation of the licences cited in the README
- Incorrect attribution of the Spectral Method to a third party

---

## 4. How to report an issue

### 4.1 Private channel (strongly recommended for critical vulnerabilities)

Send an email to:

**`2racinede4carreunivers@gmail.com`**

Suggested subject line:
```
[SECURITY-GABRIEL] <category> — <5-word summary>
```

Example:
```
[SECURITY-GABRIEL] Key leak — Universal Key visible in Docker logs
```

### 4.2 Public channel (for non-critical issues)

Open a GitHub *issue*:

**`https://github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local/issues/new`**

Use the `[SECURITY]` prefix in the title. **Never post** API keys, tokens, or content extracted from a `.env` file in a public issue.

### 4.3 Information to include in your report

To speed up triage, please attach:

- **Affected version** (e.g., `v3.38.1`, commit hash `6c0383f`)
- **Environment** (OS, Python version, Isabelle version, Docker version)
- **Minimal, deterministic reproduction steps**
- **Expected behaviour** vs **observed behaviour**
- **Relevant logs** (excerpts, not full files — with API keys redacted beforehand)
- **Perceived impact** (leak, crash, mathematical divergence, test regression, etc.)
- **Proof of concept** if applicable (minimal script reproducing the issue)

A report template is available at `docs/security_report_template.md` (to be created if missing).

---

## 5. Handling commitments

| Stage | Indicative timeline |
|-------|:-:|
| Acknowledgement of report | Within **72 business hours** |
| Initial triage and categorization | Within **7 days** |
| Fix or mitigation plan | Depending on severity (see §6) |
| Publication of the fix on `main` | After validation by the 1732 Pytest cases + `isabelle build` |
| Public communication (if applicable) | After the fix, with credit to the reporter |

---

## 6. Severity classification

| Level | Description | Fix target |
|:-:|--------|:-:|
| **P0 — Critical** | API key leak, arbitrary code execution, `audit_trail` corruption | ≤ 48 h |
| **P1 — High** | Major mathematical regression, Isabelle build failure on `main`, divergence between linguistic versions of the `.thy` | ≤ 7 days |
| **P2 — Medium** | Isolated Pytest regression, non-exploitable CLI crash, GitHub Actions warning | ≤ 30 days |
| **P3 — Low** | Typographical error, comment typo, cosmetic improvement | Next minor release |

---

## 7. Responsible disclosure policy

We ask reporters to respect the following principles:

1. **Temporary confidentiality**: do not publicly disclose a vulnerability until a fix is published on `main` AND available in a released Docker image.
2. **Embargo window**: by default, **90 days** after receipt of the report, or earlier if the fix is published.
3. **No exploitation**: do not exploit the vulnerability beyond the minimum needed for demonstration.
4. **No destructive testing**: do not launch denial-of-service attacks, nor attempt to access other users' data.

In exchange, we commit to:

- **Credit the reporter** in the CHANGELOG and release notes, unless anonymity is requested.
- **Not pursue legal action** against good-faith researchers respecting this policy.
- **Provide regular status updates** during investigation.

---

## 8. Out-of-scope items

The following reports do **not** fall under this security policy:

- Feature suggestions (use a standard GitHub *feature request*)
- Non-security behavioural bugs (use a standard GitHub *bug report*)
- Debates on the mathematical validity of the Spectral Method (see `theories/methode_spectral.thy` and associated publications)
- Third-party LLM behaviour (Claude, GPT) — these vendors have their own reporting channels
- Issues affecting only unsupported versions (see §2)
- Vulnerabilities in third-party dependencies already tracked in `requirements.txt` — report to the vendor concerned

---

## 9. Attribution and acknowledgements

The list of reporters who contributed to improving Gabriel Multi-Loop's security is maintained in `SECURITY_HALL_OF_FAME.md` (created upon the first credited report).

---

## 10. Author, intellectual property and jurisdiction

- **Sole author** of the Spectral Method,Géométrie du spectre des nombres premiers and the theorie "L'univers est au carré" and of the Gabriel Multi-Loop implementation: **Philippe Thomas Savard**
- **Address**: Lévis, Chaudière-Appalaches, Quebec, Canada
- **Governing law** for security disputes: **Quebec law** and, subsidiarily, **Canadian federal law**
- **Source code licence**: see `LICENSE` at the root of the repository

---

## 11. Revision history

| Date | Version | Change |
|------|---------|--------|
| 2026-07-25 | 1.0 | Initial creation of the security policy (English mirror of `declaration_securite.md`) |

---

## 12. Quick contact

| Need | Channel |
|------|---------|
| Confidential critical vulnerability | `2racinede4carreunivers@gmail.com` |`philippethomassavar@gmail.com` `philippotcarre@outlook.com`
| Non-security bug | GitHub Issues (prefix `[BUG]`) |
| Question about this policy | GitHub Issues (prefix `[SECURITY-QUESTION]`) |
| Contribution / fix submission | Pull Request on the `main` branch |

---

*This document is published under the same terms as the source code of the Gabriel Multi-Loop repository. Any substantial change will be noted in section §11 "Revision history".*
