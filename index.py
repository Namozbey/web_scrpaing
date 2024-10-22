# from selenium import webdriver

# driver = webdriver.Chrome()  # or use Firefox, etc.
# driver.get('https://www.wg-gesucht.de/en/wg-zimmer-in-Muenchen.90.0.1.0.html')

# # Extract some data
# title = driver.title
# print(title)

# driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

data = []

# Initialize WebDriver (make sure the path to ChromeDriver is correct)
driver = webdriver.Chrome()  # Or you can specify the full path to chromedriver if needed

# Open the website
url = 'https://www.wg-gesucht.de'
driver.get(url)

# Wait for the page to load fully (you may need to adjust the time)
time.sleep(5)

# Accept essentials
accept_elm = driver.find_element(By.ID, 'cmpwelcomebtnyes')
accept_btn = accept_elm.find_element(By.TAG_NAME, "a")
accept_btn.click()

# Search for listings (for example, using a specific URL for the rental listings)
driver.get('https://www.wg-gesucht.de/en/wg-zimmer-in-Muenchen.90.0.1.0.html')

# Allow time for the page to fully load
time.sleep(5)

list_wrapper = driver.find_element(By.ID, 'main_column')

# Find elements containing the title, description, price, and location
# Adjust the XPath/CSS selectors according to the structure of the website

# Extract listing details
# listings = driver.find_elements(By.CLASS_NAME, 'wgg_card')  # Listing container class
listings = driver.find_elements(By.XPATH, "//div[contains(@class, 'wgg_card') and not(ancestor::div[contains(@class, 'premium_user_extra_list')])]")

for listing in listings:
    try:
        obj = {}

         # Part 1: Extract title from h3 > a
        title = listing.find_element(By.CSS_SELECTOR, 'div.row.noprint > div:first-child > h3 > a').text
        print(f"Title: {title}")
        obj["title"] = title

        # Part 2: Extract description from second-child span
        description = listing.find_element(By.CSS_SELECTOR, 'div.row.noprint > div:nth-child(2) span:first-child').text
        print(f"Description: {description}")
        obj["description"] = description

        # Part 3: Extract list of alt attributes from images in the second child
        imgs = listing.find_elements(By.CSS_SELECTOR, 'div.row.noprint > div:nth-child(2) > span:nth-child(2) img')
        people = [img.get_attribute('alt') for img in imgs]
        obj["people"] = people
        print(f"Image Alts: {people}")

        # Part 4: Extract price, date, and area from .row.noprint.middle
        price = listing.find_element(By.CSS_SELECTOR, 'div.row.noprint.middle > div:nth-child(1)').text
        date = listing.find_element(By.CSS_SELECTOR, 'div.row.noprint.middle > div:nth-child(2)').text
        area = listing.find_element(By.CSS_SELECTOR, 'div.row.noprint.middle > div:nth-child(3)').text
        print(f"Price: {price}, Date: {date}, Area: {area}")
        
        obj["price"] = price
        obj["date"] = date
        obj["area"] = area

        data.append(obj)

        print('-' * 40)
    except Exception as e:
        print(f"Error scraping listing: {e}")

# Close the browser
driver.quit()

# Write to data.txt
f = open("data.json", "w")
f.write(json.dumps(data))
f.close()