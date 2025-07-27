import unittest

from devsminer import discover_atomic_devs_of_ms, read_file
from math import inf

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

    def test_execute(self):
        event_log = read_file.read_csv("tests/input_data/event_log_1.csv")
        state_log = read_file.read_csv("tests/input_data/state_log_1.csv")
        X, Y, S, ta, ext_trans, int_trans, output = discover_atomic_devs_of_ms.execute(event_log, state_log)

        self.assertTrue("enter" in X)
        self.assertTrue("end" in Y)
        self.assertTrue("idle" in S)
        self.assertTrue("busy" in S)

        self.assertEqual(2, len(ta))
        counter = 0
        for m in ta:
            if m[0] == "idle":
                self.assertEqual(inf, m[1])
                counter += 1
            elif m[0] == "busy":
                self.assertEqual(5, m[1])
                counter += 1
        self.assertEqual(len(ta), counter) # checked all mappings

        self.assertEqual(1, len(ext_trans))
        counter = 0
        for m in ext_trans:
            if m[0][0] == "idle":
                self.assertEqual("enter", m[0][1])
                self.assertEqual("busy", m[1])
                counter += 1
        self.assertEqual(len(ext_trans), counter) # checked all mappings

        self.assertEqual(1, len(int_trans))
        counter = 0
        for m in int_trans:
            if m[0] == "busy":
                self.assertEqual("idle", m[1])
                counter += 1
        self.assertEqual(len(int_trans), counter) # checked all mappings

        self.assertEqual(1, len(output))
        counter = 0
        for m in output:
            if m[0] == "busy":
                self.assertEqual("end", m[1])
                counter += 1
        self.assertEqual(len(output), counter) # checked all mappings

if __name__ == "__main__":
    unittest.main()
