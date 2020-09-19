class HttpException(Exception):
    def __init__(self, status, *args):
        super(HttpException, self).__init__(*args)
        self._status = status

    def code(self) -> int:
        return self._status
