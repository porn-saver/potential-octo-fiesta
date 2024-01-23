class ErrorResponse:

    def __init__(self, code=200, msg: str = None):
        self.code = code
        self.message = msg

    def toJson(self):
        return vars(self)
