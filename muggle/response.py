from abc import ABC, abstractmethod

from muggle.body import Body
from muggle.headrq import HeadRs
from muggle.primitives.scalar import Scalar


class Response(HeadRs, Body, ABC):
    @abstractmethod
    def status(self) -> Scalar[str]:
        pass
