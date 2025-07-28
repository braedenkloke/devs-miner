import unittest

from devsminer import io

class IOTest(unittest.TestCase):

    def test_read_csv(self):
        books = io.read_csv("tests/input_data/books_sorted_by_author.csv")

        self.assertEqual(3, len(books))
        self.assertEqual("The Little Mermaid", books[0][0])
        self.assertEqual("The Steadfast Tin Soldier", books[0][1])
        self.assertEqual("The Elder-Tree Mother", books[0][2])
        self.assertEqual("The Jungle Book", books[1][0])
        self.assertEqual("Matilda", books[2][0])
        self.assertEqual("Charlie and the Chocolate Factory", books[2][1])


if __name__ == "__main__":
    unittest.main()
