import ast
from pathlib import Path

def detect_all_errors(file_path: Path):
    all_errors = []

    try:
        if not file_path.exists():
            return []
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.strip():
            return []

        if file_path.suffix != '.py':
            return [content]

        filename = str(file_path)
        lines = content.splitlines(keepends=True)
        
        if not lines:
            return []
            
        current_lines = lines[:]
        max_iterations = 20
        seen_errors = set()

        for iteration in range(max_iterations):
            current_content = ''.join(current_lines)
            
            non_comment_lines = [line for line in current_lines 
                               if line.strip() and not line.strip().startswith('#')]
            if not non_comment_lines:
                break
            
            try:
                ast.parse(current_content, filename=filename)
                break
                
            except SyntaxError as e:
                error_type = "SyntaxError"
                lineno = e.lineno if e.lineno else 1
                msg = e.msg if e.msg else "invalid syntax"
                
                error_id = f"{error_type}:{lineno}:{msg}"
                if error_id in seen_errors:
                    break
                seen_errors.add(error_id)
                
                error_msg = f"{error_type}: {msg}\n  File \"{filename}\", line {lineno}"
                
                if hasattr(e, 'text') and e.text:
                    error_msg += f"\n    {e.text.rstrip()}"
                    if hasattr(e, 'offset') and e.offset and e.offset > 0:
                        error_msg += f"\n    {' ' * (e.offset - 1)}^"
                
                all_errors.append(error_msg)

                if 0 <= lineno - 1 < len(current_lines):
                    offending_line = current_lines[lineno - 1]
                    
                    if not offending_line.strip().startswith('#'):
                        stripped = offending_line.lstrip()
                        if stripped:
                            indent = offending_line[:len(offending_line) - len(stripped)]
                            current_lines[lineno - 1] = f"{indent}# {stripped}"
                        else:
                            current_lines[lineno - 1] = '# \n'
                else:
                    break
                    
            except IndentationError as e:
                error_type = "IndentationError"
                lineno = e.lineno if e.lineno else 1
                msg = e.msg if e.msg else "unexpected indent"
                
                error_id = f"{error_type}:{lineno}:{msg}"
                if error_id in seen_errors:
                    break
                seen_errors.add(error_id)
                
                error_msg = f"{error_type}: {msg}\n  File \"{filename}\", line {lineno}"
                
                if hasattr(e, 'text') and e.text:
                    error_msg += f"\n    {e.text.rstrip()}"
                    if hasattr(e, 'offset') and e.offset and e.offset > 0:
                        error_msg += f"\n    {' ' * (e.offset - 1)}^"
                
                all_errors.append(error_msg)

                if 0 <= lineno - 1 < len(current_lines):
                    offending_line = current_lines[lineno - 1]
                    if not offending_line.strip().startswith('#'):
                        stripped = offending_line.lstrip()
                        if stripped:
                            indent = offending_line[:len(offending_line) - len(stripped)]
                            current_lines[lineno - 1] = f"{indent}# {stripped}"
                else:
                    break
                    
            except Exception:
                break

    except Exception:
        return []

    return all_errors