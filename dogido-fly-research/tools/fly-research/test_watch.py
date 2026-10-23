import unittest
from datetime import datetime, timedelta, timezone
from watch import classify


class ActivityTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 9, 16, 0, 0, tzinfo=timezone.utc)
        self.row = {'repo': 'example/fly', 'head': 'abc', 'errors': {},
                    'head_date': (self.now - timedelta(days=8)).isoformat(),
                    'pushed_at': (self.now - timedelta(days=8)).isoformat(),
                    'follow_author_on_stale': True, 'owner': {'type': 'User'},
                    'release': None, 'pulls': [], 'archived': False}

    def test_week_of_silence_requests_investigation_not_abandonment(self):
        result = classify(self.row, None, self.now)
        self.assertTrue(result['x_review_due'])
        self.assertEqual(result['activity_assessment'], 'quiet_needs_context')

    def test_fetch_failure_does_not_produce_stale_author_claim(self):
        for lane in ('metadata', 'commits', 'releases'):
            with self.subTest(lane=lane):
                row = dict(self.row, errors={lane: 'HTTP 403'})
                result = classify(row, self.row, self.now)
                self.assertFalse(result['x_review_due'])
                self.assertEqual(result['activity_assessment'], 'unknown')

    def test_branch_push_or_release_counts_as_public_activity(self):
        for update in ({'pushed_at': self.now.isoformat()},
                       {'release': {'published_at': self.now.isoformat()}}):
            with self.subTest(update=update):
                self.assertFalse(classify(dict(self.row, **update), self.row, self.now)['x_review_due'])

    def test_new_head_with_old_commit_date_is_not_stale(self):
        updated = dict(self.row, head='def')
        result = classify(updated, self.row, self.now)
        self.assertIn('head', result['changes'])
        self.assertFalse(result['x_review_due'])
        later = dict(updated, **result)
        self.assertFalse(classify(updated, later, self.now + timedelta(days=3))['x_review_due'])

    def test_verified_author_check_is_not_repeated_every_tick(self):
        recent = {'checked_at': (self.now - timedelta(days=3)).isoformat()}
        self.assertFalse(classify(self.row, self.row, self.now, author_review=recent)['x_review_due'])
        old = {'checked_at': (self.now - timedelta(days=7)).isoformat()}
        self.assertTrue(classify(self.row, self.row, self.now, author_review=old)['x_review_due'])

    def test_organization_is_not_treated_as_single_bored_person(self):
        row = dict(self.row, owner={'type': 'Organization'})
        self.assertFalse(classify(row, self.row, self.now)['x_review_due'])

    def test_initial_baseline_is_not_reported_as_new_progress(self):
        result = classify(self.row, None, self.now)
        self.assertTrue(result['baseline_only'])
        self.assertEqual(result['changes'], [])


if __name__ == '__main__':
    unittest.main()
