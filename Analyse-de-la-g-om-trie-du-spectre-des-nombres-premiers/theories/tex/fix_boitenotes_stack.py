import os
import re


def fix_boitenotes_with_stack(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    env_pattern = re.compile(r'\\(begin|end)\s*\{([^}]+)\}')

    lines = content.splitlines()
    new_lines = []

    stack = []
    opened_count = 0
    closed_count = 0
    auto_closed_count = 0

    for line in lines:
        matches = list(env_pattern.finditer(line))
        if not matches:
            new_lines.append(line)
            continue

        current_idx = 0
        parts = []
        for m in matches:
            start_pos = m.start()
            parts.append(line[current_idx:start_pos])

            tag_type = m.group(1)
            env_name = m.group(2).strip()

            if tag_type == 'begin':
                stack.append(env_name)
                parts.append(m.group(0))
                if env_name == 'boitenote':
                    opened_count += 1
            else:  # end
                if env_name in stack:
                    while stack and stack[-1] != env_name:
                        unclosed = stack.pop()
                        if unclosed == 'boitenote':
                            indent = '  ' * len(stack)
                            parts.append('\n%s\\end{boitenote}' % indent)
                            auto_closed_count += 1
                            closed_count += 1
                    if stack and stack[-1] == env_name:
                        stack.pop()
                        if env_name == 'boitenote':
                            closed_count += 1
                parts.append(m.group(0))

            current_idx = m.end()

        parts.append(line[current_idx:])
        new_lines.append(''.join(parts))

    while stack:
        unclosed = stack.pop()
        if unclosed == 'boitenote':
            new_lines.append('\\end{boitenote}')
            auto_closed_count += 1
            closed_count += 1

    print('--- Rapport d\'analyse stack-based ---')
    print('Total \\begin{boitenote} detectes : %d' % opened_count)
    print('\\end{boitenote} fermes automatiquement : %d' % auto_closed_count)
    print('Total \\end{boitenote} apres traitement : %d' % closed_count)

    return '\n'.join(new_lines)


if __name__ == '__main__':
    base = 'C:/Analyse-de-la-geometrie-du-spectre-des-nombres-premiers/Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers/theories/tex'
    target_file = base + '/Le-systeme-convolutif-Gabriel.tex'
    output_file = base + '/Le-systeme-convolutif-Gabriel_stack_fixed.tex'

    print('Analyse et correction par pile de : %s' % target_file)
    fixed_content = fix_boitenotes_with_stack(target_file)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    print('Fichier corrige genere avec succes : %s' % output_file)