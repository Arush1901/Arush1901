import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import living_edition as art


class ContributionDataTests(unittest.TestCase):
    def test_future_calendar_cells_cannot_affect_the_artwork(self):
        html = '''<td data-date="2026-01-01" data-level="2"></td>
        <td data-date="2026-01-02" data-level="4"></td>
        <td data-date="2026-12-31" data-level="4"></td>'''
        self.assertEqual(art.calendar_days(html, date(2026, 1, 2)),
                         {'2026-01-01': 2, '2026-01-02': 4})

    def test_incomplete_calendar_fails_instead_of_overwriting_good_art(self):
        with self.assertRaises(ValueError):
            art.calendar_days('<td data-date="2026-01-01" data-level="4"></td>', date(2026, 1, 2))

    def test_partial_weeks_keep_sunday_alignment(self):
        weeks = art.group_weeks({'2026-01-01': 2, '2026-01-02': 4})
        self.assertEqual(len(weeks), 1)
        self.assertEqual(weeks[0]['start'], '2025-12-28')
        self.assertEqual(weeks[0]['levels'], [0, 0, 0, 0, 2, 4, 0])


if __name__ == '__main__':
    unittest.main()
