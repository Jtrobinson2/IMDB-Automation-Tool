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
        frierenList = ["Frieren: Beyond Journey's End", 'Frieren', 'Soso no Frieren: Mini Anime', 
                       'Kleine frieren auch im Sommer', 'The Suitor', "Let's Get Married", 
                       'Labyrinth of Peace', 'Frères', 'Pros and Cons', 'Band of Brothers', 'Kylmä', 
                       'One Tree Hill', 'Brothers', 'White Chicks', 'Frieren', 'Daisy Jones & The Six', 
                       'Step Brothers', 'War & Peace', 'Friere', 'Guilt', 'Black-ish', 
                       'Rest in Peace', 'Book Club', 'The Brothers Sun', 'The Brigade'
                       ]
        
        assert web_actions.getCinemaItems(driver, "Frieren") == frierenList

    def testLogin(self, driver):
        #invalid login
        with pytest.raises(LoginError) as error:  
            web_actions.login(driver, "invalidUser@gmail.com", "wrongPass", "WrongAccountName")
        assert str(error.value).__contains__("Error logging in") 
        
        #valid login
        web_actions.login(driver, "03jrob@gmail.com", "testpass", "TestAccount")
        loggedInUserElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='imdbHeader']/div[2]/div[5]/div/label[2]/span/span")))
        assert loggedInUserElement.text == "TestAccount"

    



