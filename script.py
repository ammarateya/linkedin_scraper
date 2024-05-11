import csv, os, sys, time
from typing import List, Tuple

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

# Load environment variables from .env file
load_dotenv()

# Path to ChromeDriver
CHROMEDRIVER_PATH = "./chromedriver-mac-arm64/chromedriver"
# Put in your LinkedIn login details
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def extract_comments(driver, post_url: str) -> List[Tuple[str, str, str, str]]:
    """
    Extract comments from a LinkedIn post.

    Arguments:
        driver (webdriver.Chrome): Selenium Chrome driver instance.
        post_url (str): URL of the LinkedIn post.

    returns:
        List[Tuple[str, str, str, str]]: A list of tuples containing (name, profile_url, position, comment_text).
    """
    comments = []

    # Navigate to the page
    driver.get(post_url)
    time.sleep(3)  # Let it load

    # Scroll to load all comments
    while True:
        try:
            more_comments_button = driver.find_element_by_class_name("comments-comments-list__load-more-comments-button")
            more_comments_button.click()
            time.sleep(2)
        except NoSuchElementException:
            break

    # Find the container for all comments
    comments_container = driver.find_element_by_class_name("comments-comments-list--expanded")
    
    # Extract comments
    comment_elements = comments_container.find_elements_by_class_name("comments-comments-list__comment-item")
    for comment_element in comment_elements:
        try:
            name_element = comment_element.find_element_by_class_name("comments-post-meta__name-text")
            name = name_element.find_element_by_xpath(".//span[@aria-hidden='true']").text
            profile_url = comment_element.find_element_by_class_name("app-aware-link").get_attribute("href")
            position = comment_element.find_element_by_class_name("comments-post-meta__headline").text
            text = comment_element.find_element_by_class_name("update-components-text").text
            comments.append((name, profile_url, position, text))
        except NoSuchElementException as e:
            print(f"Error extracting comment data: {str(e)}")

    return comments


def main():
    try:
        # Accepting LinkedIn post URL from command line
        if len(sys.argv) != 2:
            print("Usage: python script.py <linkedin_post_url>")
            sys.exit(1)

        post_url = sys.argv[1]

        # Setting up Chrome WebDriver
        print("Initializing Chrome WebDriver...")
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--incognito")
        # options.add_argument("--headless")  # Optional: Run Chrome in headless mode, hiding the actual GUI, which is faster
        driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
        print("Chrome WebDriver initialized successfully.")

        # Opening LinkedIn and logging in
        print("Opening LinkedIn...")
        driver.get("https://www.linkedin.com/login")
        print("LinkedIn page opened.")

        email_input = driver.find_element_by_id("username")
        email_input.send_keys(EMAIL)
        password_input = driver.find_element_by_id("password")
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)
        print("Logged into LinkedIn.")

        time.sleep(5)  # Show the page

        # Extract comments
        print("Extracting comments...")
        comments = extract_comments(driver, post_url)
        print(f"Extracted {len(comments)} comments from the post.")

        if comments:
            # Save comments to a CSV file
            with open("comments.csv", "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Name", "Profile URL", "Position", "Comment Text"])
                writer.writerows(comments)

            print("Data saved to comments.csv.")
        else:
            print("No comments found on the post.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        if 'driver' in locals():
            # Close the browser
            driver.quit()
            print("Chrome WebDriver closed.")

if __name__ == "__main__":
    main()
