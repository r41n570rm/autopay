# Author: Aqwa Hameed
# Date: June 21, 2024

import os
from dotenv import load_dotenv   
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time

# Load environment variables
load_dotenv()

# Get account details 
ACCOUNT_NUMBER = os.getenv("ACCOUNT_NUMBER")
TEL_NUMBER = os.getenv("TEL_NUMBER")
EMAIL = os.getenv("EMAIL")

# Get payment card details
CARD_NUMBER = os.getenv("CARD_NUMBER")
EXPIRY_MONTH = os.getenv("EXPIRY_MONTH")
EXPIRY_YEAR = os.getenv("EXPIRY_YEAR")
CARD_NAME = os.getenv("CARD_NAME")
CARD_CODE = os.getenv("CARD_CODE")


# Function to wait for elements to be present
def wait_for_element(driver, by, element_identifier, timeout=5):
    try:
        element_present = EC.presence_of_element_located((by, element_identifier))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print(f"Timed out wating for {element_identifier}")
        return None
    return driver.find_element(by, element_identifier)


# Define the script & webdriver path
script_directory = Path(__file__).resolve().parent
driver_path = script_directory.joinpath("geckodriver-v0.34.0-win64", "geckodriver.exe") 

service = Service(driver_path)
driver = webdriver.Firefox(service=service)

payment_page = "https://pay.slt.lk/instantpay"
driver.get(payment_page)

acc_number = wait_for_element(driver, By.ID, "EventSource")
tel_number = wait_for_element(driver, By.ID, "ContactNumber")
email = wait_for_element(driver, By.ID, "CustEmail")
amount = wait_for_element(driver, By.ID, "vpc_Amount")
submit_button = wait_for_element(driver, By.ID, "SubButL")

# Get bill payment amount
payment_amount = input("Enter bill payment amount: ") 

# Enter account details and click the submit button
if acc_number and tel_number and email and amount and submit_button:
    acc_number.send_keys(ACCOUNT_NUMBER)
    tel_number.send_keys(TEL_NUMBER)
    email.send_keys(EMAIL)
    amount.clear()
    amount.send_keys(payment_amount)
    submit_button.click()


# Check the terms & conditions textbox and choose the payment method
check_terms = wait_for_element(driver, By.ID, "checkTermsAndCondition")
payment_method = wait_for_element(driver, By.XPATH, "/html/body/div[1]/div/div/div/div/div/div/div/div/form[1]/button")


if check_terms and payment_method:
    check_terms.click()
    payment_method.click()


# Wait for elements to be present before proceeding
card_number = wait_for_element(driver, By.ID, "cardNumber")
expiry_month = Select(wait_for_element(driver, By.ID, "expiryMonth"))
expiry_year = Select(wait_for_element(driver, By.ID, "expiryYear"))
card_name = wait_for_element(driver, By.ID, "cardHolderName")
card_code = wait_for_element(driver, By.ID, "csc")
pay_now_button = wait_for_element(driver, By.XPATH, "/html/body/div[1]/div[9]/div[4]/button[1]")


# Enter card details and click the pay now button
if card_number and expiry_month and expiry_year and card_name and card_code and pay_now_button:
    card_number.send_keys(CARD_NUMBER)
    expiry_month.select_by_value(EXPIRY_MONTH)
    expiry_year.select_by_value(EXPIRY_YEAR)
    card_name.send_keys(CARD_NAME)
    card_code.send_keys(CARD_CODE)
    pay_now_button.click()

driver.quit()