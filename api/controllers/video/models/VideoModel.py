class VideoModel:
    title: str
    url: str
    rating: int
    duration: str
    imageUrl: str
    views: str
    userUploadedData: dict()

    def __init__(self):
        self.title = None
        self.url = None
        self.rating = None
        self.duration = None
        self.imageUrl = None
        self.views = None
        self.userUploadedData = None

    def checkValues(self):
        return any(value is None for value in vars(self).values())

    def toJson(self):
        return vars(self)
