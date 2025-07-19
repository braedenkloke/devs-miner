"""Functions for reading files.
"""

import csv

def read_csv(filepath, delimiter=","):
    """Returns a list of where each element is a row from a CSV file.

    >>> data = read_csv("books_sorted_by_author.csv")
    >>> print(data)
    [ 
        [The Little Mermaid, The Steadfast Tin Soldier, The Elder-Tree Mother], 
        [The Jungle Book],
        [Matilda, Charlie and the Chocolate Factory]
    ]
    """
    data = []
    with open(filepath, 'r', newline='') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            data.append(row)
    return data

