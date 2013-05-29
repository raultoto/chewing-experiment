#!/usr/bin/env python3
# coding=utf-8

import lib

from bk_tree import BKTree
from fq_tree import FQTree


def main():
    data = map(lambda x: x["bopomofo"], lib.load_tsi_src())

    bktree = BKTree()
    bktree.insert(data)
    bktree.print_statistic()


if __name__ == "__main__":
    main()
