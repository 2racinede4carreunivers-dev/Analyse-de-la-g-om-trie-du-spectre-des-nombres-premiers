#!/usr/bin/env python3
"""LaTeX boitenote Environment Fixer v2 - Stack-based approach"""

import re
import os
import sys

def find_all_environments(content):
    """Find all \\begin{...} and \\end{...} tags in order."""
    pattern = r'\\(begin|end)\{([^}]+)\}'
    matches = list(re.finditer(pattern, content))
    return matches

def fix_boitenotes(input_path, output_path=None):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all environment tags
    env_tags = find_all_environments(content)
    
    # Stack-based matching
    stack = []
    boitenote_positions = []  # List of (begin_pos, end_pos) for each boitenote
    
    for match in env_tags:
        tag_type = match.group(1)  # 'begin' or 'end'
        env_name = match.group(2)  # environment name
        pos = match.start()
        
        if tag_type == 'begin':
            stack.append((env_name, pos, match))
        else:  # end
            # Find matching begin in stack
            for i in range(len(stack) - 1, -1, -1):
                if stack[i][0] == env_name:
                    # Found matching begin
                    begin_pos, begin_match = stack[i][1], stack[i][2]
                    if env_name == 'boitenote':
                        boitenote_positions.append((begin_pos, pos))
                    # Remove from stack
                    del stack[i:]
                    break
    
    # Find boitenote environments that don't have a matching end
    all_begins = [(m.start(), m) for m in re.finditer(r'\\begin\{boitenote(\[([^\]]*)\])?\}', content)]
    all_ends = [(m.start(), m) for m in re.finditer(r'\\end\{boitenote\}', content)]
    
    print("Found %d \\begin{boitenote}" % len(all_begins))
    print("Found %d \\end{boitenote}" % len(all_ends))
    print("Missing %d closing tags" % (len(all_begins) - len(all_ends)))
    
    # For each unclosed boitenote, find where to insert \end{boitenote}
    # Strategy: insert before the next \begin{boitenote} or \end{document}
    # but only if there's no \end{boitenote} already there
    
    # Find positions of all \begin{boitenote}
    begin_positions = [m.start() for m in re.finditer(r'\\begin\{boitenote(\[([^\]]*)\])?\}', content)]
    
    insertions = []
    for i, begin_pos in enumerate(begin_positions):
        # Find the end position for this boitenote
        if i < len(begin_positions) - 1:
            end_pos = begin_positions[i + 1]
        else:
            doc_end = content.rfind('\\end{document}')
            end_pos = doc_end if doc_end != -1 else len(content)
        
        # Check if there's already an \end{boitenote} in this range
        segment = content[begin_pos:end_pos]
        if '\\end{boitenote}' not in segment:
            insertions.append((end_pos, '\n\\end{boitenote}\n'))
    
    # Apply insertions in reverse order
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
    if len(sys.argv) < 2:
        print("Usage: python fix_boitenotes_v2.py <input.tex> [output.tex]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_path):
        print("Error: File not found: %s" % input_path)
        sys.exit(1)
    
    fix_boitenotes(input_path, output_path)

if __name__ == '__main__':
    main()