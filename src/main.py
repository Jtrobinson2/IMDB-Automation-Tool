from pathlib import Path
import sys

# Get the directory where the script is located
script_path = Path(__file__).resolve()
# Get the parent directory
parent_dir = script_path.parent.parent
sys.path.append( str(parent_dir) )

from src.web_controller import web_actions
from src.model.review import Review
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(options=chrome_options)

web_actions.login(driver, "03jrob@gmail.com", "testpass", "TestAccount")



