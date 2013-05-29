#!/usr/bin/env python3
# coding=utf-8

import lib


class FQTree():
    _BUCKET_SIZE = 1

    def __init__(self, *, distance_func=lib.calculate_hamming_distance):
        self._distance_func = distance_func
        self._root = {}

    @staticmethod
    def _get_bopomofo_length(bopomofo):
        return len(bopomofo.split(" "))

    @staticmethod
    def _is_internal_node(node):
        return "children" in node

    @staticmethod
    def _is_leaf_node(node):
        return "bopomofo" in node

    @staticmethod
    def _change_to_internal_node(node):
        del node["bopomofo"]
        node["children"] = {}

    def _insert(self, current, root, depth, bopomofo):
        """This function inserts new bopomofo string to FQ-tree
        """

        if self._is_internal_node(current):
            distance = self._distance_func(
                root["key"][depth], bopomofo)
            if distance in current["children"]:
                self._insert(
                    current["children"][distance], root, depth + 1, bopomofo)
            else:
                current["children"][distance] = {
                    "bopomofo": [bopomofo],
                }

        elif self._is_leaf_node(current):
            if len(current["bopomofo"]) < self._BUCKET_SIZE:
                current["bopomofo"].append(bopomofo)
            else:
                bopomofo_list = current["bopomofo"]
                bopomofo_list.append(bopomofo)

                self._change_to_internal_node(current)

                if len(root["key"]) < depth + 1:
                    root["key"].append(bopomofo)

                for item in bopomofo_list:
                    self._insert(current, root, depth, item)
        else:
            assert False, "Unknown node"

    def insert(self, bopomofo_list):
        """Insert bopomofo dictionary to FQ-tree
        """
        for bopomofo in bopomofo_list:
            length = self._get_bopomofo_length(bopomofo)

            if length in self._root:
                self._insert(
                    self._root[length], self._root[length], 0, bopomofo)
            else:
                self._root[length] = {
                    "key": [bopomofo],
                    "children": {
                        0: {
                            "bopomofo": [bopomofo],
                        },
                    },
                }

    def _query(self, current, root, depth, bopomofo, length, threshold):
        result = []

        if self._is_internal_node(current):
            distance = self._distance_func(bopomofo, root["key"][depth])
            for i in range(distance - threshold, distance + threshold + 1):
                if "children" in current and i in current["children"]:
                    result.extend(self._query(current["children"][i], root, depth + 1, bopomofo, length, threshold))
        elif self._is_leaf_node(current):
            for candidate in current["bopomofo"]:
                distance = self._distance_func(candidate, bopomofo)
                if distance < threshold:
                    result.append({
                        "bopomofo": candidate,
                        "distance": distance,
                    })
        else:
            assert False, "Unknown node"

        return result

    def query(self, bopomofo, threshold):
        """This function queries FQ-tree with distance threshold

        >>> tree = FQTree()
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

        if length in self._root:
            return self._query(self._root[length], self._root[length], 0, bopomofo, length, threshold)
        else:
            return []


if __name__ == "__main__":
    import doctest
    doctest.testmod()
