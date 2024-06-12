"""Module that contains all of the web actions from logging in to submitting a review that automation tool will need.
"""
from src.model.review import Review
import src.util.review_util as util
from src.model.duplicate_list_item_exception import DuplicateListItemException
from src.model.watchlist_item_not_found_error import WatchListItemNotFoundError
from src.util import endpoints
from selenium import webdriver
from src.model.login_error import LoginError
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re
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
            raise LoginError("Error logging in you must login manually")
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
    
    
def submitReview(driver : webdriver, review : Review) -> bool:
    """Submits a review to a user's IMDB lists and the reviewed item's page

    Args:
        Review (Review): The review to submit 
        driver (webdriver): the web driver to perform the actions

    Raises:
        ValueError: If driver is None.
        ValueError: If review  is None.
        LoginError: if the user isn't logged in
        ValueError: If review is invalid for whatever reason   
    """
    if(not driver):
        raise ValueError("Error: provide a valid driver.")
    if(not isLoggedIn(driver)):
        raise LoginError("Error: user must be logged in submit review.")
    #TODO: maybe refactor is review valid to just through value errors instead
    inspectionResults = util.isReviewValid(review, {"[/spoiler]" : "[spoiler]", "[/b]" : "[b]"})
    if(not inspectionResults[0]):
        raise ValueError(inspectionResults[1])
    
    driver.get(endpoints.IMDB_HOME_PAGE)

    actions = ActionChains(driver)
    
    searchTypeDropDown = driver.find_element(By.XPATH, "//*[@id='nav-search-form']/div[1]/div/label")
    actions.move_to_element_with_offset(searchTypeDropDown, int(random.uniform(1,3)), int(random.uniform(1,3)))
    actions.click()

    titleSearchTypeDropDownItem = driver.find_element(By.XPATH, "//*[@id='navbar-search-category-select-contents']/ul/li[2]") 
    actions.move_to_element_with_offset(titleSearchTypeDropDownItem, int(random.uniform(1,3)), int(random.uniform(1,3)))
    actions.click()

    searchBar = driver.find_element(By.XPATH, "//*[@id='suggestion-search']")
    sendKeysLikeHuman(review.itemTitle, driver, searchBar)
    searchButton = driver.find_element(By.XPATH, "//*[@id='suggestion-search-button']")
    actions.move_to_element_with_offset(searchButton, int(random.uniform(1,3)), int(random.uniform(1,3)))
    actions.click()
    
    actions.perform()

    itemFound = False

    for item in driver.find_elements(By.XPATH, "//*[@id='__next']/main/div/div/section/div/div/section/div/ul/li/div/div/a"):
        if(review.itemTitle in item.text):
            item.click()
            itemFound = True
            break

    if(not itemFound):
        raise ValueError("Error: item wasn't found on search please give a valid item title exactly.")
    
    #click the review button 
    reviewButton = driver.find_element(By.XPATH, "//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/ul/li[1]/a")
    actions.scroll_to_element(reviewButton)
    actions.click(reviewButton)
    actions.perform()
    
    
    #click review this title
    driver.find_element(By.XPATH, "//*[@id='main']/section/div[1]/div/a").click()

    #move the driver to the iframe the review elements are in
    driver.switch_to.frame(WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[@id='cboxLoadedContent']/iframe"))))

    #get all the stars in the review bar 
    reviewStarRatingBar = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[@id='react-entry-point']/div/div/div[1]/div[3]/div[1]/div")))
    ratingStars = reviewStarRatingBar.find_elements(By.CLASS_NAME, "ice-star-wrapper")

    #click the one that corresponds to the rating out of ten
    ratingStars[review.rating - 1].click()

    #ensure that it was rated correctly the 1/10, 2/10 etc alert should pop up here
    assert( f"{review.rating}/{10}" in WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//*[@id='react-entry-point']/div/div/div[1]/div[3]/div[2]/div/div/div"))).text)

    #paste in headline 
    driver.find_element(By.XPATH, "//*[@id='react-entry-point']/div/div/div[1]/div[5]/div[1]/input").send_keys(review.headline)

    #paste in review body 
    driver.find_element(By.XPATH, "//*[@id='react-entry-point']/div/div/div[1]/div[5]/div[2]/textarea").send_keys(review.reviewBody)
    
    #select spoilers option (yes or no)
    spoilerButtonID = 1 if review.containsSpoilers else 2
    driver.find_element(By.XPATH, f"//*[@id='react-entry-point']/div/div/div[1]/div[5]/div[3]/div/ul/li[{spoilerButtonID}]/span[1]").click()

    #click the submit button
    driver.find_element(By.XPATH, "//*[@id='react-entry-point']/div/div/div[2]/span/span/input").click()

    #ensure it was submitted correctly
    return "Submission" in WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='react-entry-point']/div/div/div[1]/div/div/div[2]/span[4]"))).get_attribute("innerHTML")

    


def addReviewToUserList(driver : webdriver, itemToReview : str,  userCinemaListURL : str, reviewBody : str, validTags : dict[str,str]=None):
    """Submits a review to a specified user created list on imdb 

    Args:
        driver (webdriver): web driver to execute actions
        userCinemaListURL (str): the url of the list the review needs to be added to
        itemToReview (str): title of cinema item to review NOTE: you need to append the year of item to review to the string "Attack On Titan (2013)" 
        reviewBody (str): the review itself with our without markup
        validTags (dict[str,str]): markup tags that will be used in the review if needed ({closing tag : opening tag})

    Raises:
        ValueError: if itemToReview is empty or None
        ValueError: if userCinemaListURL is empty or None
        ValueError: if reviewBody is empty or None
        ValueError: if reviewBody markup is invalid
        LoginError: if user is not logged in
        DuplicateListItemException: if users attempts to add a review to a list that already has that review
    """
    if(not driver):
        raise ValueError("Error: provide a valid driver.")
    if(not itemToReview):
        raise ValueError("Error: item to review not provided.")
    if(not userCinemaListURL):
        raise ValueError("Error: watchlist URL cannot be empty or none.")
    if(not reviewBody):
        raise ValueError("Error: review body cannot be empty or none.")
    if(not isLoggedIn(driver)):
        raise LoginError("Error: user must be logged in to submit review to watchlist.")
    if(not validTags):
        validTags = {"[/spoiler]" : "[spoiler]", "[/b]" : "[b]"}
    if(not util.validateMarkup(reviewBody, validTags)):
        raise ValueError("Error: invalid review markup")

    driver.get(userCinemaListURL)

    #regex is for removing the 1., 2., on the cinema item titles before putting them in the set (1. example --> example)
    listItemTitlesSet = set()
    [listItemTitlesSet.add(re.sub(r'^\d+\.\s*', '', elem.text)) for elem in driver.find_elements(By.XPATH, "//*[@id='__next']/main/div/section/div/section/div/div[1]/section/div[2]/ul/li/div/div/div/div[1]/div[2]/div[1]/a/h3")]
    if(itemToReview[:-7] in listItemTitlesSet):
        raise DuplicateListItemException()

    #Hit edit button 
    driver.find_element(By.XPATH, "//*[@id='__next']/main/div/section/section/div[3]/section/div[1]/div/div[2]/a").click()

    #select the search bar and put the cinema item to review into search bar
    searchBar = driver.find_element(By.XPATH, "//*[starts-with(@id, 'text-input')]")
    sendKeysLikeHuman(itemToReview, driver, searchBar)
    driver.find_element(By.XPATH, "//*[starts-with(@id, 'text-input')]").click()

    #find the cinema item from the dropdown and click it
    itemFound = False
    for result in driver.find_elements(By.XPATH, "//*[starts-with(@id, 'react-autowhatever-1--item-')]"):
        if(result.text == itemToReview):
            result.click()
            itemFound = True
            break
    
    if(not itemFound):
        return False
        
    #wait until the new item has been actually added to the list (this is a snackbar that shows indicated success)
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "/html/body/section")))
    listItemsAfterAddition = driver.find_elements(By.XPATH, "//*[@id='__next']/main/div/section/div/section/div/div[1]/section/div/ul/div/li/div[2]/div/div/div[1]/a/h3")

    #find the cinema item in the new dropdown list
    for index, item in enumerate(listItemsAfterAddition):
        #slicing off the year from the itemToReview string (test (2011) -> test )
        if(itemToReview[:-7] in item.text):
            #click into the cinema item's description field
            inputFieldButton = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='__next']/main/div/section/div/section/div/div[1]/section/div[4]/ul/div[{index + 1}]/li/div[2]/div/div/div[4]")))
            driver.execute_script("arguments[0].click();", inputFieldButton)
            #paste the review markup 
            reviewInputArea = driver.find_element(By.XPATH, "//*[@id='__next']/main/div/section/div/section/div/div[1]/section/div[4]/ul/div/li/div[2]/div/div/div[4]/div/div/div").find_element(By.TAG_NAME, "textarea")
            reviewInputArea.send_keys(reviewBody + Keys.ENTER)
            break
            
    # check if  list item descrtiption successfully updated element is present if so it worked.
    try:
        driver.find_element(By.XPATH, "/html/body/section")
        return True
    except NoSuchElementException:
        return False

def getCinemaItems(driver : webdriver, cinemaItemTitle : str) -> list[str]:
    """Retrieves a list of cinema items from IMDB given the cinema items title

    Args:
        cinemaItemTitle (str): title of the cinema item your looking for
        driver (webdriver): the web driver to perform the actions 

    Raises:
        ValueError: If cinemaItemTitle is None or Empty.
        ValueError: If the driver is None 
    """  

    if(not driver):
        raise ValueError("Error: provide a valid driver")
    if(not cinemaItemTitle):
        raise ValueError("Error: cinema item title cannot be empty")
    

    driver.get(endpoints.IMDB_HOME_PAGE)

    actions = ActionChains(driver)
    
    searchTypeDropDown = driver.find_element(By.XPATH, "//*[@id='nav-search-form']/div[1]/div/label")
    actions.move_to_element_with_offset(searchTypeDropDown, int(random.uniform(1,3)), int(random.uniform(1,3)))
    actions.click()

    titleSearchTypeDropDownItem = driver.find_element(By.XPATH, "//*[@id='navbar-search-category-select-contents']/ul/li[2]") 
    actions.move_to_element_with_offset(titleSearchTypeDropDownItem, int(random.uniform(1,3)), int(random.uniform(1,3)))
    actions.click()

    searchBar = driver.find_element(By.XPATH, "//*[@id='suggestion-search']")
    sendKeysLikeHuman(cinemaItemTitle, driver, searchBar)
    searchButton = driver.find_element(By.XPATH, "//*[@id='suggestion-search-button']")
    actions.move_to_element_with_offset(searchButton, int(random.uniform(1,3)), int(random.uniform(1,3)))
    actions.click()
    
    actions.perform()
    searchResultListItems = driver.find_elements(By.XPATH, "//*[@id='__next']/main/div[2]/div/section/div/div[1]/section[2]/div[2]/ul/li/div[2]/div/a")

    return  [item.text for item in searchResultListItems]


def removeFromWatchList(driver : webdriver, cinemaItemTitle : str) -> bool :
    """Removes a cinema item from the users watchlist

    Args:
        cinemaItemTitle (str): title of cinema item to remove from watch list
        driver (webdriver): the web driver to perform the actions 

    Returns:
        bool: if item was able to be removed from watchlist

    Raises:
        WatchListItemNotFoundError: If cinema item wasn't in the watchlist
        ValueError: If the webdriver is None 
        Exception: If user is not logged in
          
    """  
    if(not driver):
        raise ValueError("Error: provide a valid driver")
    if(not isLoggedIn(driver)):
        raise Exception("Error: nobody is logged in cannot remove from watchlist.")

    try:
       watchListSizeText = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='imdbHeader']/div[2]/div[4]/a/span/span"))).get_attribute("innerHTML")
    except Exception:
        raise TimeoutError("Error: the web element that contains the watchlist didn't load for some reason")

    watchListSizePrior = int(watchListSizeText)
    watchlistSizeNow = watchListSizePrior
    watchListHyperLink = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[@id='imdbHeader']/div[2]/div[4]/a"))).get_attribute("href")
    driver.get(watchListHyperLink)

    #actions to be used when watchlist removal takes place
    actions = ActionChains(driver)

    #two different versions of the imdb website we have to have logic for removing from watchlist
    try:
        #if we get this version of the watchlist page do this algorithmn
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[@id='styleguide-v2']")))
        watchListItems = driver.find_elements(By.CLASS_NAME, "lister-item-header")

        for index, item in enumerate(watchListItems):
            if(cinemaItemTitle in item.text):
                #css selector for each watch list item ribbon changes based on the cinema item's positon in the watchlist
                watchListRemoveButton = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, f"#center-1-react > div > div:nth-child(3) > div > div:nth-child({index + 1}) > div > div.lister-item-image > div")))
                actions.move_to_element_with_offset(watchListRemoveButton, int(random.uniform(1,3)), int(random.uniform(1,3)))
                actions.click()
                actions.perform()            
                driver.refresh()
                #need to re-find this element because if you don't you'll get a stale element exception even though it's still in the dom??
                watchlistSizeNow = int(driver.find_element(By.XPATH, "//*[@id='imdbHeader']/div[2]/div[4]/a/span/span").get_attribute("innerHTML"))
                return watchListSizePrior - 1 == watchlistSizeNow
             
    except TimeoutException:
        watchlistContainer = driver.find_element(By.XPATH, "//*[@id='__next']/main/div/section/div/section/div/div[1]/section/div[2]/ul")
        watchListItems = watchlistContainer.find_elements(By.TAG_NAME, "li")
    
        for index, item in enumerate(watchListItems):
            watchListItemName = item.find_element(By.CLASS_NAME, "ipc-title-link-wrapper").text
            if(cinemaItemTitle in watchListItemName):
                #the xpath of the watch list items change one parameters based on there position in the list that is why index + 1is used to find the xpath of the found item's watchlist button
                watchListRemoveButton = item.find_element(By.XPATH, f"//*[@id='__next']/main/div/section/div/section/div/div[1]/section/div[2]/ul/li[{index + 1}]/div/div/div/div[1]/div[1]/div/div[1]")
                actions.move_to_element_with_offset(watchListRemoveButton, int(random.uniform(1,3)), int(random.uniform(1,3)))
                actions.click()
                actions.perform()
                #need a small window to allow the dom to update
                time.sleep(.5)
                watchlistSizeNow = int(driver.find_element(By.XPATH, "//*[@id='imdbHeader']/div[2]/div[4]/a/span/span").get_attribute("innerHTML"))
                return watchListSizePrior - 1 == watchlistSizeNow  
            
        raise WatchListItemNotFoundError() 


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

