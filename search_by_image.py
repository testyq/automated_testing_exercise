# coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from time import sleep
import os

# Configuration for visiting the specific search result
VISIT_RESULT = 3

# The search results on my computer screen are 4 columns and you can adjust this  setting according to your screen size
SEARCH_RESULT_COLUMN_NUM = 4


def search_by_image(image_path):
    # Create web driver instance
    service = Service(executable_path="/usr/local/bin/chromedriver")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Open Google Images
        driver.get("https://images.google.com/")

        # Wait for the 'Search by image' button to appear
        condition_1 = EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[3]/div[3]"))
        WebDriverWait(driver, timeout=3, poll_frequency=0.5).until(condition_1)
        driver.maximize_window()

        # Find the 'Search by image' button and click it
        search_by_image_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[3]/div[3]")
        search_by_image_button.click()

        # Wait for the words Upload Picture to appear
        wait_condition_2 = EC.visibility_of_element_located(
            (By.XPATH, "//*[@id='ow9']/div[3]/c-wiz/div[2]/div/div[3]/div[2]/div/div[2]/span"))
        WebDriverWait(driver, timeout=5, poll_frequency=0.5).until(wait_condition_2)

        # Upload the image
        image_input = driver.find_element(By.NAME, "encoded_image")
        image_input.send_keys(image_path)
        image_input.submit()

        # Wait for search results to load
        wait_condition_3 = EC.visibility_of_element_located(
            (By.ID, 'yDmH0d'))
        WebDriverWait(driver, timeout=5, poll_frequency=0.5).until(wait_condition_3)

        # Calculate the image position in the search result
        result_image_column = VISIT_RESULT % SEARCH_RESULT_COLUMN_NUM
        result_image_offset = int(VISIT_RESULT / SEARCH_RESULT_COLUMN_NUM) + 1

        # Click on the specified result
        result_xpath = f"//*[@id='yDmH0d']/c-wiz/div/div[2]/div/c-wiz/div/div[2]/c-wiz/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div[{result_image_column}]/div[{result_image_offset}]/div/a/div/div[1]/div/img"
        result_element = driver.find_element(By.XPATH, result_xpath)
        result_element.click()
        sleep(5)

        # Switch to new window
        current_window = driver.current_window_handle
        all_windows = driver.window_handles

        for window in all_windows:
            if window != current_window:
                driver.switch_to.window(window)

        # Delete the original image before saving the screenshot
        screen_shot_name = "last_visited_page.png"
        screen_shot_path = f"./{screen_shot_name}"
        if os.path.exists(screen_shot_path):
            os.remove(screen_shot_path)

        # Take a screenshot of the last visited page
        driver.save_screenshot("last_visited_page.png")

        # Validate that the search results are related to the used image
        validate_search_results(driver.page_source)

    finally:
        # Close the browser
        driver.quit()


def validate_search_results(page_source):
    # Check if relevant keywords are present in the HTML content
    relevant_keywords = ["happy", "life"]

    soup = BeautifulSoup(page_source, 'html.parser')
    page_text = soup.get_text().lower()

    for keyword in relevant_keywords:
        if keyword in page_text:
            print(f"Validation successful. Found '{keyword}' in the search results.")
        else:
            print(f"Validation failed. '{keyword}' not found in the search results.")


if __name__ == "__main__":
    cwd = os.getcwd()
    image_absolute_path = cwd + '/test_image.jpg'
    search_by_image(image_absolute_path)
