import pytest
from src.web_controller import web_actions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.model.login_error import LoginError
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#driver to be used for all web actions that don't require loggin in. Destroyed when those tests are done.
@pytest.fixture(scope="class")
def loggedInDriver():
    chrome_options = Options()
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=chrome_options)
    web_actions.login(driver, "03jrob@gmail.com", "testpass", "TestAccount")
    yield driver
    driver.quit()

class TestWebActionsLoginRequired: 
    """Tests web actions that require the user to be logged in"""
        
    def testSubmitReview(self, loggedInDriver):
        assert web_actions.isLoggedIn(loggedInDriver)
        pass

    def testRemoveFromWatchlist(self, loggedInDriver):
        assert web_actions.isLoggedIn(loggedInDriver)
        pass



#driver to be used for all web actions that don't require loggin in. Destroyed when those tests are done.
@pytest.fixture(scope="class")
def driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("detach", True)
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




        



    



