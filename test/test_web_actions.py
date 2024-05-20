import pytest
from src.web_controller import web_actions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.model.login_error import LoginError
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#setup driver once for the entire module tear down when tests are done.
@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

class TestWebActionsLoginRequired:    
    def testIsLoggedIn(self, driver):
        pass 
    
    def testSubmitReview(self, driver):
        pass


    def testRemoveFromWatchlist(self, driver):
        pass


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

    def testLogin(self, driver):
        #invalid login
        with pytest.raises(LoginError) as error:  
            web_actions.login(driver, "invalidUser@gmail.com", "wrongPass", "WrongAccountName")
        assert str(error.value).__contains__("Error logging in") 
        
        #valid login
        web_actions.login(driver, "03jrob@gmail.com", "testpass", "TestAccount")
        loggedInUserElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='imdbHeader']/div[2]/div[5]/div/label[2]/span/span")))
        assert loggedInUserElement.text == "TestAccount"

    



