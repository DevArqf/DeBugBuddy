import ast
from pathlib import Path

def detect_all_errors(file_path: Path):
    all_errors = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.strip():
            return []

        if file_path.suffix != '.py':
            return [content]

        filename = str(file_path)
        lines = content.splitlines(keepends=True)
        current_lines = lines[:]
        max_iterations = 20
        seen_errors = set()

        for iteration in range(max_iterations):
            current_content = ''.join(current_lines)
            
            if not current_content.strip() or all(line.strip().startswith('#') or not line.strip() for line in current_lines):
                break
                
            try:
                ast.parse(current_content, filename=filename)
                break
            except (SyntaxError, IndentationError) as e:
                error_type = type(e).__name__
                lineno = e.lineno or 1
                msg = e.msg or "syntax error"
                
                error_id = f"{error_type}:{lineno}:{msg}"
                if error_id in seen_errors:
                    break
                seen_errors.add(error_id)
                
                error_msg = f"{error_type}: {msg}\n  File \"{filename}\", line {lineno}"
                if hasattr(e, 'text') and e.text:
                    error_msg += f"\n    {e.text.rstrip()}\n"
                    if hasattr(e, 'offset') and e.offset:
                        error_msg += f"    {' ' * (e.offset - 1)}^"
                
                all_errors.append(error_msg)

                if 0 <= lineno - 1 < len(current_lines):
                    offending_line = current_lines[lineno - 1]
                    if not offending_line.strip().startswith('#'):
                        stripped = offending_line.lstrip()
                        if stripped:
                            indent = offending_line[:len(offending_line) - len(stripped)]
                            commented = indent + '# ' + stripped
                            current_lines[lineno - 1] = commented
                        else:
                            current_lines[lineno - 1] = '# \n'
                else:
                    break

    except Exception as e:
        return []

    return all_errors