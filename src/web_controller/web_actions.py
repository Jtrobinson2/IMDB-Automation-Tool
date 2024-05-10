"""Module that contains all of the web actions from logging in to submitting a review that automation tool will need.
"""
from model.review import Review
from util import endpoints
from selenium import webdriver
from model.login_error import LoginError
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def login(driver : webdriver, accountUsername : str, password : str, username : str):
    """Logs the user into their IMDB account.

    Args:
        accountUsername (str): the username of the account (email phone number etc, used to login).
        password (str): the user's account password.
        username (str): the username of the imdb profile (post login).
        driver (webdriver): the web driver to perform the actions

    Raises:
        ValueError: If accountUsername is None or Empty.
        ValueError: If username is None or Empty.
        ValueError: If password is None or Empty. 
        ValueError: If the webdriver is None
        ValueError: If the login failed for any reason 
    """
    if(not driver):
        raise ValueError("Error: Please Provide a valid driver")
    if(not username):
        raise ValueError("Error: username cannot be null or empty")
    if(not accountUsername):
        raise ValueError("Error: account username cannot be null or empty")
    if(not password):
        raise ValueError("Error: password cannot be null or empty")
    
    driver.get(endpoints.LOGIN_PAGE)
    usernameInputField = driver.find_element(By.XPATH, "//*[@id='ap_email']")
    passwordInputField = driver.find_element(By.XPATH, "//*[@id='ap_password']")
    signInButton = driver.find_element(By.ID, "signInSubmit")
    sendKeysLikeHuman(accountUsername, driver, usernameInputField)
    sendKeysLikeHuman(password, driver, passwordInputField)
    signInButton.click()

    #check that the login didn't fail
    try:
        loginErrorElement = driver.find_element(By.CLASS_NAME, "a-list-item")
        raise LoginError(f"Error logging in: {loginErrorElement.text}")
    except NoSuchElementException:
        #check if IMDB detected you as a bot despite a successful login
        try:
            #this element only appears if imdb thinks your a bot
            driver.find_element(By.CLASS_NAME, "a-size-large")
            raise LoginError(f"Error logging in you must login manually")
        except NoSuchElementException:
            #make sure we're logged into the correct user
            loggedInUserElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='imdbHeader']/div[2]/div[5]/div/label[2]/span/span")))
            #this should never happen unless the user gives the wrong username
            assert loggedInUserElement.text == username


def isLoggedIn(driver : webdriver) -> bool:
    """Checks if the user is logged into their imdb

    Args:
        driver (webdriver): the web driver to perform the actions

    Returns:
        bool: True if user is logged in

    Raises: 
        ValueError: If the webdriver is None 
    """
    if(not driver):
        raise ValueError("Error: Please Provide a valid driver")
    
    try:
        driver.get(endpoints.IMDB_HOME_PAGE)
        driver.find_element(By.XPATH, "//*[@id='imdbHeader']/div[2]/div[5]/div/label[2]/span/span")
        return True
    except NoSuchElementException:
        return False
    



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


def sendKeysLikeHuman(keys : str, driver : webdriver, inputElement : WebElement):
    """Sends keys to an input field in a human like way to avoid websites bot detection

    Args:
        keys (str): keys to send
        driver (webdriver): web driver to execute the action
        inputElement (WebElement): the input field  

    Raises:
        ValueError: If keys are empty or none
        ValueError: If webDriver is none
        ValueError: If inputElement is none
    """  

    if(not keys):
        raise ValueError("Error: you must submit something for the keys")
    if(not driver):
        raise ValueError("Error: you must provide a web driver")
    if(not inputElement):
        raise ValueError("Error: you must provide the the input element")

    #move to the input element in a human way before sending the keys
    actions = ActionChains(driver)
    actions.move_to_element_with_offset(inputElement, int(random.uniform(1,3)), int(random.uniform(1,3)))
    actions.click()
    actions.perform()

    #mimics a human pause between keystrokes
    for character in keys:
        actions.send_keys(character)
        actions.perform()
        time.sleep(random.uniform(0.1,0.2))

    




