from collections.abc import Collection
from dataclasses import dataclass

@dataclass
class IRange:
    start : int
    end   : int

def into_irange(*args, **kwargs):
    if len(args) == 1:
        r = args[0]
        if isinstance(r, IRange):
            return r
        elif isinstance(r, (tuple, list, Collection)) and len(r) == 2:
            return IRange(*r)
        elif isinstance(r, dict):
            return IRange(**r)
    elif len(args) == 0:
        return IRange(**kwargs)