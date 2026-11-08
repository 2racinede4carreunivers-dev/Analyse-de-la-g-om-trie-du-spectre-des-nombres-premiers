#!/usr/bin/env python3
"""LaTeX boitenote Environment Fixer"""

import re
import os
import sys
import argparse

def find_boitenotes(content):
    pattern = r'\\begin{boitenote(\[([^\]]*)\])?}'
    return list(re.finditer(pattern, content))

def find_closures(content):
    pattern = r'\\end{boitenote}'
    return list(re.finditer(pattern, content))

def fix_file(input_path, output_path=None):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    begins = find_boitenotes(content)
    ends = find_closures(content)

    print("Found %d \\begin{boitenote} environments" % len(begins))
    print("Found %d \\end{boitenote} environments" % len(ends))
    print("Missing %d closing tags" % (len(begins) - len(ends)))

    if len(begins) <= len(ends):
        print("No fixes needed.")
        return

    insertions = []
    for i, begin_match in enumerate(begins):
        start_pos = begin_match.start()
        if i < len(begins) - 1:
            end_pos = begins[i + 1].start()
        else:
            doc_end = content.rfind('\\end{document}')
            end_pos = doc_end if doc_end != -1 else len(content)

        context = content[max(0, end_pos - 50):end_pos + 50]
        if '\\end{boitenote}' not in context:
            insertions.append((end_pos, '\n\\end{boitenote}\n'))

    insertions.sort(key=lambda x: x[0], reverse=True)
    for pos, text in insertions:
        content = content[:pos] + text + content[pos:]

    if output_path is None:
        output_path = input_path.replace('.tex', '_fixed.tex')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("\nFixed! Output: %s" % output_path)
    print("Added %d \\end{boitenote} tags." % len(insertions))

def main():
    parser = argparse.ArgumentParser(description='Fix unclosed boitenote environments')
    parser.add_argument('input', help='Input LaTeX file')
    parser.add_argument('-o', '--output', help='Output file (default: input_fixed.tex)')
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    if not os.path.exists(input_path):
        print("Error: File not found: %s" % input_path)
        sys.exit(1)

    fix_file(input_path, output_path)

if __name__ == '__main__':
    main()