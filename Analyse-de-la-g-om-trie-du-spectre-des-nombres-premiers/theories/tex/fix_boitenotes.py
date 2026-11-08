#!/usr/bin/env python3
"""LaTeX boitenote Environment Fixer."""
import re, os, sys

def find_boitenotes(content):
    r"""Find all \begin{boitenote} environments."""
    return list(re.finditer(r'\\begin{boitenote(\[([^\]]*)\])?}', content))

def find_boitenote_closures(content):
    r"""Find all \end{boitenote} environments."""
    return list(re.finditer(r'\\end{boitenote}', content))

def fix_boitenotes(input_path, output_path=None):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    begins = find_boitenotes(content)
    ends = find_boitenote_closures(content)
    print('Found %d \\begin{boitenote}' % len(begins))
    print('Found %d \\end{boitenote}' % len(ends))
    print('Missing %d closing tags' % (len(begins) - len(ends)))
    begin_positions = [m.start() for m in begins]
    insertions = []
    for i, begin_pos in enumerate(begin_positions):
        if i < len(begin_positions) - 1:
            end_pos = begin_positions[i + 1]
        else:
            doc_end = content.rfind('\\end{document}')
            end_pos = doc_end if doc_end != -1 else len(content)
        segment = content[begin_pos:end_pos]
        if '\\end{boitenote}' not in segment:
            insertions.append((end_pos, '\n\\end{boitenote}\n'))
    insertions.sort(key=lambda x: x[0], reverse=True)
    for pos, text in insertions:
        content = content[:pos] + text + content[pos:]
    if output_path is None:
        output_path = input_path.replace('.tex', '_fixed.tex')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Fixed! Output: %s' % output_path)
    print('Added %d \\end{boitenote} tags.' % len(insertions))
    return output_path

def main():
    if len(sys.argv) < 2:
        print('Usage: python fix_boitenotes.py <input.tex> [output.tex]')
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    if not os.path.exists(input_path):
        print('Error: File not found: %s' % input_path)
        sys.exit(1)
    fix_boitenotes(input_path, output_path)

if __name__ == '__main__':
    main()
