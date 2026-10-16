import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import update


def fixture(count='17'):
    return ''.join(
        f'<tr class="gsc_a_tr"><a href="?citation_for_view=dxkSAiwAAAAJ:{pid}">{title}</a>'
        f'<a class="gsc_a_ac gs_ibl" href="?cites={cluster}">{count}</a></tr>'
        for pid, title, cluster in update.PAPERS.values())


class SnapshotTests(unittest.TestCase):
    def test_all_papers_and_zero(self):
        self.assertEqual(len(update.parse(fixture())['papers']), 3)
        self.assertEqual(update.parse(fixture('0'))['papers']['tamer']['count'], 0)

    def test_invalid_pages_leave_last_good_bytes(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parents[2] / 'temp') as directory:
            output = Path(directory) / 'scholar.json'
            update.publish(fixture(), output)
            before = output.read_bytes()
            for invalid in ['captcha', fixture(''), fixture('n/a'), fixture().replace('TAMER', 'Other'),
                            fixture().replace('16049250649077447821', '999'), fixture() + fixture()]:
                with self.assertRaises(ValueError):
                    update.publish(invalid, output)
                self.assertEqual(output.read_bytes(), before)

    def test_atomic_write_failure_keeps_previous(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parents[2] / 'temp') as directory:
            output = Path(directory) / 'scholar.json'
            update.publish(fixture(), output)
            before = output.read_bytes()
            with patch('update.os.replace', side_effect=OSError('simulated')):
                with self.assertRaises(OSError):
                    update.publish(fixture('18'), output)
            self.assertEqual(output.read_bytes(), before)
            self.assertEqual(len(list(Path(directory).iterdir())), 1)


if __name__ == '__main__':
    unittest.main()
