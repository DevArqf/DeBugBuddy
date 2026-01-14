import sys
from pathlib import Path
import pytest

sys.path.insert(0, '.')

from debugbuddy.core.parsers import ErrorParser
from debugbuddy.storage.patterns import PatternManager

def test_java_parser_extracts_type_and_location():
    parser = ErrorParser()
    error_text = (
        'Exception in thread "main" java.lang.NullPointerException: '
        'Cannot invoke "String.length()" because "name" is null\n'
        '\tat com.example.Main.main(Main.java:10)'
    )
    parsed = parser.parse(error_text)
    assert parsed['language'] == 'java'
    assert parsed['type'] == 'NullPointerException'
    assert parsed['file'] == 'Main.java'
    assert parsed['line'] == 10

def test_ruby_parser_extracts_type_and_location():
    parser = ErrorParser()
    error_text = (
        "NoMethodError: undefined method 'name' for nil:NilClass\n"
        "\tfrom app.rb:5:in `main'"
    )
    parsed = parser.parse(error_text)
    assert parsed['language'] == 'ruby'
    assert parsed['type'] == 'NoMethodError'
    assert parsed['file'] == 'app.rb'
    assert parsed['line'] == 5

def test_pattern_manager_loads_java_and_ruby_patterns():
    mgr = PatternManager()
    java_patterns = mgr.load_patterns('java')
    ruby_patterns = mgr.load_patterns('ruby')
    assert any(p.get('type') == 'NullPointerException' for p in java_patterns)
    assert any(p.get('type') == 'NoMethodError' for p in ruby_patterns)

@pytest.mark.parametrize(
    "file_name, expected",
    [
        ("Example.java", "java"),
        ("script.rb", "ruby"),
    ],
)
def test_language_mapping_for_new_extensions(file_name, expected):
    mgr = PatternManager()
    language = mgr.get_language_for_file(Path(file_name))
    assert language == expected
