#!/usr/bin/env python3
"""Convert a DOCX into a compilable LaTeX document with structural fidelity.

This converter keeps the document flow order and maps:
- Heading1/2/3 -> section/subsection/subsubsection
- Word lists -> enumerate
- Word tables -> longtable
- Hyperlinks and footnotes where present
"""

from __future__ import annotations

import argparse
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
DC_NS = "http://purl.org/dc/elements/1.1/"
CP_NS = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"

NS = {"w": W_NS, "r": R_NS}


def qn(ns: str, tag: str) -> str:
    return f"{{{ns}}}{tag}"


def normalize_ws(text: str) -> str:
    text = text.replace("\r", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def escape_latex(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "#": r"\#",
        "$": r"\$",
        "%": r"\%",
        "&": r"\&",
        "_": r"\_",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    out = []
    for ch in text:
        out.append(replacements.get(ch, ch))
    return "".join(out)


def extract_text_from_run(run: ET.Element, footnotes: dict[str, str]) -> str:
    parts: list[str] = []
    for node in run.iter():
        if node.tag == qn(W_NS, "t"):
            parts.append(node.text or "")
        elif node.tag in {qn(W_NS, "br"), qn(W_NS, "cr")}:
            parts.append("\n")
        elif node.tag == qn(W_NS, "tab"):
            parts.append("\t")
        elif node.tag == qn(W_NS, "footnoteReference"):
            fid = node.get(qn(W_NS, "id"))
            if fid and fid in footnotes:
                parts.append(f" [Note: {footnotes[fid]}]")
    return "".join(parts)


def extract_inline_text(paragraph: ET.Element, rels: dict[str, str], footnotes: dict[str, str]) -> str:
    parts: list[str] = []
    for child in paragraph:
        if child.tag == qn(W_NS, "r"):
            parts.append(extract_text_from_run(child, footnotes))
        elif child.tag == qn(W_NS, "hyperlink"):
            rid = child.get(qn(R_NS, "id"))
            label_parts = []
            for sub in child:
                if sub.tag == qn(W_NS, "r"):
                    label_parts.append(extract_text_from_run(sub, footnotes))
            label = "".join(label_parts)
            target = rels.get(rid or "")
            if target and label:
                parts.append(f"{label} ({target})")
            elif label:
                parts.append(label)
    text = "".join(parts)
    text = normalize_ws(text)
    return text


def get_paragraph_style(paragraph: ET.Element) -> str | None:
    ppr = paragraph.find("w:pPr", NS)
    if ppr is None:
        return None
    pstyle = ppr.find("w:pStyle", NS)
    if pstyle is None:
        return None
    return pstyle.get(qn(W_NS, "val"))


def get_num_level(paragraph: ET.Element) -> int | None:
    ppr = paragraph.find("w:pPr", NS)
    if ppr is None:
        return None
    num_pr = ppr.find("w:numPr", NS)
    if num_pr is None:
        return None
    ilvl = num_pr.find("w:ilvl", NS)
    if ilvl is None:
        return 0
    val = ilvl.get(qn(W_NS, "val"))
    try:
        return int(val) if val is not None else 0
    except ValueError:
        return 0


def load_relationships(docx_path: Path) -> dict[str, str]:
    rels: dict[str, str] = {}
    with zipfile.ZipFile(docx_path, "r") as zf:
        rel_path = "word/_rels/document.xml.rels"
        if rel_path not in zf.namelist():
            return rels
        root = ET.fromstring(zf.read(rel_path))
        for rel in root.findall(f"{{{PKG_REL_NS}}}Relationship"):
            rid = rel.get("Id")
            target = rel.get("Target")
            if rid and target:
                rels[rid] = target
    return rels


def load_footnotes(docx_path: Path) -> dict[str, str]:
    footnotes: dict[str, str] = {}
    with zipfile.ZipFile(docx_path, "r") as zf:
        path = "word/footnotes.xml"
        if path not in zf.namelist():
            return footnotes
        root = ET.fromstring(zf.read(path))
        for fn in root.findall("w:footnote", NS):
            fid = fn.get(qn(W_NS, "id"))
            if not fid or fid in {"0", "1", "-1"}:
                continue
            texts: list[str] = []
            for t in fn.findall(".//w:t", NS):
                texts.append(t.text or "")
            merged = normalize_ws("".join(texts))
            if merged:
                footnotes[fid] = merged
    return footnotes


def load_core_metadata(docx_path: Path) -> tuple[str, str]:
    title = "Document"
    author = "Auteur inconnu"
    with zipfile.ZipFile(docx_path, "r") as zf:
        core = "docProps/core.xml"
        if core not in zf.namelist():
            return title, author
        root = ET.fromstring(zf.read(core))
        title_node = root.find(f"{{{DC_NS}}}title")
        creator_node = root.find(f"{{{DC_NS}}}creator")
        if title_node is not None and title_node.text:
            title = title_node.text.strip()
        if creator_node is not None and creator_node.text:
            author = creator_node.text.strip()
    return title, author


def table_to_latex(tbl: ET.Element, rels: dict[str, str], footnotes: dict[str, str]) -> list[str]:
    rows: list[list[str]] = []
    for tr in tbl.findall("w:tr", NS):
        cells: list[str] = []
        for tc in tr.findall("w:tc", NS):
            paras: list[str] = []
            for p in tc.findall("w:p", NS):
                txt = extract_inline_text(p, rels, footnotes)
                if txt:
                    paras.append(escape_latex(txt))
            cells.append(" \\\\ ".join(paras))
        if cells:
            rows.append(cells)

    if not rows:
        return []

    max_cols = max(len(r) for r in rows)
    col_spec = "|" + "|".join(["p{%.3f\\textwidth}" % (0.94 / max_cols)] * max_cols) + "|"

    out = [r"\begin{longtable}{%s}" % col_spec, r"\hline"]
    for row in rows:
        if len(row) < max_cols:
            row = row + [""] * (max_cols - len(row))
        out.append(" & ".join(row) + r" \\")
        out.append(r"\hline")
    out.append(r"\end{longtable}")
    out.append("")
    return out


def convert(docx_path: Path, out_tex_path: Path) -> None:
    rels = load_relationships(docx_path)
    footnotes = load_footnotes(docx_path)
    title, author = load_core_metadata(docx_path)

    with zipfile.ZipFile(docx_path, "r") as zf:
        root = ET.fromstring(zf.read("word/document.xml"))

    body = root.find("w:body", NS)
    if body is None:
        raise RuntimeError("DOCX sans corps de document exploitable")

    lines: list[str] = []
    lines.extend(
        [
            r"\documentclass[11pt,a4paper]{article}",
            r"\usepackage[utf8]{inputenc}",
            r"\usepackage[T1]{fontenc}",
            r"\usepackage[french]{babel}",
            r"\usepackage{lmodern}",
            r"\usepackage{geometry}",
            r"\usepackage{hyperref}",
            r"\usepackage{longtable}",
            r"\usepackage{array}",
            r"\usepackage{booktabs}",
            r"\usepackage{enumitem}",
            r"\geometry{margin=2.4cm}",
            r"\setcounter{secnumdepth}{3}",
            r"\setcounter{tocdepth}{3}",
            r"\title{" + escape_latex(title) + "}",
            r"\author{" + escape_latex(author) + "}",
            r"\date{}",
            r"\begin{document}",
            r"\maketitle",
            r"\tableofcontents",
            r"\newpage",
            "",
        ]
    )

    list_depth = 0

    def close_lists_to(depth: int = 0) -> None:
        nonlocal list_depth
        while list_depth > depth:
            lines.append(r"\end{enumerate}")
            list_depth -= 1

    for child in body:
        if child.tag == qn(W_NS, "p"):
            text = extract_inline_text(child, rels, footnotes)
            style = get_paragraph_style(child)
            ilvl = get_num_level(child)

            if ilvl is not None:
                target_depth = ilvl + 1
                while list_depth < target_depth:
                    lines.append(r"\begin{enumerate}[leftmargin=*]")
                    list_depth += 1
                while list_depth > target_depth:
                    lines.append(r"\end{enumerate}")
                    list_depth -= 1
                if text:
                    lines.append(r"\item " + escape_latex(text))
                else:
                    lines.append(r"\item")
                continue
            else:
                close_lists_to(0)

            if not text:
                lines.append("")
                continue

            escaped = escape_latex(text)
            if style == "Heading1":
                lines.append(r"\section{" + escaped + "}")
            elif style == "Heading2":
                lines.append(r"\subsection{" + escaped + "}")
            elif style == "Heading3":
                lines.append(r"\subsubsection{" + escaped + "}")
            else:
                lines.append(escaped)
                lines.append("")

        elif child.tag == qn(W_NS, "tbl"):
            close_lists_to(0)
            lines.extend(table_to_latex(child, rels, footnotes))

        elif child.tag == qn(W_NS, "sectPr"):
            close_lists_to(0)
            continue

    close_lists_to(0)
    lines.append(r"\end{document}")

    out_tex_path.parent.mkdir(parents=True, exist_ok=True)
    out_tex_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="DOCX -> LaTeX converter")
    parser.add_argument("docx", type=Path, help="Path to source DOCX file")
    parser.add_argument("output", type=Path, help="Path to output TEX file")
    args = parser.parse_args()

    convert(args.docx, args.output)


if __name__ == "__main__":
    main()
