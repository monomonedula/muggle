## Muggle | No magic
An experimental ASGI-compatible object-oriented web framework for Python.
Under development.

This work is heavily inspired by the [Takes](https://github.com/yegor256/takes) framework for Java.



### Quick sample app

Create file `app.py` with the following content:

```python
from muggle.http.app_basic import AppBasic
from muggle.facets.fk.fk_regex import FkRegex
from muggle.facets.fk.mg_fork import MgFork

app = AppBasic(
    MgFork(
        FkRegex(pattern="/home", resp="Hello world!"),
    )
)
```

Run it with an ASGI HTTP Server (Uvicorn, Hypercorn, Daphne, etc.):
```
uvicorn app:app
```

Visit `http://127.0.0.1:8000/home` in your browser.
