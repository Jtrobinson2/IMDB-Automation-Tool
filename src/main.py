from pathlib import Path
import sys 
# Get the directory where the script is located
script_path = Path(__file__).resolve()
# Get the parent directory
parent_dir = script_path.parent.parent
sys.path.append( str(parent_dir) )

from src.web_controller import web_actions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = Options()
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(options=chrome_options)


fList = web_actions.getCinemaItems(driver, "Frieren")
print("lmao")
