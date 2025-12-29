import json
import gzip

def compress_patterns():
    pattern_dir = Path('patterns')
    for pattern_file in pattern_dir.glob('*.json'):
        with open(pattern_file, 'r') as f:
            data = json.load(f)

        minified = json.dumps(data, separators=(',', ':'))

        compressed_path = pattern_file.with_suffix('.json.gz')
        with gzip.open(compressed_path, 'wt') as f:
            f.write(minified)