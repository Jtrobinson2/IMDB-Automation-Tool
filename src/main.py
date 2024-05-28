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
from src.util import Configuration


#TODO correct profile is opened but session not created exception persists will dry downloading and updating chrome driver
"""    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome failed to start: exited normally.
  (session not created: DevToolsActivePort file doesn't exist)
  (The process started from chrome location C:\Program Files (x86)\Google\Chrome\Application\chrome.exe is no longer running, so ChromeDriver is assuming that Chrome has crashed.)"""
chrome_options = Options()
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument(f"--user-data-dir={Configuration.PATH_TO_CHROME_PROFILE}")
chrome_options.add_argument('--profile-directory=Profile 3')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options=chrome_options)

# web_actions.login(driver, "03jrob@gmail.com", "testpass", "TestAccount")
web_actions.isLoggedIn(driver)

