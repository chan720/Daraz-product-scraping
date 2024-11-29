from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import os

# Selenium section: Scraping product HTML files
driver = webdriver.Chrome()
query = 'laptop'
url = f'https://www.daraz.pk/catalog/?page=1&q={query}&spm=a2a0e.tm80335142.search.d_go'
file = 0

try:
    # Open the URL
    driver.get(url)

    # Wait until elements with class name "Bm3ON" are visible (adjust timeout as needed)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "Bm3ON"))
    )

    # Find elements and save HTML
    elems = driver.find_elements(By.CLASS_NAME, "Bm3ON")
    for elem in elems:
        d = elem.get_attribute("outerHTML")
        os.makedirs("data", exist_ok=True)  # Ensure the "data" directory exists
        with open(f"data/{query}_{file}.html", "w", encoding="utf-8") as f:
            f.write(d)
        file += 1

finally:
    # Close the driver
    driver.quit()

# BeautifulSoup section: Parsing saved HTML files and writing to CSV
data_dir = "data"
output_file = 'product.csv'

with open(output_file, 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Title', 'Price']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for file in os.listdir(data_dir):
        try:
            file_path = os.path.join(data_dir, file)
            with open(file_path, "r", encoding='utf-8') as f:
                html_doc = f.read()

            soup = BeautifulSoup(html_doc, 'html.parser')
            product = soup.find('a', title=True)['title']
            price = soup.find('span', class_='ooOxS')

            # Write extracted data to CSV
            writer.writerow({'Title': product, 'Price': price.text.strip()})
        except Exception as e:
            print(f"Error processing {file}: {e}")
