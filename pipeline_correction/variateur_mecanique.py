import sqlite3
import os
import re

DB_PATH = "data/convolutive_spectral.db"

def query_db_range(n: int, k_start: int, k_end: int) -> list[tuple[str, int]]:
    if not os.path.exists(DB_PATH):
        return []
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT ratio_label, p_value 
        FROM p_reconstructions 
        WHERE n = ? AND ratio_k BETWEEN ? AND ?
        ORDER BY ratio_k ASC
    ''', (n, k_start, k_end))
    rows = cursor.fetchall()
    conn.close()
    return rows

def process_query_variateur(query_text: str) -> str | None:
    range_match = re.search(r"1/(\d+)\s+à\s+1/(\d+)", query_text)
    n_match = re.search(r"n\s*=\s*(\d+)", query_text)
    n_val = int(n_match.group(1)) if n_match else 10

    k_start, k_end = None, None
    if range_match:
        k_start = int(range_match.group(1))
        k_end = int(range_match.group(2))
    elif "1/10" in query_text and "1/111" in query_text:
        k_start, k_end = 10, 111

    if k_start is not None and k_end is not None:
        results = query_db_range(n_val, k_start, k_end)
        if results:
            lines = [f"### Valeurs de P extraites de `convolutive_spectral.db` (n = {n_val})\n"]
            lines.append("| Rapport (1/k) | Nombre Premier P |")
            lines.append("| :--- | :--- |")
            for ratio, p_val in results:
                lines.append(f"| {ratio} | {p_val:,}".replace(",", " ") + " |")
            return "\n".join(lines)

    return None
