#!/usr/bin/env python3
"""Publish validated public Scholar counts atomically; failures preserve old data."""
import argparse
import datetime
import html
import json
import os
from pathlib import Path
import re
import tempfile
import urllib.request

PROFILE = 'https://scholar.google.com/citations?user=dxkSAiwAAAAJ&hl=en&pagesize=100'
PAPERS = {
    'uni_mumer': ('d1gkVwhDpl0C', 'Uni-MuMER', '12883448328760563712'),
    'uni_docrobust': ('qjMakFHDy7sC', 'Uni-DocRobust', '5610418177369708880'),
    'tamer': ('u-x6o8ySG0sC', 'TAMER', '16049250649077447821'),
}


def parse(source):
    papers = {}
    for key, (paper_id, title, cluster) in PAPERS.items():
        rows = [row for row in re.findall(r'<tr\b[^>]*class="gsc_a_tr"[^>]*>(.*?)</tr>', source, re.S)
                if 'citation_for_view=dxkSAiwAAAAJ:' + paper_id in html.unescape(row)]
        if len(rows) != 1 or title.casefold() not in rows[0].casefold():
            raise ValueError('Missing or mismatched paper: ' + key)
        match = re.search(r'<a\b[^>]*class="gsc_a_ac[^"]*"[^>]*>(.*?)</a>', rows[0], re.S)
        if not match:
            raise ValueError('Missing citation field: ' + key)
        value = html.unescape(re.sub('<[^>]+>', '', match[1])).strip()
        if not re.fullmatch(r'[0-9]+', value) or 'cites=' + cluster not in html.unescape(rows[0]):
            raise ValueError('Invalid citation count or cluster: ' + key)
        papers[key] = {'count': int(value)}
    return {'updated_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'papers': papers}


def publish(source, output):
    payload = parse(source)
    output = Path(output)
    with tempfile.NamedTemporaryFile(mode='w', dir=output.parent, prefix='.scholar-', delete=False) as stream:
        temporary = Path(stream.name)
        try:
            json.dump(payload, stream, indent=2)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
            os.chmod(temporary, 0o644)
            os.replace(temporary, output)
        finally:
            temporary.unlink(missing_ok=True)
    return payload


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    request = urllib.request.Request(PROFILE, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read(2_000_001)
        if len(body) > 2_000_000:
            raise ValueError('Unexpected profile size')
        source = body.decode(response.headers.get_content_charset() or 'utf-8')
    result = publish(source, args.output)
    print('Updated:', {key: value['count'] for key, value in result['papers'].items()})
