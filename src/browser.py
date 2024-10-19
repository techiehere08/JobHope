import os
import logging
import traceback
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class BrowserAutomation:
    def __init__(self, profile_path):
        """Initialize the browser automation with ChromeDriver."""
        # Set up logging
        self.logger = self.setup_logging()

        self.logger.info("Initializing BrowserAutomation class.")

        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")  # Open maximized window
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation detection
        chrome_options.add_argument("--disable-infobars")  # Disable infobars
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model

        # Set the user profile path
        chrome_options.add_argument(f"user-data-dir={profile_path}")  # Path to your Chrome profile

        try:
            # Automatically download and set up ChromeDriver
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            self.logger.info("ChromeDriver initialized and browser launched.")
        except Exception as e:
            self.logger.critical(f"Failed to initialize ChromeDriver: {e}")
            self.logger.debug(traceback.format_exc())  # Log full traceback
            raise  # Reraise the exception to handle it in the main script

    def setup_logging(self):
        """Set up logging to both terminal and a log file inside the 'log' folder."""
        # Ensure the log directory exists
        log_dir = "../log"
        os.makedirs(log_dir, exist_ok=True)

        # Create a timestamped filename for the log file
        log_filename = datetime.now().strftime(f"{log_dir}/log_%Y-%m-%d_%H-%M-%S.log")

        # Create a logger
        logger = logging.getLogger("BrowserAutomation")
        logger.setLevel(logging.DEBUG)  # Set log level

        # Create handlers for terminal and file logging
        stream_handler = logging.StreamHandler()  # Terminal output
        file_handler = logging.FileHandler(log_filename, mode="a")  # Log file

        # Define log format
        log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        stream_handler.setFormatter(log_format)
        file_handler.setFormatter(log_format)

        # Add handlers to the logger
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

        return logger

    def open_website(self, url: str):
        """Open a webpage."""
        try:
            self.driver.get(url)
            self.logger.info(f"Opened website: {url}")
        except Exception as e:
            self.logger.error(f"Failed to open {url}: {e}")
            self.logger.debug(traceback.format_exc())  # Log full traceback

    def close_browser(self):
        """Close the browser."""
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
                self.logger.info("Browser closed successfully.")
            except Exception as e:
                self.logger.error(f"Error while closing the browser: {e}")
                self.logger.debug(traceback.format_exc())  # Log full traceback

# Example usage
if __name__ == "__main__":
    url = "https://www.linkedin.com/"
    import os
import logging
import traceback
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class BrowserAutomation:
    def __init__(self, profile_path):
        """Initialize the browser automation with ChromeDriver."""
        # Set up logging
        self.logger = self.setup_logging()

        self.logger.info("Initializing BrowserAutomation class.")

        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")  # Open maximized window
        # chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation detection
        # chrome_options.add_argument("--disable-infobars")  # Disable infobars
        # chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model

        # Set the user profile path
        chrome_options.add_argument(f"user-data-dir={profile_path}")  # Path to your Chrome profile

        try:
            # Automatically download and set up ChromeDriver
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            self.logger.info("ChromeDriver initialized and browser launched.")
        except Exception as e:
            self.logger.critical(f"Failed to initialize ChromeDriver: {e}")
            self.logger.debug(traceback.format_exc())  # Log full traceback
            raise  # Reraise the exception to handle it in the main script

    def setup_logging(self):
        """Set up logging to both terminal and a log file inside the 'log' folder."""
        # Ensure the log directory exists
        log_dir = "../log"
        os.makedirs(log_dir, exist_ok=True)

        # Create a timestamped filename for the log file
        log_filename = datetime.now().strftime(f"{log_dir}/log_%Y-%m-%d_%H-%M-%S.log")

        # Create a logger
        logger = logging.getLogger("BrowserAutomation")
        logger.setLevel(logging.DEBUG)  # Set log level

        # Create handlers for terminal and file logging
        stream_handler = logging.StreamHandler()  # Terminal output
        file_handler = logging.FileHandler(log_filename, mode="a")  # Log file

        # Define log format
        log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        stream_handler.setFormatter(log_format)
        file_handler.setFormatter(log_format)

        # Add handlers to the logger
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

        return logger

    def open_website(self, url: str):
        """Open a webpage."""
        try:
            self.driver.get(url)
            time.sleep(5)
            self.logger.info(f"Opened website: {url}")
        except Exception as e:
            self.logger.error(f"Failed to open {url}: {e}")
            self.logger.debug(traceback.format_exc())  # Log full traceback

    def close_browser(self):
        """Close the browser."""
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
                self.logger.info("Browser closed successfully.")
            except Exception as e:
                self.logger.error(f"Error while closing the browser: {e}")
                self.logger.debug(traceback.format_exc())  # Log full traceback

# Example usage
if __name__ == "__main__":
    url = "https://www.linkedin.com/"
    profile_path = os.path.expanduser("~/.config/google-chrome")  # Path to your Chrome user data directory
    browser = None  # Initialize outside try block for proper cleanup

    try:
        logging.info("Starting browser automation script.")
        browser = BrowserAutomation(profile_path=profile_path)  # Initialize the browser with a profile
        browser.open_website(url=url)  # Open the specified URL
    except KeyboardInterrupt:
        logging.warning("Script interrupted by the user.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        logging.debug(traceback.format_exc())  # Log full traceback
    finally:
        if browser:
            browser.close_browser()  # Ensure browser is closed safely
        logging.info("Script execution completed.")

    browser = None  # Initialize outside try block for proper cleanup

    try:
        logging.info("Starting browser automation script.")
        browser = BrowserAutomation(profile_path=profile_path)  # Initialize the browser with a profile
        browser.open_website(url=url)  # Open the specified URL
    except KeyboardInterrupt:
        logging.warning("Script interrupted by the user.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        logging.debug(traceback.format_exc())  # Log full traceback
    finally:
        if browser:
            browser.close_browser()  # Ensure browser is closed safely
        logging.info("Script execution completed.")
