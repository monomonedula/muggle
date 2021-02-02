from abc import ABC

from muggle.body import Body
from muggle.headrq import HeadRq


class Request(HeadRq, Body, ABC):
    pass
