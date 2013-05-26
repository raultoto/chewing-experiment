#!/usr/bin/env python3
# coding=utf-8

import re

BOPOMOFO = {
    "initial": {
        "literal": "ㄅㄆㄇㄈㄉㄊㄋㄌㄍㄎㄏㄐㄑㄒㄓㄔㄕㄖㄗㄘㄙ",
        "shift": 9,
        "mask": 0x1f,
    },
    "middle": {
        "literal": "ㄧㄨㄩ",
        "shift": 7,
        "mask": 0x3,
    },
    "final": {
        "literal": "ㄚㄛㄜㄝㄞㄟㄠㄡㄢㄣㄤㄥㄦ",
        "shift": 3,
        "mask": 0xf,
    },
    "tone": {
        "literal": "˙ˊˇˋ",
        "shift": 0,
        "mask": 0x7,
    },
}

BOPOMOFO_KEY = ["initial", "middle", "final", "tone"]

BOPOMOFO_REGEX = re.compile(
    "".join(["(?P<{}>[{{}}]?)".format(key) for key in BOPOMOFO_KEY]).format(
        *[BOPOMOFO[key]["literal"] for key in BOPOMOFO_KEY]),
    re.X)


def convert_bopomofo_to_phone_list(bopomofo):
    """This function converts a bopomofo string to phone list

    The bopomofo must be space separated.

    >>> convert_bopomofo_to_phone_list("ㄘㄜˋ ㄕˋ")
    [10268, 8708]
    """

    phone_list = []

    for x in bopomofo.split(" "):
        phone = 0
        m = BOPOMOFO_REGEX.match(x)
        if not m:
            raise Exception("{} is illegal bopomofo".format(x))

        for key in BOPOMOFO.keys():
            if m.group(key):
                phone += ((BOPOMOFO[key]["literal"].find(m.group(key)) + 1) <<
                          BOPOMOFO[key]["shift"])

        phone_list.append(phone)

    return phone_list


def get_partial_phone(phone, key):
    return (phone >> BOPOMOFO[key]["shift"]) & BOPOMOFO[key]["mask"]


def calculate_hamming_distance(x, y):
    """This function calculates Hamming distance of two bopomofo string

    Two bopomofo string shall have the same length.

    >>> calculate_hamming_distance("ㄘㄜˋ ㄕˋ", "ㄘㄜˋ ㄕˋ")
    0

    >>> calculate_hamming_distance("ㄘㄜˋ ㄕˋ", "ㄘㄜ ㄕˋ")
    1

    >>> calculate_hamming_distance("ㄘㄜˋ ㄕˋ", "ㄔㄜˋ ㄙˋ")
    2
    """

    phone_list_x = convert_bopomofo_to_phone_list(x)
    phone_list_y = convert_bopomofo_to_phone_list(y)

    if len(phone_list_x) != len(phone_list_y):
        raise Exception("{} and {} have different lengths".format(x, y))

    hamming_distance = 0
    for i in range(len(phone_list_x)):
        for key in BOPOMOFO_KEY:
            partial_x = get_partial_phone(phone_list_x[i], key)
            partial_y = get_partial_phone(phone_list_y[i], key)
            if partial_x != partial_y:
                hamming_distance += 1
        pass

    return hamming_distance


if __name__ == "__main__":
    import doctest
    doctest.testmod()
