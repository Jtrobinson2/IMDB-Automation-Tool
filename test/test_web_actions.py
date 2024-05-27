import pytest
from src.web_controller import web_actions
from src.model.review import Review
from src.model.watchlist_item_not_found_error import WatchListItemNotFoundError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.model.login_error import LoginError
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import NoSuchElementException
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
    assert TestWebActionsLoginRequired.resetWatchlistAfterRemoval(driver, "https://www.imdb.com/user/ur181375520/watchlist/", "Frieren: Beyond Journey's End")
    assert TestWebActionsLoginRequired.resetTestUserListAfterAddition(driver, "https://www.imdb.com/list/ls545984321/edit/?ref_=ls_ov", "Rise of the Planet of the Apes (2011)")
    driver.quit()
    
class TestWebActionsLoginRequired: 
    """Tests web actions that require the user to be logged in"""
        
    def testSubmitReview(self, loggedInDriver):
        headline = "This is a test headline"
        reviewBody = """Wayyy to much romantic melodrama in this. 
        The opening scene was Harry about the get laid and the ending scene (right after Dumbledore's funeral) was Hermione talking to Harry about "snogging" Ginny. 
        That and having to watch the melodrama of Ron getting it on with comically crazy Lavender Brown while Hermione implodes and Harry avoids getting drugged by yet another love interest was cringe and disrupted the otherwise dark tone of the film. 
        Many pivotal scenes in this didn't really make sense such as why Harry didn't just use the water spell directly in Dumbledore's mouth when he couldn't spoon feed him water, why Bellatrix randomly attacked the burrow (they can't harm harry so what's the point), or why Snape refers to himself as the Half blood prince. 
        Why did he even decide to to become a death eater. Last movie he was teaching Harry how to protect his mind from Voldemort but it's unclear why he changed sides (this may be revealed in the subsequent movie). 
        The revelation of the half blood prince as well as Dumbledore's death was weirdly anticlimactic since one revelation had zero leadup and the other suspends your disbelief that the most powerful wizard alive would go down to Snape without a fight. 
        One could argue this is ok because he was weakened but a weakened master should still solo an advanced magic user. This entry was a tonal mess, that relied to heavily on corny interpersonal 
        conflicts however we got to see more of Tom riddle pre-deformation which was the highlight of this film."""
        itemTitle = "Avatar"
        validReview = Review(itemTitle, headline, reviewBody, True, False,  7, True)

        #test invalid arguments
        with pytest.raises(ValueError) as error:  
            web_actions.submitReview(None, validReview)
        assert str(error.value) == "Error: provide a valid driver." 

        #test attempting to review cinema item that doesn't exist
        with pytest.raises(ValueError) as error:
            validReview.itemTitle = "One Piece Film: Redddd"  
            web_actions.submitReview(loggedInDriver, validReview)
        assert str(error.value) == "Error: item wasn't found on search please give a valid item title exactly."

        #test reviewing valid item
        validReview.itemTitle = itemTitle
        assert web_actions.submitReview(loggedInDriver, validReview)

    def testAddItemToUserList(self, loggedInDriver):
        #test invalid arguments
        with pytest.raises(ValueError) as error:  
            web_actions.addReviewToUserList(None, "Rise of the Planet of the Apes (2011)", "https://imdb.com/list/ls545984321/?ref_=uspf_t_1", "this movie is good", None)
        assert str(error.value) == "Error: provide a valid driver."

        with pytest.raises(ValueError) as error:  
            web_actions.addReviewToUserList(loggedInDriver, "", "https://imdb.com/list/ls545984321/?ref_=uspf_t_1", "this movie is good", None)
        assert str(error.value) == "Error: item to review not provided."

        with pytest.raises(ValueError) as error:  
            web_actions.addReviewToUserList(loggedInDriver, None, "https://imdb.com/list/ls545984321/?ref_=uspf_t_1", "this movie is good", None)
        assert str(error.value) == "Error: item to review not provided."

        with pytest.raises(ValueError) as error:  
            web_actions.addReviewToUserList(loggedInDriver, "Rise of the Planet of the Apes (2011)", "", "this movie is good", None)
        assert str(error.value) == "Error: watchlist URL cannot be empty or none."

        with pytest.raises(ValueError) as error:  
            web_actions.addReviewToUserList(loggedInDriver, "Rise of the Planet of the Apes (2011)", None, "this movie is good", None)
        assert str(error.value) == "Error: watchlist URL cannot be empty or none."

        with pytest.raises(ValueError) as error:  
            web_actions.addReviewToUserList(loggedInDriver, "Rise of the Planet of the Apes (2011)", "https://imdb.com/list/ls545984321/?ref_=uspf_t_1", "", None)
        assert str(error.value) == "Error: review body cannot be empty or none."

        with pytest.raises(ValueError) as error:  
            web_actions.addReviewToUserList(loggedInDriver, "Rise of the Planet of the Apes (2011)", "https://imdb.com/list/ls545984321/?ref_=uspf_t_1", None, None)
        assert str(error.value) == "Error: review body cannot be empty or none."

        #try to add a cinmema item to the review list that doesn't exist 
        assert not web_actions.addReviewToUserList(loggedInDriver, "Rise of the Planet of the Apes (2066)", "https://imdb.com/list/ls545984321/?ref_=uspf_t_1", "this movie is good", None)

        #add a valid review item
        assert web_actions.addReviewToUserList(loggedInDriver, "Rise of the Planet of the Apes (2011)", "https://imdb.com/list/ls545984321/?ref_=uspf_t_1", "this movie is good", None)

    def testRemoveFromWatchlist(self, loggedInDriver):
        #Invalid arguments
        with pytest.raises(ValueError) as error:  
            web_actions.removeFromWatchList(None, "Frieren: Beyond Journey's End")
        assert str(error.value) == "Error: provide a valid driver"
        
        with pytest.raises(WatchListItemNotFoundError):  
            web_actions.removeFromWatchList(loggedInDriver, "Item not in watchlist lmaoo")

        #remove something actually in watchlist
        assert web_actions.removeFromWatchList(loggedInDriver, "Frieren: Beyond Journey's End")

    def resetWatchlistAfterRemoval(driver : webdriver,  watchlistURL : str, removedItem : str)-> bool:
        """Resets the watchlist to what it was before testing the removal of a cinema item.
            
            Args:
                removedItem (str) : removed cinema item you want to re-add to the watchlist
                driver (webdriver) : web driver
            Returns:
                bool: True if watchlist was reset successfully
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

        searchResultListItems = driver.find_elements(By.XPATH, "//*[@id='__next']/main/div[2]/div[4]/section/div/div[1]/section[2]/div[2]/ul/li/div[2]/div/a")
        
        for item in searchResultListItems:
            if(item.text == removedItem):
                item.click()
                addToWatchlistRibbon = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[3]/div[1]/div[1]/div/div[2]"))) 
                addToWatchlistRibbon.click()
                return True 
        
        return False
    
    def resetTestUserListAfterAddition(driver : webdriver,  watchlistURL : str, addedItem : str)-> bool:
        """Resets the test user list by removing the cinema item we added to it for subsequent tests
            
            Args:
                addedItem (str) : added cinema item you want to re-add to the watchlist
                driver (webdriver) : web driver
            Returns:
                bool: True if the item was removed from the user list  successfully
            Raises:
                ValueError : if addedItem is none or empty
                ValueError : if web driver is  none or empty
        """
        if(not addedItem):
            raise ValueError("Error: item that was added to the user list was not provided")
        if(not driver):
            raise ValueError("Error: you must provide a web driver")
        if(not watchlistURL):
            raise ValueError("Error: you need to provide the watchlist to remove from.")
        #if your signed in and use this url it will pull up the test list already in edit mode from the previous test
        driver.get(watchlistURL)

        listItems = driver.find_elements(By.XPATH, "//*[@id='__next']/main/div/section/div/section/div/div[1]/section/div/ul/div/li/div[2]/div/div/div[1]/a/h3")
        assert listItems

        #find the cinema item in the new dropdown list
        for index, item in enumerate(listItems):
            #slicing off the year from the itemToReview string (test (2011) -> test )
            if(addedItem[:-7] in item.text):
                #click the items checkbox
                itemcheckbox = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='__next']/main/div/section/div/section/div/div[1]/section/div[4]/ul/div[{index + 1}]/li/div[1]/div[1]/span/span/input")))
                driver.execute_script("arguments[0].click();", itemcheckbox)
                #click delete
                deleteButton  = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='__next']/main/div/section/div/section/div/div[1]/section/div[3]/div[2]/button[3]"))) 
                driver.execute_script("arguments[0].click();", deleteButton)
                #click confirm to delete
                confirmDeleteButton  = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[6]/div[2]/div/div[2]/div/div[2]/button[2]")))
                driver.execute_script("arguments[0].click();", confirmDeleteButton)
                break
                
        # check if the item was actually removed
        try:
            driver.find_element(By.XPATH, "/html/body/section")
            return True
        except NoSuchElementException:
            return False


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
