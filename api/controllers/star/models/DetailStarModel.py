from api.controllers.star.models.StarModel import StarModel


class DetailStarModel(StarModel):
    subscribers: str
    posterPhoto: str
    bio: str
    socialMedia: dict()
    personalInfo: dict()

    def __init__(self):
        super().__init__()
        self.subscribers = ''
        self.posterPhoto = None
        self.bio = ''
        self.socialMedia = None
        self.personalInfo = None
        self.videos = ''
