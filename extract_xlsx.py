#!/usr/bin/env python3
"""Extraction complète du fichier Excel systeme_convolutif_spectral_general.xlsx"""
import openpyxl

wb = openpyxl.load_workbook(
    r"C:\agent-multiloop-Gabriel-local\systeme_convolutif_spectral_general.xlsx",
    data_only=False
)
print("SHEETS:", wb.sheetnames)
print("=" * 70)
print("EXTRACTION DU CONTENU DE CHAQUE ONGLET")
print("=" * 70)

for name in wb.sheetnames:
    ws = wb[name]
    print(f"\n{'─' * 70}")
    print(f"📌 {name}  ({ws.max_row} lignes × {ws.max_column} colonnes)")
    print(f"{'─' * 70}")
    for row in ws.iter_rows(min_row=1, max_row=min(ws.max_row, 200), values_only=False):
        cells = []
        for cell in row:
            if cell.value is not None:
                cells.append(f"{cell.coordinate}={repr(cell.value)[:200]}")
        if cells:
            print("  ", " | ".join(cells))
