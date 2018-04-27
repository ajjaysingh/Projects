# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

# driver = webdriver.Firefox()
# driver.get("http://www.python.org")
# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


word = 'republec'
chromedriver = "/Users/chaser/Downloads/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

# driver.get("http://www.google.com")
# input_element = driver.find_element_by_name("q")
# input_element.send_keys("define " + word + "\n")
# input_element.submit()


driver.get("https://www.google.co.in/search?q=define+" + word)
RESULTS_LOCATOR = "//div[@class='ellip _Axg exp-txt-c xcas']"

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, RESULTS_LOCATOR)))

more = driver.find_elements(By.XPATH, RESULTS_LOCATOR)

more[0].click()

RESULTS_LOCATOR = "//span[@class='lr_dct_trns_sel_cnt']"

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, RESULTS_LOCATOR)))

options = driver.find_element(By.XPATH, RESULTS_LOCATOR)

# help(options)
# print(options.text)
opt = options.find_element(By.XPATH, '//Select')
# print(opt.text)
# help(opt)
for o in opt.find_elements_by_tag_name('option'):
    if o.text == 'Hindi':
        o.click() # select() in earlier versions of webdriver
        break

# print(options[0].first_selected_option.text)
RESULTS_LOCATOR = "//div[@class='lr_dct_trns']"
# vk_txt
trans = driver.find_element(By.XPATH, RESULTS_LOCATOR)
# for ll in trans:
#     level = ll.find_elements(By.XPATH, "//li")
#     print("---")
#     for l in level:
#         print(">" + l.text)

level = trans.find_elements(By.XPATH, "//li[@class='vk_txt']")
print("---")
for l in level:
    print(">" + l.text)

driver.quit()

