import os
from pathlib import Path

def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent

def find_files(pattern: str, root_dir: Path) -> list:
    return [f for f in root_dir.rglob(pattern) if f.is_file()]

def sanitize_filename(filename: str) -> str:
    return re.sub(r'[^\w\-_\.]', '_', filename)

def read_file_content(file_path: Path, max_lines: int = 100) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:max_lines]
            return ''.join(lines)
    except Exception:
        return f"Could not read {file_path}"

def write_to_temp(content: str, extension: str = '.txt') -> Path:
    temp_dir = Path.home() / '.debugbuddy' / 'temp'
    temp_dir.mkdir(exist_ok=True)
    temp_file = temp_dir / f"temp_{int(os.times()[4])}{extension}"
    with open(temp_file, 'w') as f:
        f.write(content)
    return temp_file