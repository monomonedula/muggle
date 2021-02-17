## Muggle | No magic
An experimental WSGI-compatible object-oriented web framework for Python.
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

Run it with a WSGI HTTP Server (Gunicorn, uWSGI, etc.):
```
gunicorn app:app
```

Visit `http://127.0.0.1:8000/home` in your browser.
