from typing import *

T = TypeVar('T')
U = TypeVar('U')

def noop(*args, **kwargs):
    pass

def lmap(f: Callable[[T], U], l: Iterable[T]) -> List[U]:
    return list(map(f, l))
