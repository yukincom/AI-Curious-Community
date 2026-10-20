import unittest
from analyze import sustained_start

class DecayDetectionTest(unittest.TestCase):
    def test_observation_censored_not_invented_stop(self):
        self.assertIsNone(sustained_start([134]*60,1))
    def test_brief_dip_does_not_count(self):
        self.assertIsNone(sustained_start([100,0,0,0,0,100],1))
    def test_returns_start_not_end_of_confirming_interval(self):
        self.assertEqual(sustained_start([100,100,1,1,0,0,0],1),2)
    def test_incomplete_confirmation_is_censored(self):
        self.assertIsNone(sustained_start([100,0,0,0],1))

if __name__=='__main__':unittest.main()
