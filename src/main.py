from pathlib import Path
import sys

# Get the directory where the script is located
script_path = Path(__file__).resolve()
# Get the parent directory
parent_dir = script_path.parent.parent
sys.path.append( str(parent_dir) )

from src.web_controller import web_actions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(options=chrome_options)

web_actions.login(driver, "03jrob@gmail.com", "testpass", "TestAccount")
assert web_actions.addReviewToWatchList(driver, "Rise of the Planet of the Apes (2011)", "https://imdb.com/list/ls545984321/?ref_=uspf_t_1", "this movie is good", None)