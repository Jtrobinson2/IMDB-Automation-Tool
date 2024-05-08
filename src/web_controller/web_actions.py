"""Module that contains all of the web actions from logging in to submitting a review that imdb automation tool 
will need"""

from model.review import Review

def login(username : str, password : str):
    pass

def isLoggedIn() -> bool:
    pass 

def submitReview(review : Review):
    pass

def getCinemaItems(cinemaItemTitle : str) -> list[str]:
    pass

def isReviewValid(review : Review):
    pass 

def removeFromWatchList(cinemaItemTitle : str):
    pass

def removeReviewMarkup(review : str) -> str:
    pass



