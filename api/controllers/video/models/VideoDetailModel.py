from api.controllers.video.models.VideoModel import VideoModel


class VideoDetailModel(VideoModel):
    accurateViews: int
    loaded: str
    uploadDate: str
    likes: str
    accurateLikes: int
    dislikes: str
    accurateDislikes: int
    favorite: str
    author: str
    pornstars: [dict()]
    categories: [str]
    tags: [str]
    production: str

    def __init__(self):
        super().__init__()
        self.accurateLikes = 0
        self.loaded = ''
        self.uploadDate = ''
        self.likes = ''
        self.accurateViews = 0
        self.dislikes = ''
        self.accurateDislikes = 0
        self.favorite = ''
        self.author = ''
        self.pornstars = []
        self.categories = []
        self.tags = []
        self.production = ''
