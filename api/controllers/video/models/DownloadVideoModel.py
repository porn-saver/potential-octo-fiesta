class DownloadVideoModel:
    url: str
    aspectRatio: float
    ext: str
    format: str
    height: int
    resolution: str

    def __init__(self):
        self.url = ''
        self.aspectRatio = 0
        self.ext = ''
        self.format = ''
        self.height = 0
        self.resolution = ''

    def toJson(self):
        return vars(self)
