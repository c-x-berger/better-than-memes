import re

PATH_PART_REGEX = r"([\w\d_]+\.)+[\w\d_]+$"


def is_valid(path: str) -> bool:
    return re.fullmatch(PATH_PART_REGEX, path) is not None


def parent_of(path: str) -> str:
    return ".".join(path.split(".")[:-1])
