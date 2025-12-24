import re
from typing import Dict, Optional
from .base import BaseParser

class PythonParser(BaseParser):
    language = 'python'

    PATTERNS = {
        'traceback': re.compile(r'Traceback \(most recent call last\):.*?(\w+Error.*?)(?:\n|$)', re.DOTALL),
        'error_line': re.compile(r'(\w+Error): (.+)'),
        'syntax_error': re.compile(r'SyntaxError: (.+)'),
        'name_error': re.compile(r'NameError: name \'([^\']+)\' is not defined'),
        'type_error': re.compile(r'TypeError: (.+)'),
        'attribute_error': re.compile(r'AttributeError: (.+)'),
        'import_error': re.compile(r'(ImportError|ModuleNotFoundError): (.+)'),
        'index_error': re.compile(r'IndexError: (.+)'),
        'key_error': re.compile(r'KeyError: (.+)'),
        'value_error': re.compile(r'ValueError: (.+)'),
    }

    def parse(self, text: str) -> Optional[Dict]:
        result = {
            "raw": text,
            "type": "Unknown Error",
            "message": text.strip(),
            "file": None,
            "line": None,
            "language": "python"
        }

        file_match = re.search(r'File "([^"]+)", line (\d+)', text)
        if file_match:
            result['file'] = file_match.group(1)
            result['line'] = int(file_match.group(2))

        if 'NameError' in text and 'name' in text and 'is not defined' in text:
            name_match = re.search(r"name ['\"]([^'\"]+)['\"] is not defined", text)
            if name_match:
                result['type'] = 'Name Error'
                result['message'] = f"name '{name_match.group(1)}' is not defined"
                return result
        
        if 'TypeError:' in text:
            type_match = re.search(r'TypeError: (.+)', text)
            if type_match:
                result['type'] = 'Type Error'
                result['message'] = type_match.group(1).strip()
                return result
        
        if 'IndexError:' in text:
            index_match = re.search(r'IndexError: (.+)', text)
            if index_match:
                result['type'] = 'Index Error'
                result['message'] = index_match.group(1).strip()
                return result
        
        if 'KeyError:' in text:
            key_match = re.search(r'KeyError: (.+)', text)
            if key_match:
                result['type'] = 'Key Error'
                result['message'] = key_match.group(1).strip()
                return result
        
        if 'SyntaxError:' in text:
            syntax_match = re.search(r'SyntaxError: (.+)', text)
            if syntax_match:
                result['type'] = 'Syntax Error'
                result['message'] = syntax_match.group(1).strip()
                return result
        
        if 'AttributeError:' in text:
            attr_match = re.search(r'AttributeError: (.+)', text)
            if attr_match:
                result['type'] = 'Attribute Error'
                result['message'] = attr_match.group(1).strip()
                return result
        
        if 'ImportError:' in text or 'ModuleNotFoundError:' in text:
            import_match = re.search(r'(ImportError|ModuleNotFoundError): (.+)', text)
            if import_match:
                result['type'] = 'Import Error' if 'ImportError' in text else 'Module Not Found Error'
                result['message'] = import_match.group(2).strip()
                return result
        
        if 'ValueError:' in text:
            value_match = re.search(r'ValueError: (.+)', text)
            if value_match:
                result['type'] = 'Value Error'
                result['message'] = value_match.group(1).strip()
                return result

        error_match = re.search(r'(\w+Error): (.+)', text)
        if error_match:
            error_type = error_match.group(1)
            if error_type.endswith('Error'):
                base = error_type[:-5]
                spaced = re.sub(r'([A-Z])', r' \1', base).strip()
                result['type'] = f"{spaced} Error"
            else:
                result['type'] = error_type
            result['message'] = error_match.group(2).strip()
            return result

        return result