import pytest
from src.web_controller import web_actions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.model.login_error import LoginError
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class TestWebActions:
    #TODO get this test to be recoginzed
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


    @pytest.fixture(autouse=True)
    def setup(self, driver, request):
        if(request.node.name != "testLogin"):
            web_actions.login(driver, "03jrob@gmail.com", "testpass", "TestAccount")
            
    def testGetCinemaItems(self, driver):
        pass

    
    def testLogin(self, driver):
        #invalid login
        with pytest.raises(LoginError) as error:  
            web_actions.login(self.driver, "invalidUser@gmail.com", "wrongPass", "WrongAccountName")
        assert str(error.value).__contains__("Error logging in") 
        
        #valid login
        web_actions.login(self.driver, "03jrob@gmail.com", "testpass", "TestAccount")
        loggedInUserElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='imdbHeader']/div[2]/div[5]/div/label[2]/span/span")))
        assert loggedInUserElement.text == "TestAccount"

    def testIsLoggedIn(self, driver):
        pass 
    
    def testSubmitReview(self, driver):
        pass


    def testRemoveFromWatchlist(self, driver):
        pass

    def testGetCinemaItems(self, driver):
        pass
        


