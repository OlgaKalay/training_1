from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import timedelta, date, datetime
#from selenium.webdriver.support import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_payments_reporting():

    url = "https://stage.zentist.io/"
    login = "login"
    password = "password"

    email_input = (By.CSS_SELECTOR, '[data-testid="email"]')
    password_input = (By.CSS_SELECTOR, '[data-testid="password"]')
    login_button = (By.CSS_SELECTOR, '[data-testid="submit"]')
    main_menu = (By.CSS_SELECTOR, '[data-testid="main-menu"] div[role="button"]')
    menu_paiments_reporting = (By.XPATH, '//span[text()="Payments Reporting"]')
    title_paiments_reporting = (By.XPATH, '//h1[text()="Payments Reporting"]')
    calendar_1 = (By.CSS_SELECTOR, '[data-testid="calendar-field-1"]')
    recieved_on_sort = ((By.XPATH, '//span[text()="Received on"]'))
    recieved_on = ((By.CSS_SELECTOR, '[data-testid="received-on"]'))

    driver = webdriver.Chrome()
    driver.get(url)
    timeout_main = 21

    #login to the system
    try:
        element = WebDriverWait(driver, timeout_main).until(
            EC.visibility_of_element_located(email_input)
        )
        driver.find_element(*email_input).send_keys(login)
        driver.find_element(*password_input).send_keys(password)
    finally:
        driver.find_element(*login_button).click()

    #open Payments Reporting and check that it is Payments reporting
    try:
        element = WebDriverWait(driver, timeout_main).until(
            EC.visibility_of_element_located(main_menu)
        )
    finally:
        driver.find_element(*main_menu).click()
        driver.find_element(*menu_paiments_reporting).click()
    try:
        element = WebDriverWait(driver, timeout_main).until(
            EC.visibility_of_element_located(title_paiments_reporting)
        )
    finally:
        driver.find_element(*title_paiments_reporting)

    #open Calendar
    driver.find_element(*calendar_1).click()

    #clear Calendar
    driver.find_element(*calendar_1).send_keys(Keys.CONTROL + "a")
    driver.find_element(*calendar_1).send_keys(Keys.DELETE)

    #set Calendar - 15 days
    first_date = date.today() - timedelta(15)
    second_date = date.today()
    requested_date = first_date.strftime("%m/%d/%Y")
    driver.find_element(*calendar_1).send_keys(requested_date)
    driver.find_element(*calendar_1).send_keys(Keys.ESCAPE)

    #get Recieved_on_date
    try:
        element = WebDriverWait(driver, timeout_main).until(
            EC.visibility_of_element_located(recieved_on)
        )
    finally:
        sort = driver.find_element(*recieved_on_sort).click
        recieved_on_date = driver.find_element(*recieved_on).text
    recieved_on_date_object = datetime.strptime(recieved_on_date, '%b %d, %Y').date()

    #close browser
    driver.close()
    driver.quit()

    #check_results
    assert first_date <= recieved_on_date_object <= second_date


