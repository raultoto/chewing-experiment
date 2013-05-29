#!/usr/bin/env python3
# coding=utf-8

import lib


class FQTree():
    _MAXIMUM_BOPOMOFO_LEN = 11
    _BUCKET_SIZE = 1

    def __init__(self, *, distance_func=lib.calculate_hamming_distance):
        self._distance_func = distance_func
        self._root = {}

        self._counter = {}
        for i in range(1, self._MAXIMUM_BOPOMOFO_LEN + 1):
            self._counter[i] = {
                "insert": 0,
                "internal": 0,
                "leaf": 0,
            }
        self._latest_query_lookup = 0

    @staticmethod
    def _get_bopomofo_length(bopomofo):
        return len(bopomofo.split(" "))

    @staticmethod
    def _is_internal_node(node):
        return "children" in node

    @staticmethod
    def _is_leaf_node(node):
        return "bopomofo" in node

    def _change_to_internal_node(self, node, length):
        del node["bopomofo"]
        node["children"] = {}
        self._counter[length]["internal"] += 1
        self._counter[length]["leaf"] -= 1

    def _insert(self, current, root, depth, bopomofo, length):
        """This function inserts new bopomofo string to FQ-tree
        """

        if self._is_internal_node(current):
            distance = self._distance_func(
                root["key"][depth], bopomofo)
            if distance in current["children"]:
                self._insert(
                    current["children"][distance], root, depth + 1, bopomofo, length)
            else:
                current["children"][distance] = {
                    "bopomofo": [bopomofo],
                }
                self._counter[length]["leaf"] -= 1

        elif self._is_leaf_node(current):
            if len(current["bopomofo"]) < self._BUCKET_SIZE:
                current["bopomofo"].append(bopomofo)
            else:
                bopomofo_list = current["bopomofo"]
                bopomofo_list.append(bopomofo)

                self._change_to_internal_node(current, length)

                if len(root["key"]) < depth + 1:
                    root["key"].append(bopomofo)

                for item in bopomofo_list:
                    self._insert(current, root, depth, item, length)
        else:
            assert False, "Unknown node"

    def insert(self, bopomofo_list):
        """Insert bopomofo dictionary to FQ-tree
        """
        for bopomofo in bopomofo_list:
            length = self._get_bopomofo_length(bopomofo)
            self._counter[length]["insert"] += 1

            if length in self._root:
                self._insert(
                    self._root[length], self._root[length], 0, bopomofo, length)
            else:
                self._root[length] = {
                    "key": [bopomofo],
                    "children": {
                        0: {
                            "bopomofo": [bopomofo],
                        },
                    },
                }
                self._counter[length]["internal"] += 1
                self._counter[length]["leaf"] += 1

    def _query(self, current, root, depth, bopomofo, length, threshold):
        result = []

        if self._is_internal_node(current):
            distance = self._distance_func(bopomofo, root["key"][depth])
            self._latest_query_lookup += 1
            for i in range(distance - threshold, distance + threshold + 1):
                if "children" in current and i in current["children"]:
                    result.extend(self._query(current["children"][i], root, depth + 1, bopomofo, length, threshold))
        elif self._is_leaf_node(current):
            for candidate in current["bopomofo"]:
                distance = self._distance_func(candidate, bopomofo)
                self._latest_query_lookup += 1
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
        self._latest_query_lookup = 0

        if length in self._root:
            return self._query(self._root[length], self._root[length], 0, bopomofo, length, threshold)
        else:
            return []

    def print_statistic(self):
        insert = 0
        internal = 0
        leaf = 0

        print("Bucket size is {}".format(self._BUCKET_SIZE))
        for i in range(1, self._MAXIMUM_BOPOMOFO_LEN + 1):
            print("For length {}:".format(i))
            print("\tInsert count is {}".format(self._counter[i]["insert"]))
            print("\tinternal node count is {}".format(self._counter[i]["internal"]))
            print("\tleaf node count is {}".format(self._counter[i]["leaf"]))
            insert += self._counter[i]["insert"]
            internal += self._counter[i]["internal"]
            leaf += self._counter[i]["leaf"]
        print("Total insert count is {}".format(insert))
        print("Total internal node count is {}".format(internal))
        print("Total leaf node count is {}".format(leaf))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
