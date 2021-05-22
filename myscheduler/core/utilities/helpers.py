from typing import Any
from typing import Optional


def safe_list_get(list_: list, index: int, default: Optional[Any] = None) -> Any:
    """
    A function to safely retrieve a list entry,
    retuning `None` as a default value.
    """
    try:
        return list_[index]
    except IndexError:
        return default
