"""
analyste_tex.py — Lexer/tokenizer LaTeX à machine d'états finis.

Ce module lit un fichier .tex et produit une analyse token par token,
enregistrée dans la base SQLite ``relever_CMD_tex.db``.
"""
from __future__ import annotations

import re
import sqlite3
import json
from dataclasses import dataclass, field
from pathlib import Path

# ── Constantes ──────────────────────────────────────────────────────────────

VERBATIM_ENVS = {"verbatim", "Verbatim", "lstlisting", "Verbatim*"}

TOBOX_ENVS = {
    "boitenote", "boitealerte", "boitecalc", "boiteexo",
    "boitedef", "boitereference", "boiteex", "boite",
}

STRUCTURAL_COMMANDS = {
    "part", "chapter", "section", "subsection",
    "subsubsection", "paragraph", "subparagraph",
}


# ── Classes de données ───────────────────────────────────────────────────────

@dataclass
class Token:
    """Un token LaTeX."""
    token_type: str
    raw_text: str
    line_num: int
    col_num: int
    seq: int = 0
    command_name: str = ""
    env_name: str = ""
    extra: dict = field(default_factory=dict)


@dataclass
class EnvironmentFrame:
    """Une entrée dans la pile d'environnements."""
    env_name: str
    begin_seq: int
    begin_line: int
    begin_col: int
    nesting_level: int
    end_seq: int | None = None
    end_line: int | None = None
    closed: bool = False




# ── Tokenizer à machine d'états ──────────────────────────────────────────────

class LaTeXTokenizer:
    r"""
    Tokeniseur LaTeX conscient du contexte.

    États internes :
        NORMAL      — texte ordinaire
        COMMENT     — à l'intérieur d'un ``%...``
        MATH_DOLLAR — à l'intérieur de ``$...$``
        MATH_DISPLAY — à l'intérieur de ``$$...$$``
        MATH_PAREN  — à l'intérieur de ``\(...\)``
        MATH_BRACKET — à l'intérieur de ``\[...\]``
        VERBATIM    — à l'intérieur d'un bloc verbatim
    """

    _RE_COMMAND = re.compile(r"[A-Za-z@]+")
    _RE_OPTIONAL_ARG = re.compile(r"\[([^\]]*)\]")
    _RE_WHITESPACE = re.compile(r"\s+")

    def __init__(self, content: str) -> None:
        self.content = content
        self.pos = 0
        self.length = len(content)
        self.line = 1
        self.col = 1
        self.tokens: list[Token] = []
        self._seq = 0

    # ── Utilitaires de position ───────────────────────────────────────────────

    def _peek(self, offset: int = 0) -> str:
        """Retourne le caractère à `offset` positions en avant."""
        idx = self.pos + offset
        if idx < self.length:
            return self.content[idx]
        return ""

    def _advance(self) -> str:
        """Consomme un caractère et met à jour ligne/colonne."""
        ch = self.content[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    # ── Tokenizer principal ───────────────────────────────────────────────────

    def tokenize(self) -> list[Token]:
        """Tokenise le contenu complet et retourne la liste des tokens."""
        while self.pos < self.length:
            ch = self.content[self.pos]

            if ch == "%":
                self.tokens.append(self._read_comment())
                continue
            if ch == "\\":
                self._read_command()
                continue
            if ch == "$":
                self._read_math_dollar()
                continue
            if ch == "{":
                self._add_token("T_BRACE_OPEN", "{", self.line, self.col)
                self._advance()
                continue
            if ch == "}":
                self._add_token("T_BRACE_CLOSE", "}", self.line, self.col)
                self._advance()
                continue
            if ch == "[":
                self._add_token("T_BRACKET_OPEN", "[", self.line, self.col)
                self._advance()
                continue
            if ch == "]":
                self._add_token("T_BRACKET_CLOSE", "]", self.line, self.col)
                self._advance()
                continue

            if ch.isspace():
                self._read_whitespace()
                continue

            # \[[
            if ch == "\\" and self._peek(1) == "[":
                self._read_bracket_math()
                continue
            # \]
            if ch == "\\" and self._peek(1) == "]":
                token_start_line, token_start_col = self.line, self.col
                self._advance()
                self._advance()
                self._add_token("T_COMMAND", "\\]",
                                token_start_line, token_start_col,
                                command_name="]")
                continue

            self._read_text()

        return self.tokens

    # ── Lecture des commandes LaTeX ──────────────────────────────────────────

    def _read_command(self) -> None:
        """
        Lit une commande LaTeX (``\\command`` ou ``\\begin{env}`` / ``\\end{env}``).
        Gère spécialement ``\\begin``, ``\\end``, ``\\verb``, ``\[``, ``\]``.
        """
        start_line, start_col = self.line, self.col
        self._advance()  # backslash

        name_match = self._RE_COMMAND.match(self.content, self.pos)
        if not name_match:
            ch = self._advance()
            self._add_token("T_COMMAND", f"\\{ch}", start_line, start_col,
                            command_name=ch, extra={"is_bare_backslash": True})
            return

        cmd_name = name_match.group(0)
        for _ in cmd_name:
            self._advance()

        if cmd_name == "begin":
            self._handle_begin(start_line, start_col, cmd_name)
            return
        if cmd_name == "end":
            self._handle_end(start_line, start_col, cmd_name)
            return
        if cmd_name in ("verb", "Verb"):
            self._read_verb(start_line, start_col, cmd_name)
            return

        # Arguments optionnels [...]
        args: list[str] = []
        opt_match = self._RE_OPTIONAL_ARG.match(self.content[self.pos:])
        if opt_match:
            opt_text = opt_match.group(0)
            args.append(f"[{opt_text[1:-1]}]")
            for _ in opt_text:
                self._advance()

        # Arguments obligatoires {...}
        while self._peek() == "{":
            self._advance()
            brace_content = ""
            depth = 1
            while self.pos < self.length and depth > 0:
                ch = self._advance()
                if ch == "{":
                    depth += 1
                    brace_content += ch
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        break
                    brace_content += ch
                else:
                    brace_content += ch
            args.append(f"{{{brace_content}}}")

        self._add_token("T_COMMAND", f"\\{cmd_name}", start_line, start_col,
                        command_name=cmd_name,
                        extra={"args": args})

    def _handle_begin(self, start_line: int, start_col: int,
                      cmd_name: str) -> None:
        """Traite ``\\begin{env}``."""
        if self._peek() != "{":
            self._add_token("T_COMMAND", f"\\{cmd_name}", start_line, start_col,
                            command_name=cmd_name)
            return

        env_name = self._read_braced_content()

        opt_text = ""
        if self._peek() == "[":
            opt_text = self._read_optional_arg()

        full_text = f"\\begin{{{env_name}}}{opt_text}"
        extra: dict = {"args": [opt_text] if opt_text else []}

        if env_name in VERBATIM_ENVS:
            self._read_verb_block(start_line, start_col, env_name, full_text, extra)
            return

        is_box = env_name.lower() in TOBOX_ENVS
        self._add_token("T_BEGIN", full_text, start_line, start_col,
                        command_name="begin", env_name=env_name,
                        extra={**extra, "is_tcolorbox": is_box})

    def _handle_end(self, start_line: int, start_col: int,
                    cmd_name: str) -> None:
        """Traite ``\\end{env}``."""
        if self._peek() != "{":
            self._add_token("T_COMMAND", f"\\{cmd_name}", start_line, start_col,
                            command_name=cmd_name)
            return

        env_name = self._read_braced_content()
        full_text = f"\\end{{{env_name}}}"
        is_box = env_name.lower() in TOBOX_ENVS
        self._add_token("T_END", full_text, start_line, start_col,
                        command_name="end", env_name=env_name,
                        extra={"is_tcolorbox": is_box})

    def _read_verb(self, start_line: int, start_col: int,
                   cmd_name: str) -> None:
        """Traite ``\\verb<delim>...<delim>``."""
        delim = self._advance() if self.pos < self.length else "|"
        if delim == "*":
            delim = self._advance() if self.pos < self.length else "|"

        raw = f"\\{cmd_name}" + delim
        while self.pos < self.length:
            ch = self._advance()
            raw += ch
            if ch == delim:
                break
        self._add_token("T_VERB_INLINE", raw, start_line, start_col,
                        command_name=cmd_name,
                        extra={"delim": delim})

    def _read_verb_block(self, start_line: int, start_col: int,
                         env_name: str, begin_text: str,
                         extra: dict) -> None:
        """Lit un bloc verbatim complet (``\\begin{env}`` ... ``\\end{env}``)."""
        end_marker = f"\\end{{{env_name}}}"
        content = ""
        found_end = False
        while self.pos < self.length:
            if self.content[self.pos:self.pos + len(end_marker)] == end_marker:
                for _ in end_marker:
                    self._advance()
                found_end = True
                break
            content += self._advance()

        full_text = begin_text + content + end_marker
        self._add_token("T_VERBATIM", full_text, start_line, start_col,
                        env_name=env_name,
                        extra={**extra, "content_length": len(content),
                               "end_marker_found": found_end})

    def _read_math_dollar(self) -> None:
        """Lit une zone mathématique ``$...$`` ou ``$$...$$``."""
        start_line, start_col = self.line, self.col

        if self._peek(1) == "$":
            self._advance()
            self._advance()
            content = ""
            while self.pos < self.length:
                if self._peek() == "$" and self._peek(1) == "$":
                    self._advance()
                    self._advance()
                    break
                content += self._advance()
            self._add_token("T_MATH_DISPLAY", "$$" + content + "$$",
                            start_line, start_col, extra={"delim": "$$"})
        elif self._peek(1) == "\\" and self._peek(2) == ")":
            self._advance()
            self._advance()
            self._advance()
            content = ""
            while self.pos < self.length:
                if self._peek() == "\\" and self._peek(1) == ")":
                    self._advance()
                    self._advance()
                    break
                content += self._advance()
            self._add_token("T_MATH_INLINE", f"\\({content}\\)" if content else "\\(\\)",
                            start_line, start_col, extra={"delim": "\\("})
        else:
            self._advance()
            content = ""
            while self.pos < self.length:
                ch = self._peek()
                if ch == "$":
                    self._advance()
                    break
                content += self._advance()
            self._add_token("T_MATH_INLINE", "$" + content + "$",
                            start_line, start_col, extra={"delim": "$"})

    def _read_bracket_math(self) -> None:
        """Lit une zone mathématique ``\\[...\\]``."""
        start_line, start_col = self.line, self.col
        self._advance()
        self._advance()
        content = ""
        while self.pos < self.length:
            if self._peek() == "\\" and self._peek(1) == "]":
                self._advance()
                self._advance()
                break
            content += self._advance()
        self._add_token("T_MATH_DISPLAY", f"\\[{content}\\]",
                        start_line, start_col, extra={"delim": "\\["})

    def _read_comment(self) -> None:
        """Lit un commentaire ``%...`` jusqu'à la fin de ligne."""
        start_line, start_col = self.line, self.col
        text = ""
        while self.pos < self.length:
            ch = self._advance()
            text += ch
            if ch == "\n":
                break
        self._add_token("T_COMMENT", text, start_line, start_col)

    def _read_whitespace(self) -> None:
        """Lit un bloc de whitespace consécutif."""
        start_line, start_col = self.line, self.col
        text = ""
        while self.pos < self.length and self.content[self.pos].isspace():
            text += self._advance()
        self._add_token("T_WHITESPACE", text, start_line, start_col)

    def _read_text(self) -> None:
        """Lit du texte jusqu'au prochain caractère spécial."""
        start_line, start_col = self.line, self.col
        text = ""
        while self.pos < self.length:
            ch = self.content[self.pos]
            if ch in "%$\\{}[]\n":
                break
            if ch == "\\" and self._peek(1) == "[":
                break
            if ch == "\\" and self._peek(1) == "]":
                break
            text += self._advance()
        if text:
            self._add_token("T_TEXT", text, start_line, start_col)
        else:
            self._advance()

    def _read_braced_content(self) -> str:
        """Lit le contenu entre ``{`` et ``}`` (imbrication possible)."""
        self._advance()
        content = ""
        depth = 1
        while self.pos < self.length and depth > 0:
            ch = self._advance()
            if ch == "{":
                depth += 1
                content += ch
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    break
                content += ch
            else:
                content += ch
        return content

    def _read_optional_arg(self) -> str:
        """Lit le contenu entre ``[`` et ``]``."""
        self._advance()
        content = "["
        while self.pos < self.length:
            ch = self._advance()
            content += ch
            if ch == "]":
                break
        return content

    def _add_token(self, token_type: str, raw_text: str,
                   line_num: int, col_num: int,
                   command_name: str = "", env_name: str = "",
                   extra: dict | None = None) -> None:
        """Ajoute un token à la liste avec numéro de séquence."""
        self._seq += 1
        token = Token(
            token_type=token_type,
            raw_text=raw_text,
            line_num=line_num,
            col_num=col_num,
            seq=self._seq,
            command_name=command_name,
            env_name=env_name,
            extra=extra or {},
        )
        self.tokens.append(token)

    # ── Analyse post-tokenisation ──────────────────────────────────────────────

    def analyze(self) -> dict:
        """
        Analyse les tokens pour produire :
          • La pile d'environnements (avec fermeture ou non)
          • La profondeur d'accolades
          • La balance des modes mathématiques
          • Les points structurels (headings)
        """
        env_stack: list[EnvironmentFrame] = []
        all_envs: list[EnvironmentFrame] = []
        brace_depth = 0
        structural_points: list[dict] = []
        issues: list[dict] = []

        # Filtrer les tokens None (peut arriver si un caractère est consommé sans token)
        valid_tokens = [t for t in self.tokens if t is not None]

        for token in valid_tokens:
            if token.token_type == "T_BEGIN":
                frame = EnvironmentFrame(
                    env_name=token.env_name,
                    begin_seq=token.seq,
                    begin_line=token.line_num,
                    begin_col=token.col_num,
                    nesting_level=len(env_stack) + 1,
                )
                env_stack.append(frame)
                all_envs.append(frame)

            elif token.token_type == "T_END":
                if env_stack and env_stack[-1].env_name == token.env_name:
                    frame = env_stack.pop()
                    frame.end_seq = token.seq
                    frame.end_line = token.line_num
                    frame.closed = True
                else:
                    issues.append({
                        "type": "STRAY_END",
                        "line": token.line_num,
                        "col": token.col_num,
                        "description": f"\\end{{{token.env_name}}} sans \\begin correspondant",
                        "token_seq": token.seq,
                    })

            elif token.token_type == "T_BRACE_OPEN":
                brace_depth += 1

            elif token.token_type == "T_BRACE_CLOSE":
                brace_depth -= 1
                if brace_depth < 0:
                    issues.append({
                        "type": "EXTRA_BRACE_CLOSE",
                        "line": token.line_num,
                        "col": token.col_num,
                        "description": "Accolade fermante excédentaire",
                        "token_seq": token.seq,
                    })
                    brace_depth = 0

            if token.token_type == "T_COMMAND" and \
               token.command_name in STRUCTURAL_COMMANDS:
                structural_points.append({
                    "line": token.line_num,
                    "col": token.col_num,
                    "command": token.command_name,
                    "seq": token.seq,
                    "full_text": token.raw_text,
                })

        # Environnements non fermés
        for frame in env_stack:
            issues.append({
                "type": "UNCLOSED_ENV",
                "line": frame.begin_line,
                "description": f"Environnement '{frame.env_name}' non fermé",
            })

        return {
            "env_stack": env_stack,
            "all_envs": all_envs,
            "brace_depth": brace_depth,
            "issues": issues,
            "structural_points": structural_points,
        }

# ── Fonction principale d'analyse et persistance ─────────────────────────────

def analyze_tex_file(tex_path: Path, db_dir: Path) -> Path:
    """
    Analyse un fichier .tex et persiste les résultats dans une base SQLite.

    Parameters
    ----------
    tex_path : Path
        Chemin vers le fichier .tex source
    db_dir : Path
        Répertoire où créer la base de données

    Returns
    -------
    Path
        Chemin vers la base de données créée
    """
    db_dir.mkdir(parents=True, exist_ok=True)
    db_path = db_dir / "relever_CMD_tex_v2.db"
    if db_path.exists():
        db_path.unlink()

    content = tex_path.read_text(encoding="utf-8")

    tokenizer = LaTeXTokenizer(content)
    tokens = tokenizer.tokenize()
    analysis = tokenizer.analyze()

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE tokens (
            seq INTEGER PRIMARY KEY,
            token_type TEXT,
            raw_text TEXT,
            line_num INTEGER,
            col_num INTEGER,
            command_name TEXT,
            env_name TEXT,
            extra_json TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE environments (
            env_id INTEGER PRIMARY KEY AUTOINCREMENT,
            env_name TEXT,
            begin_seq INTEGER,
            end_seq INTEGER,
            begin_line INTEGER,
            begin_col INTEGER,
            end_line INTEGER,
            nesting_level INTEGER,
            closed INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE commands (
            cmd_id INTEGER PRIMARY KEY AUTOINCREMENT,
            token_seq INTEGER,
            command_name TEXT,
            line_num INTEGER,
            col_num INTEGER,
            extra_json TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE structural_points (
            point_id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT,
            line_num INTEGER,
            col_num INTEGER,
            token_seq INTEGER,
            full_text TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE meta (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    # Filtrer les tokens None
    valid_tokens = [t for t in tokens if t is not None]

    for token in valid_tokens:
        cursor.execute(
            "INSERT INTO tokens VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (token.seq, token.token_type, token.raw_text,
             token.line_num, token.col_num,
             token.command_name, token.env_name,
             json.dumps(token.extra))
        )

    for frame in analysis["all_envs"]:
        cursor.execute(
            "INSERT INTO environments VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)",
            (frame.env_name, frame.begin_seq, frame.end_seq,
             frame.begin_line, frame.begin_col,
             frame.end_line, frame.nesting_level,
             1 if frame.closed else 0)
        )

    for token in valid_tokens:
        if token.token_type == "T_COMMAND":
            if token.command_name not in ("begin", "end"):
                cursor.execute(
                    "INSERT INTO commands VALUES (NULL, ?, ?, ?, ?, ?)",
                    (token.seq, token.command_name,
                     token.line_num, token.col_num,
                     json.dumps(token.extra))
                )

    for point in analysis["structural_points"]:
        cursor.execute(
            "INSERT INTO structural_points VALUES (NULL, ?, ?, ?, ?, ?)",
            (point["command"], point["line"], point["col"],
             point["seq"], point["full_text"])
        )

    cursor.execute(
        "INSERT INTO meta VALUES ('total_lines', ?)",
        (content.count("\n") + 1,)
    )
    cursor.execute(
        "INSERT INTO meta VALUES ('total_tokens', ?)",
        (len(tokens),)
    )
    cursor.execute(
        "INSERT INTO meta VALUES ('total_environments', ?)",
        (len(analysis["all_envs"]),)
    )
    cursor.execute(
        "INSERT INTO meta VALUES ('unclosed_environments', ?)",
        (len(analysis["env_stack"]),)
    )
    cursor.execute(
        "INSERT INTO meta VALUES ('brace_depth_final', ?)",
        (analysis["brace_depth"],)
    )

    conn.commit()
    conn.close()

    return db_path


# ── Entrée principale ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent
    tex_path = repo_root / "theories" / "tex" / "Le-systeme-convolutif-Gabriel.tex"
    db_dir = Path(__file__).resolve().parent / "data"

    print(f"Analyse du fichier : {tex_path}")
    db_path = analyze_tex_file(tex_path, db_dir)
    print(f"Base de données créée : {db_path}")

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute("SELECT key, value FROM meta")
    for key, value in cursor.fetchall():
        print(f"  {key}: {value}")

    cursor.execute(
        "SELECT token_type, COUNT(*) FROM tokens GROUP BY token_type ORDER BY token_type"
    )
    print("\nRépartition des tokens :")
    for ttype, count in cursor.fetchall():
        print(f"  {ttype}: {count}")

    cursor.execute(
        "SELECT env_name, COUNT(*) as cnt, SUM(closed) as closed "
        "FROM environments GROUP BY env_name ORDER BY cnt DESC"
    )
    print("\nEnvironnements rencontrés :")
    for env_name, cnt, closed in cursor.fetchall():
        status = "OK" if cnt == closed else f"NON FERMÉS ({cnt - closed})"
        print(f"  {env_name}: {cnt} ({status})")

    conn.close()
