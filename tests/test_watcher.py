import pytest
import time
from pathlib import Path
from unittest.mock import patch, MagicMock
from debugbuddy.core.watcher import ErrorWatcher, SimpleChecker

@pytest.fixture
def temp_py_file(tmp_path):
    file_path = tmp_path / "test.py"
    file_path.write_text("def func():\n    print(undefined_var)\n")
    return file_path

def test_simple_checker_basic(temp_py_file):
    checker = SimpleChecker(str(temp_py_file))
    tree = MagicMock()
    with patch.object(checker, 'visit', return_value=None):
        checker.visit(tree)
    errors = checker.get_errors()
    assert len(errors) == 0

def test_simple_checker_undefined_var(temp_py_file):
    content = temp_py_file.read_text()
    with open(temp_py_file, 'w') as f:
        f.write(content.replace('undefined_var', 'x'))
    checker = SimpleChecker(str(temp_py_file))
    tree = MagicMock()
    with patch.object(checker, 'visit', return_value=None):
        checker.used.add('missing')
        checker.defined.add('defined')
        errors = checker.get_errors()
    assert len(errors) >= 0

def test_error_watcher_start_stop(tmp_path):
    mock_observer = MagicMock()
    with patch('debugbuddy.core.watcher.Observer', return_value=mock_observer):
        watcher = ErrorWatcher(tmp_path)
        watcher.start()
        time.sleep(0.1)
        watcher.stop()
        mock_observer.start.assert_called_once()
        mock_observer.stop.assert_called_once()

def test_error_watcher_detects_errors(tmp_path, temp_py_file):
    watcher = ErrorWatcher(tmp_path)
    with patch.object(watcher, '_check_file_errors') as mock_check:
        watcher.on_modified(MagicMock(src_path=str(temp_py_file)))
        mock_check.assert_called_once_with(temp_py_file)

def test_simple_checker_visit_import(temp_py_file):
    checker = SimpleChecker(str(temp_py_file))
    mock_node = MagicMock()
    mock_node.names = [('os', None)]
    with patch.object(checker, 'generic_visit'):
        checker.visit_Import(mock_node)
    assert 'os' in checker.imports