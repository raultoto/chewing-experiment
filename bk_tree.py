#!/usr/bin/env python3
# coding=utf-8

import lib


class BKTree():
    _MAXIMUM_BOPOMOFO_LEN = 11

    def __init__(self, *, distance_func=lib.calculate_hamming_distance):
        self._distance_func = distance_func
        self._root = {}

        self._counter = {}
        for i in range(1, self._MAXIMUM_BOPOMOFO_LEN + 1):
            self._counter[i] = {
                "insert": 0,
                "node": 0,
            }
        self._latest_query_lookup = 0

    @staticmethod
    def _get_bopomofo_length(bopomofo):
        return len(bopomofo.split(" "))

    def _insert(self, current, bopomofo, length):
        """This function inserts new bopomofo string to BK-tree
        """

        distance = self._distance_func(current["bopomofo"], bopomofo)
        if distance == 0:
            return

        if "children" not in current:
            current["children"] = {}

        if distance in current["children"]:
            self._insert(current["children"][distance], bopomofo, length)
        else:
            current["children"][distance] = {
                "bopomofo": bopomofo,
            }
            self._counter[length]["node"] += 1

    def insert(self, bopomofo_list):
        """Insert bopomofo dictionary to BK-tree
        """

        for bopomofo in bopomofo_list:
            length = self._get_bopomofo_length(bopomofo)
            self._counter[length]["insert"] += 1

            if length in self._root:
                self._insert(self._root[length], bopomofo, length)
            else:
                self._root[length] = {
                    "bopomofo": bopomofo,
                }
                self._counter[length]["node"] += 1

    def _query(self, current, bopomofo, length, threshold):
        result = []

        distance = self._distance_func(current["bopomofo"], bopomofo)
        self._latest_query_lookup += 1
        if distance < threshold:
            result.append({
                "bopomofo": current["bopomofo"],
                "distance": distance,
            })

        for i in range(distance - threshold, distance + threshold + 1):
            if "children" in current and i in current["children"]:
                result.extend(
                    self._query(current["children"][i], bopomofo, length, threshold))

        return result

    def query(self, bopomofo, threshold):
        """This function queries BK-tree with distance threshold

        >>> tree = BKTree()
        >>> tree.insert(["ㄘㄜˋ ㄕˋ", "ㄘㄜ ㄕˋ", "ㄘㄜˋ ㄕ", "ㄘㄜ ㄕ", "ㄔㄜˋ ㄙˋ"])
        >>> len(tree.query("ㄘㄜˋ ㄕˋ", 1))
        1
        >>> len(tree.query("ㄘㄜˋ ㄕˋ", 2))
        3
        >>> len(tree.query("ㄘㄜˋ ㄕˋ", 3))
        5
        >>> len(tree.query("ㄘㄜˋ", 100))
        0
        """

        length = self._get_bopomofo_length(bopomofo)
        self._latest_query_lookup = 0
        if length in self._root:
            return self._query(self._root[length], bopomofo, length, threshold)
        else:
            return []

    def print_statistic(self):
        insert = 0
        node = 0
        for i in range(1, self._MAXIMUM_BOPOMOFO_LEN + 1):
            print("For length {}:".format(i))
            print("\tInsert count is {}".format(self._counter[i]["insert"]))
            print("\tTree node count is {}".format(self._counter[i]["node"]))
            insert += self._counter[i]["insert"]
            node += self._counter[i]["node"]
        print("Total insert count is {}".format(insert))
        print("Total tree node count is {}".format(node))


    def print_latest_query_lookup():
        print("Latest query lookup is {}".format(self._latest_query_lookup))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
