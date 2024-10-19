import logging
import traceback
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # Import Keys to simulate keyboard actions
from src.browser import BrowserAutomation  # Import the BrowserAutomation class

class LinkedInAutomation(BrowserAutomation):
    def __init__(self, profile_path):
        super().__init__(profile_path)  # Call the parent constructor with profile path

    def open_linkedin(self) :
        LOGIN_URL = "https://www.linkedin.com/login"
        self.open_website(LOGIN_URL)
    
    def login(self, username: str, password: str):
        """Login to LinkedIn using provided credentials."""
        LOGIN_URL = "https://www.linkedin.com/login"  # LinkedIn login URL
        self.open_website(LOGIN_URL)  # Open the LinkedIn login page

        try:
            # Wait for the username and password fields to be visible
            username_field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "username"))
            )
            password_field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "password"))
            )

            # Enter the credentials
            username_field.send_keys(username)  # Enter username
            password_field.send_keys(password)  # Enter password
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()  # Click the login button
            
            self.logger.info("Attempted to log in to LinkedIn.")
            
            # Wait for the login to complete by checking for the feed URL
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("feed")
            )
            self.logger.info("Login successful.")
        except Exception as e:
            self.logger.error(f"Error during login: {e}")
            self.logger.debug(traceback.format_exc())  # Log full traceback

    def isLogin(self) :
        if "feed" in self.driver.current_url:
            return True
        
        return False

    def search(self, keyword: str, datePosted : str = 'past-week', 
               sortedBy : str = 'relvance'):
        """Search LinkedIn for the given keyword."""
        try:
            url = "".join([
            "https://www.linkedin.com/search/results/content/?",
              f'datePosted="{datePosted}"&',
              f'keywords={keyword}&',
              f'sortBy="{sortedBy}"'
            ])
            print(url)
            self.driver.get(url=url)
            return
            # Locate the search bar and enter the keyword
            search_bar = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search']"))
            )
            search_bar.clear()  # Clear any existing text
            search_bar.send_keys(keyword)  # Type the keyword
            search_bar.send_keys(Keys.RETURN)  # Simulate pressing the Enter key
            
            self.logger.info(f"Searching for: {keyword}")

            # Wait for the search results to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".search-results"))
            )

            # Optionally, you could scrape the search results here or return the results
            self.logger.info("Search results loaded successfully.")
        except Exception as e:
            self.logger.error(f"Error during search: {e}")
            self.logger.debug(traceback.format_exc())  # Log full traceback

    def scrape_profile(self, profile_url: str):
        """Scrape a LinkedIn profile."""
        self.open_website(profile_url)  # Open the LinkedIn profile page

        try:
            # Wait for the profile name and headline to be visible
            profile_name = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1'))
            ).text  # Replace with the actual selector
            
            profile_headline = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.pv-top-card--headline'))
            ).text  # Replace with the actual selector
            
            self.logger.info(f"Scraped Profile Name: {profile_name}")
            self.logger.info(f"Scraped Profile Headline: {profile_headline}")

            return {
                'name': profile_name,
                'headline': profile_headline
            }
        except Exception as e:
            self.logger.error(f"Error while scraping profile: {e}")
            self.logger.debug(traceback.format_exc())  # Log full traceback

# Example usage
if __name__ == "__main__":
    USERNAME = "test123@gmail.com"  # Replace with your LinkedIn username
    PASSWORD = "test@123"  # Replace with your LinkedIn password
    PROFILE_URL = "https://www.linkedin.com/in/anandhere08/"  # Replace with a LinkedIn profile URL to scrape
    SEARCH_KEYWORD = "Data Scientist"  # Example keyword to search
    profile_path = os.path.expanduser("~/.config/linkedin")  # Path to your Chrome user data directory
    linkedin_browser = None  # Initialize outside try block for proper cleanup

    try:
        logging.basicConfig(level=logging.INFO)  # Set up logging
        logging.info("Starting LinkedIn automation script.")
        linkedin_browser = LinkedInAutomation(profile_path=profile_path)  # Initialize LinkedIn automation
        linkedin_browser.login(USERNAME, PASSWORD)  # Log in to LinkedIn
        linkedin_browser.search(SEARCH_KEYWORD)  # Perform the search
        profile_data = linkedin_browser.scrape_profile(PROFILE_URL)  # Scrape the profile
        logging.info(f"Profile Data: {profile_data}")
    except KeyboardInterrupt:
        logging.warning("Script interrupted by the user.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        logging.debug(traceback.format_exc())  # Log full traceback
    finally:
        if linkedin_browser:
            linkedin_browser.close_browser()  # Ensure the browser is closed safely
        logging.info("Script execution completed.")
