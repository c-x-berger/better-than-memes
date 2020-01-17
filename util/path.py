import re
from typing import Set

PATH_PART_REGEX = r"([\w\d_]+\.)+[\w\d_]+$"


def is_valid(path: str) -> bool:
    return re.fullmatch(PATH_PART_REGEX, path) is not None


def is_child(parent: str, child: str) -> bool:
    return child.startswith(parent) and parent != child


def children_of(path: str, paths: Set[str]) -> Set[str]:
    ret = set()
    for pa in paths:
        if is_child(path, pa):
            ret.add(pa)
    return ret
