from typing import Any


def try_cast_to_number(val: Any) -> Any:
    """
    Tries to cast a value to an integet, float or string
    Example:
    >>> try_cast_to_number("1")    # 1    int
    >>> try_cast_to_number("1.0")  # 1.0  float
    >>> try_cast_to_number("1a")   # '1a' str

    :param val:
    :return:
    """
    try:
        return int(val)
    except ValueError:
        try:
            return float(val)
        except ValueError:
            return val
