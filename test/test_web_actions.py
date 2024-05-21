import pytest
from src.web_controller import web_actions
from src.model.watchlist_item_not_found_error import WatchListItemNotFoundError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.model.login_error import LoginError
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from src.web_controller.web_actions import sendKeysLikeHuman
import random 


#driver to be used for all web actions that don't require loggin in. Destroyed when those tests are done.
@pytest.fixture(scope="class")
def loggedInDriver():
    chrome_options = Options()
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=chrome_options)
    web_actions.login(driver, "03jrob@gmail.com", "testpass", "TestAccount")
    yield driver
    TestWebActionsLoginRequired.resetWatchlistAfterRemoval(driver, "https://www.imdb.com/user/ur181375520/watchlist/", "Frieren: Beyond Journey's End")
    driver.quit()
    
class TestWebActionsLoginRequired: 
    """Tests web actions that require the user to be logged in"""
        
    def testSubmitReview(self, loggedInDriver):
        pass
    
    def testRemoveFromWatchlist(self, loggedInDriver):
        #Invalid arguments
        with pytest.raises(ValueError) as error:  
            web_actions.removeFromWatchList(None, "Frieren: Beyond Journey's End")
        assert str(error.value) == "Error: provide a valid driver"
        
        with pytest.raises(WatchListItemNotFoundError):  
            web_actions.removeFromWatchList(loggedInDriver, "Item not in watchlist lmaoo")

        #remove something actually in watchlist
        assert web_actions.removeFromWatchList(loggedInDriver, "Frieren: Beyond Journey's End")

    def resetWatchlistAfterRemoval(driver : webdriver,  watchlistURL : str, removedItem : str):
        """Resets the watchlist to what it was before testing the removal of a cinema item.
            
            Args:
                removedItem (str) : removed cinema item you want to re-add to the watchlist
                driver (webdriver) : web driver
            Raises:
                ValueError : if removed item  is none or empty
                ValueError : if web driver is  none or empty
        """
        if(not removedItem):
            raise ValueError("Error: item to remove from watchlist not provided")
        if(not driver):
            raise ValueError("Error: you must provide a web driver")
        if(not watchlistURL):
            raise ValueError("Error: you need to provide the watchlist to remove from.")
        
        actions = ActionChains(driver)

        driver.get(watchlistURL)
        searchBar = driver.find_element(By.XPATH, "//*[@id='suggestion-search']")
        searchTypeDropDown = driver.find_element(By.XPATH, "//*[@id='nav-search-form']/div[1]/div/label")
        actions.move_to_element_with_offset(searchTypeDropDown, int(random.uniform(1,3)), int(random.uniform(1,3)))
        actions.click()

        titleSearchTypeDropDownItem = driver.find_element(By.XPATH, "//*[@id='navbar-search-category-select-contents']/ul/li[2]") 
        actions.move_to_element_with_offset(titleSearchTypeDropDownItem, int(random.uniform(1,3)), int(random.uniform(1,3)))
        actions.click()

        searchBar = driver.find_element(By.XPATH, "//*[@id='suggestion-search']")
        sendKeysLikeHuman(removedItem, driver, searchBar)
        searchButton = driver.find_element(By.XPATH, "//*[@id='suggestion-search-button']")
        actions.move_to_element_with_offset(searchButton, int(random.uniform(1,3)), int(random.uniform(1,3)))
        actions.click()
        
        actions.perform()

        searchResultListItems = driver.find_elements(By.XPATH, "//*[@id='__next']/main/div[2]/div[3]/section/div/div[1]/section[2]/div[2]/ul/li[contains(@class, 'ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click find-result-item find-title-result')]/div[2]/div/a")
        
        for item in searchResultListItems:
            if(item.text == removedItem):
                item.click()
                addToWatchlistRibbon = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[3]/div[1]/div[1]/div/div[2]"))) 
                addToWatchlistRibbon.click()


#driver to be used for all web actions that don't require loggin in. Destroyed when those tests are done.
@pytest.fixture(scope="class")
def driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

class TestWebActionsNoLogin:
    """Tests web actions that don't require the user to be logged in, this allows setup code in class above 
     to include logic for loggin in a prerequisite for most tests to pass """
    
    def testGetCinemaItems(self, driver):
        with pytest.raises(ValueError) as error:  
            web_actions.getCinemaItems(None, "Example")
        assert str(error.value) == "Error: provide a valid driver"

        with pytest.raises(ValueError) as error:  
            web_actions.getCinemaItems(driver, "")
        assert str(error.value) == "Error: cinema item title cannot be empty"

        with pytest.raises(ValueError) as error:  
            web_actions.getCinemaItems(driver, None)
        assert str(error.value) == "Error: cinema item title cannot be empty"

        # only checks the first five elements because the rest are liable to change often
        firstFiveFrierenResults = ["Frieren: Beyond Journey's End", 'Frieren', 'Soso no Frieren: Mini Anime', 
                       'The Suitor', 'Kleine frieren auch im Sommer']
        
        actualList = web_actions.getCinemaItems(driver, "Frieren")     
        assert len(actualList) > len(firstFiveFrierenResults)
        assert  actualList[:5] == firstFiveFrierenResults[:5]


    def testLoginAndIsLoggedIn(self, driver):
        #invalid parameters
        with pytest.raises(ValueError) as error:  
            web_actions.login(None, "invalidUser@gmail.com", "wrongPass", "WrongAccountName")
        assert str(error.value).__contains__("Error: Please Provide a valid driver") 

        with pytest.raises(ValueError) as error:  
            web_actions.login(driver, "accountName", "wrongPass", "")
        assert str(error.value).__contains__("Error: username cannot be null or empty") 

        with pytest.raises(ValueError) as error:  
            web_actions.login(driver, "accountName", "wrongPass", None)
        assert str(error.value).__contains__("Error: username cannot be null or empty") 

        with pytest.raises(ValueError) as error:  
            web_actions.login(driver, "", "wrongPass", "username")
        assert str(error.value).__contains__("Error: account username cannot be null or empty") 

        with pytest.raises(ValueError) as error:  
            web_actions.login(driver, None, "wrongPass", "username")
        assert str(error.value).__contains__("Error: account username cannot be null or empty") 

        with pytest.raises(ValueError) as error:  
            web_actions.login(driver, "accountName", "", "username")
        assert str(error.value).__contains__("Error: password cannot be null or empty") 

        with pytest.raises(ValueError) as error:  
            web_actions.login(driver, "accountName", None, "username")
        assert str(error.value).__contains__("Error: password cannot be null or empty") 

        #invalid login
        with pytest.raises(LoginError) as error:  
            web_actions.login(driver, "accountName", "wrongPass", "username")
        assert str(error.value).__contains__("Error logging in") 

        #invalid is logged in arguements
        with pytest.raises(ValueError) as error:  
            web_actions.isLoggedIn(None)
        assert str(error.value).__contains__("Error: Please Provide a valid driver") 
    
        #valid login
        web_actions.login(driver, "03jrob@gmail.com", "testpass", "TestAccount")
        loggedInUserElement = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[@id='imdbHeader']/div[2]/div[5]/div/label[2]/span/span")))
        assert loggedInUserElement.text == "TestAccount"
        assert web_actions.isLoggedIn(driver)
