from typing import TypeVar

from muggle.primitives.scalar import Scalar


T = TypeVar('T')


class If(Scalar[T]):
    def __init__(
        self, condition: Scalar[bool],
        if_true,
        if_false,
    ):
        self._scalar: Scalar[bool] = condition
        self._if_true = if_true
        self._if_false = if_false

    async def value(self) -> T:
        if self._scalar.value():
            return await self._if_true.value()
        return await self._if_false.value()
