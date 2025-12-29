import sys
sys.path.insert(0, '.')

from debugbuddy.core.parsers import ErrorParser

test_cases = [
    "NameError: name 'x' is not defined",
    "NameError: name 'user_id' is not defined",
    "TypeError: unsupported operand type(s) for +",
    "IndexError: list index out of range",
    "KeyError: 'missing_key'",
]

parser = ErrorParser()

print("="*60)
print("PARSER DEBUG TEST")
print("="*60)

for i, error_text in enumerate(test_cases, 1):
    print(f"\nTest {i}:")
    print(f"Input:  {error_text}")
    
    result = parser.parse(error_text)
    
    print(f"Type:   {result.get('type')}")
    print(f"Msg:    {result.get('message')}")
    print(f"Lang:   {result.get('language')}")
    
    if result.get('type') == 'Unknown Error':
        print("❌ FAILED - Got 'Unknown Error'")
    else:
        print("✅ PASSED")

print("\n" + "="*60)
print("If any tests show 'Unknown Error', the parser needs fixing")
print("="*60)