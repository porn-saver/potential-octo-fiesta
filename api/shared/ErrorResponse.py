class ErrorResponse:
    code: int
    message: str

    def __init__(self):
        self.code = 200
        self.message = ''

    def toJson(self):
        return vars(self)
