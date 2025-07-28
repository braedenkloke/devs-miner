import unittest

from devsminer import discover_atomic_devs_of_ms, read_file
from math import inf

class DiscoverAtomicDevsOfMSTest(unittest.TestCase):

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
