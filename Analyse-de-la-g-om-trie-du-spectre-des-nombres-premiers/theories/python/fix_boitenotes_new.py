#!/usr/bin/env python3
"""
LaTeX boitenote Environment Fixer

This script automatically fixes unclosed boitenote environments in LaTeX documents.
It identifies all \begin{boitenote} environments and inserts \end{boitenote} 
at the appropriate locations (before the next \begin{boitenote} or before \end{document}).

Usage:
    python3 fix_boitenotes.py Le-systeme-convolutif-Gabriel.tex

Or with a JSON patch file:
    python3 fix_boitenotes.py --patch corrections.json
"""

import re
import sys
import os
import json
import argparse


def find_boitenotes(content):
    """Find all \begin{boitenote} environments in the LaTeX content."""
    # Pattern to match \begin{boitenote}[optional arg]
    pattern = r'\\begin{boitenote(\[([^\]]*)\])?}'
    matches = list(re.finditer(pattern, content))
    return matches


def find_boitenote_closures(content):
    """Find all \end{boitenote} environments in the LaTeX content."""
    pattern = r'\\end{boitenote}'
    matches = list(re.finditer(pattern, content))
    return matches
