# import yaml
import ast
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


def try_cast_to_dict(val: Any) -> Any:
    """
    Try to case a dict-like string into a dictionary, if not possible, returns the input value.

    >>> try_cast_to_dict('{"user": "userA", "password": "ad2as9dua@das/*asd/*1", "age": 30}')    #  dict
    >>> try_cast_to_dict("random/string@1")           #  str
    """

    if isinstance(val, str):
        val_ = val.strip()
        if val_[0] + val_[-1] == "{}":
            try:
                return ast.literal_eval(val)
                # NOTE: would it be more secure to do `import yaml; yaml.safe_load(val), but it produces some artifacts
                #  in some scenarios
            except Exception:
                pass
    return val
