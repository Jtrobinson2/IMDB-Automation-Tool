"""Module that contains all of the web actions from logging in to submitting a review that automation tool will need.
"""
from model.review import Review
from model import watchlist_item_not_found_error
from util import endpoints
from selenium import webdriver
from model.login_error import LoginError
from selenium.common.exceptions import TimeoutException
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



def removeFromWatchList(driver : webdriver.Chrome, cinemaItemTitle : str) -> bool :
    """Removes a cinema item from the users watchlist

    Args:
        cinemaItemTitle (str): title of cinema item to remove from watch list
        driver (webdriver): the web driver to perform the actions 

    Returns:
        bool: if item was able to be removed from watchlist

    Raises:
        WatchListItemNotFoundError: If cinema item wasn't in the watchlist
        ValueError: If the webdriver is None 
        ValueError: If user is not logged in
        Exception: If an incompatible version of the IMDB website was returned on startup
          
    """  
    if(not driver):
        raise ValueError("Error: provide a valid driver")
    if(not isLoggedIn(driver)):
        raise ValueError("Error: nobody is logged in cannot remove from watchlist.")

    #resolves lots of issues with dom elements not being ready when find element is called
    driver.implicitly_wait(5)

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='imdbHeader']/div[2]/div[4]/a/span/span")))
    except Exception:
        raise TimeoutError("Error: the web element that contains the watchlist didn't load for some reason")

    watchListSizeText = driver.find_element(By.XPATH, "//*[@id='imdbHeader']/div[2]/div[4]/a/span/span").get_attribute("innerHTML")
    watchListSizePrior = int(watchListSizeText)
    watchlistSizeNow = watchListSizePrior
    watchListHyperLink = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[@id='imdbHeader']/div[2]/div[4]/a"))).get_attribute("href")
    driver.get(watchListHyperLink)

    #actions to be used when watchlist removal takes place
    actions = ActionChains(driver)

    #two different versions of the imdb website we have to have logic for removing from watchlist
    try:
        #if we get this version of the watchlist page do this algorithmn
        if(WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[@id='styleguide-v2']")))):
            print("V2 SITE VERSION SPOTTED")
        
        watchListItems = driver.find_elements(By.CLASS_NAME, "lister-item-header")
        assert(3 == len(watchListItems))

        for index, item in enumerate(watchListItems):
            if(cinemaItemTitle in item.text):
                print(f"found {cinemaItemTitle} on index {index} in v2 site")
                #css selector for each watch list item ribbon changes based on the cinema item's positon in the watchlist
                watchListRemoveButton = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, f"#center-1-react > div > div:nth-child(3) > div > div:nth-child({index + 1}) > div > div.lister-item-image > div")))
                actions.move_to_element_with_offset(watchListRemoveButton, int(random.uniform(1,3)), int(random.uniform(1,3)))
                actions.click()
                actions.perform()
                print("remove from watchlist button clicked in v2 version")                
                #need to re-find this element because if you don't you'll get a stale element exception even though it's still in the dom??
                driver.refresh()
                watchlistSizeNow = int(driver.find_element(By.XPATH, "//*[@id='imdbHeader']/div[2]/div[4]/a/span/span").get_attribute("innerHTML"))
                assert(watchListSizePrior - 1 == watchlistSizeNow)
                return watchListSizePrior - 1 == watchlistSizeNow
             
    except TimeoutException:
        watchlistContainer = driver.find_element(By.XPATH, "//*[@id='__next']/main/div/section/div/section/div/div[1]/section/div[2]/ul")
        watchListItems = watchlistContainer.find_elements(By.TAG_NAME, "li")
    
        for index, item in enumerate(watchListItems):
            #TODO replace all substring finds with in keyword instead 
            #TODO test this
            watchListItemName = item.find_element(By.CLASS_NAME, "ipc-title-link-wrapper").text

            if(cinemaItemTitle in watchListItemName):
                print(f"found title {cinemaItemTitle} at index {index} in non v2 site")
                #the xpath of the watch list items change one parameters based on there position in the list that is why index + 1is used to find the xpath of the found item's watchlist button
                watchListRemoveButton = item.find_element(By.XPATH, f"//*[@id='__next']/main/div/section/div/section/div/div[1]/section/div[2]/ul/li[{index + 1}]/div/div/div/div[1]/div[1]/div/div[1]")
                actions.move_to_element_with_offset(watchListRemoveButton, int(random.uniform(1,3)), int(random.uniform(1,3)))
                actions.click()
                actions.perform()
                print("clicked remove from watchlist on item in non v2 site")
                #need a small window to allow the dom to update
                time.sleep(.5)
                watchlistSizeNow = int(driver.find_element(By.XPATH, "//*[@id='imdbHeader']/div[2]/div[4]/a/span/span").get_attribute("innerHTML"))
                assert(watchListSizePrior - 1 == watchlistSizeNow)
                return watchListSizePrior - 1 == watchlistSizeNow  
            
        raise watchlist_item_not_found_error() 


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

    




