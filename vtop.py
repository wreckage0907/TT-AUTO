from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image
import numpy as np
import pytesseract
import cv2
from dotenv import load_dotenv
import os
import requests
from io import BytesIO

load_dotenv()
user = os.getenv('USERNAME')
password = os.getenv('PWD')
driver = webdriver.Chrome()
driver.get("https://vtopcc.vit.ac.in/vtop/login")
save_path = "captcha.png"

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Girish\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
try:
    # Wait for student login form to appear
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="stdForm"]'))
    ).click()

    # Enter username and password
    driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(user)
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
    element = driver.find_element(By.XPATH, '//*[@id="captchaBlock"]').screenshot(save_path)
    time.sleep(5)
    image = Image.open(save_path)
    text = pytesseract.image_to_string(image)
    driver.find_element(By.XPATH, '//*[@id="captchaStr"]').send_keys(text.upper())
    time.sleep(2)

    # Submit the form
    driver.find_element(By.XPATH, '//*[@id="submitBtn"]').click()
    

except :
    driver.find_element(By.XPATH, '//*[@id="submitBtn"]').click()

time.sleep(5)
