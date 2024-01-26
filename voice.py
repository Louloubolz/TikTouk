
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import shutil
import time
from datetime import datetime



def generate_speech(text_prompt, name_project) :
     
    dst_path = "temporaire/" + name_project + "_audio.mp3"

    driver=webdriver.Chrome()

    driver.get("https://freetools.textmagic.com/text-to-speech")
    driver.maximize_window()

    driver.find_element(By.XPATH, '/html/body/div[2]/div/section/div/div[2]/textarea').clear()
    driver.find_element(By.XPATH, '/html/body/div[2]/div/section/div/div[2]/textarea').send_keys(text_prompt)
    elem = driver.find_element(By.XPATH, '/html/body/div[2]/div/section/div/div[1]/div/div[1]/button')
    elem.click()
    driver.find_element(By.XPATH, '/html/body/div[2]/div/section/div/div[1]/div/div[1]/ul/li[159]/a').click()

    elem = driver.find_element(By.XPATH, '/html/body/div[2]/div/section/div/div[3]/button[2]')

    ac = ActionChains(driver)
    driver.execute_script("window.scrollBy(0, 400);")

    ac.move_to_element(elem).move_by_offset(-150,50).click().perform()

    #download
    time.sleep(20)
    driver.find_element(By.XPATH, '/html/body/div[2]/div/section/div/div[3]/button[2]').click()
    current_datetime = datetime.now()
    time.sleep(45)

    # Format the date and time as per your requirement
    formatted_datetime = current_datetime.strftime("%d-%b-%Y_%H-%M")

    src_path = "C:/Users/louis/Downloads/Text-to-Speech_" + formatted_datetime + ".mp3"

    shutil.move(src_path, dst_path)