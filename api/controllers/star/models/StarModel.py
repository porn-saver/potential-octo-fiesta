class StarModel:
    name: str
    rank: int
    type: str
    videos: int
    views: str
    verified: bool
    trophy: bool
    url: str
    photo: str

    def __init__(self):
        self.name = None
        self.rank: int = None
        self.type: str = None
        self.videos: int = None
        self.views: str = None
        self.verified: bool = None
        self.trophy: bool = None
        self.url: str = None
        self.photo: str = None

    def checkValues(self):
        return any(value is None for value in vars(self).values())

    def toJson(self):
        return vars(self)
