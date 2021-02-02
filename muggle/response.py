from abc import ABC, abstractmethod

from muggle.body import Body
from muggle.headrq import HeadRs


class Response(HeadRs, Body, ABC):
    @abstractmethod
    async def status(self) -> str:
        pass
