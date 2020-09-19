from abc import ABC

from muggle.body import Body
from muggle.headofrequest import HeadOfRequest


class Request(HeadOfRequest, Body, ABC):
    pass
