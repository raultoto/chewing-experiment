#!/usr/bin/env python3
# coding=utf-8

import lib


class BKTree():
    def __init__(self, *, distance_func=lib.calculate_hamming_distance):
        self._distance_func = distance_func
        self._root = {}

    @staticmethod
    def _get_bopomofo_length(bopomofo):
        return len(bopomofo.split(" "))

    def _insert(self, current, bopomofo):
        """This function inserts new bopomofo string to BK-tree
        """

        distance = self._distance_func(current["bopomofo"], bopomofo)
        if distance == 0:
            return

        if "children" not in current:
            current["children"] = {}

        if distance in current["children"]:
            self._insert(current["children"][distance], bopomofo)
        else:
            current["children"][distance] = {
                "bopomofo": bopomofo,
            }

    def insert(self, bopomofo_list):
        """Insert bopomofo dictionary to BK-tree
        """

        for bopomofo in bopomofo_list:
            length = self._get_bopomofo_length(bopomofo)

            if length in self._root:
                self._insert(self._root[length], bopomofo)
            else:
                self._root[length] = {
                    "bopomofo": bopomofo,
                }

    def query(self, bopomofo, threshold):
        """This function queries BK-tree with distance threshold

        >>> tree = BKTree()
        >>> tree.insert(["ㄘㄜˋ ㄕˋ", "ㄘㄜ ㄕˋ", "ㄘㄜˋ ㄕ", "ㄘㄜ ㄕ", "ㄔㄜˋ ㄙˋ"])
        >>> tree.query("ㄘㄜˋ ㄕˋ", 1) == [
        ... {'bopomofo': 'ㄘㄜˋ ㄕˋ', 'distance': 0}
        ... ]
        True
        >>> tree.query("ㄘㄜˋ ㄕˋ", 2) == [
        ... {'bopomofo': 'ㄘㄜˋ ㄕˋ', 'distance': 0},
        ... {'bopomofo': 'ㄘㄜ ㄕˋ', 'distance': 1},
        ... {'bopomofo': 'ㄘㄜˋ ㄕ', 'distance': 1},
        ... ]
        True
        >>> tree.query("ㄘㄜˋ ㄕˋ", 3) == [
        ... {'bopomofo': 'ㄘㄜˋ ㄕˋ', 'distance': 0},
        ... {'bopomofo': 'ㄘㄜ ㄕˋ', 'distance': 1},
        ... {'bopomofo': 'ㄘㄜˋ ㄕ', 'distance': 1},
        ... {'bopomofo': 'ㄘㄜ ㄕ', 'distance': 2},
        ... {'bopomofo': 'ㄔㄜˋ ㄙˋ', 'distance': 2},
        ... ]
        True
        >>> tree.query("ㄘㄜˋ", 100) == []
        True
        """

        def _query(current):
            result = []

            distance = self._distance_func(current["bopomofo"], bopomofo)
            if distance < threshold:
                result.append({
                    "bopomofo": current["bopomofo"],
                    "distance": distance,
                })

            for i in range(distance - threshold, distance + threshold + 1):
                if "children" in current and i in current["children"]:
                    result.extend(_query(current["children"][i]))

            return result

        length = self._get_bopomofo_length(bopomofo)
        if length in self._root:
            return _query(self._root[length])
        else:
            return []


if __name__ == "__main__":
    import doctest
    doctest.testmod()
