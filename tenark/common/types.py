from typing import Sequence, Union, Tuple, TypeVar

TermTuple = Tuple[str, str, Union[str, int, float, bool, list, tuple]]

QueryDomain = Sequence[Union[str, TermTuple]]

T = TypeVar('T')
