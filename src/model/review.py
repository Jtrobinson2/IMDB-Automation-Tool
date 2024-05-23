"""Popo class that encapsulates all the fields of a review"""
class Review:
    #TODO decide if you want a user class and a user has reviews and links to there lists
    def __init__(self, headline : str, reviewBody : str, isTVShow : bool, isMovie : bool, containsSpoilers : bool = True):
        self.headline = headline
        self.reviewBody = reviewBody
        self.isTVShow = isTVShow
        self.isMovie = isMovie
        self.containsSpoilers = containsSpoilers
