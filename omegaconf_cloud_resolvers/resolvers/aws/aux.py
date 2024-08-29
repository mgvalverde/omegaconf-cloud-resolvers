import ast
from typing import Any


def try_infer_and_cast(val: Any) -> Any:
    """
    Tries to cast a value to an integet, float or string

    Args:
        val (any): The value to be cast.

    Returns:
        any: Cast value

    Example:
    ```python
    >>> try_infer_and_cast("1")       # 1    # int
    >>> try_infer_and_cast("1.0")     # 1.0  # float
    >>> try_infer_and_cast("1a")      # '1a' # str
    >>> try_infer_and_cast("False")   # False # bool
    ```
    """
    if isinstance(val, str):
        if val.strip() in {"True", "true"}:
            return True
        if val.strip() in {"False", "false"}:
            return False

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
    Args:
        val (any): The value to be cast.

    Returns:
        any: Cast value

    Example:
    ```python
    >>> try_cast_to_dict('{"user": "userA", "password": "ad2as9dua@das/*asd/*1", "age": 30}')    #  dict
    >>> try_cast_to_dict("random/string@1")           #  str
    ```
    """

    if isinstance(val, str):
        val_ = val.strip()
        if val_[0] + val_[-1] == "{}":
            try:
                return ast.literal_eval(val)
            except Exception:
                return val
    return val
