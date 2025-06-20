from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import random
import json

# Helpers
def read_comments_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def random_delay(min_delay=0.5, max_delay=2):
    time.sleep(random.uniform(min_delay, max_delay))

def init_driver():
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(100)
    return driver

def find_element_by_multiple_attributes(driver, tag_name, attributes):
    for attribute in attributes:
        try:
            return WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f"{tag_name}[{attribute}]"))
            )
        except TimeoutException:
            continue
    return None

def dofollow(urls, comment_file):
    driver = init_driver()
    comment_data = read_comments_from_file(comment_file)

    for url in urls:
        try:
            driver.get(url)
            selected_comment = random.choice(comment_data)

            comment_field = find_element_by_multiple_attributes(driver, 'textarea', ['data-sf-role=comments-new-message', 'placeholder=Leave a comment'])
            if comment_field:
                random_delay(2, 4)
                comment_field.clear()
                random_delay()
                comment_field.send_keys(selected_comment["komentar"])

            name_field = find_element_by_multiple_attributes(driver, 'input', ['data-sf-role=comments-new-name', 'placeholder=Your name'])
            if name_field:
                name_field.clear()
                random_delay()
                name_field.send_keys(selected_comment["nama"])

            email_field = find_element_by_multiple_attributes(driver, 'input', ['data-sf-role=comments-new-email', 'placeholder=Email (optional)'])
            if email_field:
                email_field.clear()
                random_delay()
                email_field.send_keys(selected_comment["email"])

            try:
                submit_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-sf-role="comments-new-submit-button"]'))
                )
                random_delay()
                submit_button.click()
                print(f"Comment successful > {url}")
            except TimeoutException:
                print(f"Comment failed > {url}")

            time.sleep(3)
        except WebDriverException:
            print(f"An error occurred > {url}")
            continue

    driver.quit()
    print("All dofollow URLs have been processed.")

def nofollow(urls, comment_file):
    driver = init_driver()
    comment_data = read_comments_from_file(comment_file)

    for url in urls:
        try:
            driver.get(url)
            selected_comment = random.choice(comment_data)

            comment_section = find_element_by_multiple_attributes(driver, 'form', ['id=comment', 'class=comment-form', 'name=comment'])
            if not comment_section:
                print(f"No comment form found > {url}")
                continue

            name_field = find_element_by_multiple_attributes(driver, 'input', ['id=author', 'name=author', 'class=name'])
            if name_field:
                name_field.clear()
                random_delay()
                name_field.send_keys(selected_comment["nama"])

            email_field = find_element_by_multiple_attributes(driver, 'input', ['id=email', 'name=email', 'class=email'])
            if email_field:
                email_field.clear()
                random_delay()
                email_field.send_keys(selected_comment["email"])

            website_field = find_element_by_multiple_attributes(driver, 'input', ['id=url', 'name=url', 'class=website'])
            if website_field:
                website_field.clear()
                random_delay()
                website_field.send_keys(selected_comment["website"])

            comment_field = find_element_by_multiple_attributes(driver, 'textarea', ['id=comment', 'name=comment', 'class=comment'])
            if comment_field:
                comment_field.clear()
                random_delay()
                comment_field.send_keys(selected_comment["komentar"])

            submit_button = find_element_by_multiple_attributes(driver, 'input', ['id=submit', 'name=submit', 'type=submit', 'class=submit'])
            if not submit_button:
                submit_button = find_element_by_multiple_attributes(driver, 'button', ['type=submit', 'class=submit', 'id=submit'])

            if submit_button:
                submit_button.click()
                print(f"Comment successful > {url}")
            else:
                print(f"Comment failed > {url}")

            time.sleep(3)
        except WebDriverException:
            print(f"An error occurred > {url}")
            continue

    driver.quit()
    print("All nofollow URLs have been processed.")

def main():
    print("Running automated comment bot...")
    choice = "1"  # hardcoded for automation

    if choice == "1":
        urls = [
           "https://appeals.cuyahogacounty.gov/about-us/judges/judge-sean-c-gallagher/eighth-district-court-of-appeals",
                
                ]  # Replace with real dofollow URLs
        dofollow(urls, "dofollow.json")
    elif choice == "2":
        urls = [
            "https://www.ub.edu/multilingua/resultats-de-la-matricula-de-rosetta-stone/",
        
          # Replace with real nofollow URLs
        nofollow(urls, "nofollow.json")

if __name__ == "__main__":
    main()
