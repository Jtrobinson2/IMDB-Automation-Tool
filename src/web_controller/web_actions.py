"""Module that contains all of the web actions from logging in to submitting a review that automation tool will need.
"""
from model.review import Review
from util import endpoints
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def login(driver : webdriver.Chrome, username : str, password : str):
    """Logs the user into thier IMDB account.

    Args:
        username (str): the user's name.
        password (str): the user's password.
        driver (webdriver): the web driver to perform the actions

    Raises:
        ValueError: If user name is None or Empty.
        ValueError: If password is None or Empty. 
        ValueError: If the webdriver is None 
    """
    if(not driver):
        raise ValueError("Error: Please Provide a valid driver")
    if(not username):
        raise ValueError("Error: username cannot be null or empty")
    if(not password):
        raise ValueError("Error: password cannot be null or empty")
    
    driver.get(endpoints.LOGIN_PAGE)
    usernameInputField = driver.find_element(By.XPATH, "//*[@id='ap_email']")
    passwordInputField = driver.find_element(By.XPATH, "//*[@id='ap_password']")
    signInButton = driver.find_element(By.ID, "signInSubmit")
    usernameInputField.send_keys(username)
    passwordInputField.send_keys(password)
    signInButton.click()


def isLoggedIn(driver : webdriver) -> bool:
    """Checks if the user is logged into their imdb

    Args:
        driver (webdriver): the web driver to perform the actions

    Returns:
        bool: True if user is logged in

    Raises: 
        ValueError: If the webdriver is None 
    """
    pass 


def submitReview(driver : webdriver, review : Review):
    """Submits a review to a user's IMDB lists and the reviewed item's page

    Args:
        Review (Review): The review to submit 
        driver (webdriver): the web driver to perform the actions

    Raises:
        ValueError: If user name is None or Empty.
        ValueError: If password is None or Empty.
        ValueError: If the driver is None   
    """
    pass


def getCinemaItems(driver : webdriver, cinemaItemTitle : str) -> list[str]:
    """Retrieves a list of cinema items from IMDB given the cinema items title

    Args:
        cinemaItemTitle (str): title of the cinema item your looking for
        driver (webdriver): the web driver to perform the actions 

    Raises:
        ValueError: If cinemaItemTitle is None or Empty.
        ValueError: If the driver is None 
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

def removeFromWatchList(driver : webdriver, cinemaItemTitle : str):
    """Removes a cinema item from the users watchlist

    Args:
        cinemaItemTitle (str): title of cinema item to remove from watch list
        driver (webdriver): the web driver to perform the actions 

    Raises:
        WatchListItemNotFoundError: If cinema item wasn't in the watchlist
        ValueError: If the webdriver is None 
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


