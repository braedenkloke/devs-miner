import unittest

from devsminer import discover_atomic_devs_of_ms

class ReadFileTest(unittest.TestCase):

    def test_join_logs_on_timestamp(self):
        # Test cases:
        # * log timestamps are the same
        # * log1 timestamp < log2 timestamp
        # * log1 timestamp > log2 timestamp
        # * log1 has the latest timestamp
        log1 = [ [0], [1], [3] ]
        log2 = [ [0], [2] ]

        joined_logs = discover_atomic_devs_of_ms._join_logs_on_timestamp(log1, log2)

        self.assertEqual(4, len(joined_logs))
        self.assertEqual(0, joined_logs[0][0])
        self.assertIsNotNone(joined_logs[0][1])
        self.assertIsNotNone(joined_logs[0][2])
        self.assertEqual(1, joined_logs[1][0])
        self.assertIsNotNone(joined_logs[1][1])
        self.assertIsNone(joined_logs[1][2])
        self.assertEqual(2, joined_logs[2][0])
        self.assertIsNone(joined_logs[2][1])
        self.assertIsNotNone(joined_logs[2][2])
        self.assertEqual(3, joined_logs[3][0])
        self.assertIsNotNone(joined_logs[3][1])
        self.assertIsNone(joined_logs[3][2])

        # Test cases:
        # * log2 has the latest timestamp
        log1 = [ [0] ]
        log2 = [ [1] ]

        joined_logs = discover_atomic_devs_of_ms._join_logs_on_timestamp(log1, log2)

        self.assertEqual(1, joined_logs[1][0])
        self.assertIsNone(joined_logs[1][1])
        self.assertIsNotNone(joined_logs[1][2])


if __name__ == "__main__":
    unittest.main()
