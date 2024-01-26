class DownloadVideoModel:
    url: str
    manifestUrl: str
    aspectRatio: float
    ext: str
    format: str
    fps: float
    height: int
    width: int
    resolution: str

    def __init__(self):
        self.url = ''
        self.manifestUrl = ''
        self.aspectRatio = 0
        self.ext = ''
        self.format = ''
        self.fps = 0
        self.width = 0
        self.height = 0
        self.resolution = ''

    def toJson(self):
        return vars(self)
