# PYTHON Example
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(r"C:\Users\thera\Desktop\Python\Chess\bot\src\chromedriver.exe", options=chrome_options)
print (driver.title)