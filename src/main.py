from web_controller import web_actions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

web_actions.login(webdriver.Chrome(), "testuser", "testpass")

