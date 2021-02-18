from typing import Callable, Awaitable, Dict, Any

App = Callable[
    [
        Dict[str, Any],
        Callable[[], Awaitable[Dict[str, Any]]],
        Callable[[Dict[str, Any]], Awaitable[None]],
    ],
    Awaitable[None],
]
