"""Module that contains all of the web actions from logging in to submitting a review that automation tool will need.
"""
from model.review import Review

def login(username : str, password : str):
    """Logs the user into thier IMDB account.

    Args:
        username (str): the user's name.
        password (str): the user's password.

    Raises:
        ValueError: If user name is None or Empty.
        ValueError: If password is None or Empty.  
    """
    pass


def isLoggedIn() -> bool:
    """Checks if the user is logged into their imdb

    Returns:
        bool: True if user is logged in
    """
    pass 


def submitReview(review : Review):
    """Submits a review to a user's IMDB lists and the reviewed item's page

    Args:
        Review (Review): The review to submit 

    Raises:
        ValueError: If user name is None or Empty.
        ValueError: If password is None or Empty.  
    """
    pass


def getCinemaItems(cinemaItemTitle : str) -> list[str]:
    """Retrieves a list of cinema items from IMDB given the cinema items title

    Args:
        cinemaItemTitle (str): title of the cinema item your looking for 

    Raises:
        ValueError: If cinemaItemTitle is None or Empty.
    """  
    pass

def isReviewValid(review : Review):
    """Checks the fields of a review to ensure they are valid for submission

    Args:
        review (Review): review to verify 

    Raises:
        ValueError: If review's headline is none, empty, or contains profanity or markup.
        ValueError: If review's review body is none, empty, or contains profanity or invalid markup.
        ValueError: If review's not demarked as either a movie or tv show or both.
        ValueError: if reviews review body is < 600 characters
    """  
    pass 

def removeFromWatchList(cinemaItemTitle : str):
    """Removes a cinema item from the users watchlist

    Args:
        cinemaItemTitle (str): title of cinema item to remove from watch list 

    Raises:
        WatchListItemNotFoundError: If cinema item wasn't in the watchlist
    """  
    pass

def removeReviewMarkup(reviewBody : str) -> str:
    """Removes the markup (spoiler tags n such) from a review

    Args:
        reviewBody (str): review body of a review 

    Returns:
        str: cleaned string without markup for review 

    Raises:
        ValueError: If reviewBody is empty or none
    """  
    pass



