from selenium import webdriver
# driver = webdriver.Firefox(executable_path=r'C:\L\Anaconda3\envs\rango\Scripts\geckodriver.exe')
# driver.get('http://localhost:8000')


browser = webdriver.Firefox()

browser.get('http://localhost:8000')

assert 'Django' in browser.title