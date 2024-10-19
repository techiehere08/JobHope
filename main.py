import os
import logging
import platform
import configparser
import traceback
from datetime import datetime
from dotenv import load_dotenv
from src.linkedin import LinkedInAutomation  # Adjust the import based on your project structure

# Load environment variables from .env file
load_dotenv()

def configure_logging():
    """Configure logging with a filename based on the current datetime."""
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Generate a log filename with the current datetime
    log_filename = datetime.now().strftime("log_%Y-%m-%d_%H-%M-%S.log")
    log_filepath = os.path.join(log_dir, log_filename)

    # Configure logging with the dynamic filename
    logging.basicConfig(
        filename=log_filepath,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logging.getLogger().addHandler(logging.StreamHandler())  # Also log to console

def get_profile_path(profile_name):
    """Get the profile path based on the operating system and profile name."""
    home = os.path.expanduser("~")
    if platform.system() == "Linux":
        return os.path.join(home, ".config", "google-chrome", profile_name)
    elif platform.system() == "Darwin":  # macOS
        return os.path.join(home, "Library", "Application Support", "Google", "Chrome", profile_name)
    elif platform.system() == "Windows":
        return os.path.join(home, "AppData", "Local", "Google", "Chrome", "User Data", profile_name)
    else:
        raise EnvironmentError("Unsupported operating system.")

def read_config(config_file, key='LinkedIn'):
    """Read the profile name and keyword from the config file."""
    config = configparser.ConfigParser()
    config.read(config_file)
    return config[key]

def main():
    # Configure logging
    configure_logging()

    USERNAME = os.getenv("LINKEDIN_USERNAME", "")  # Get username from .env
    PASSWORD = os.getenv("LINKEDIN_PASSWORD", "")  # Get password from .env

    # Read profile name and keyword from config file
    config_file = os.path.join(os.path.dirname(__file__), 'config.ini')  # Adjust the path as needed
    linkedin_config = read_config(config_file)  # Get profile name from config

    profile_name = linkedin_config['profile_name']
    keyword = linkedin_config['keyword']
    date_posted = linkedin_config.get("datePosted","")
    sort_by = linkedin_config.get("sortedBy","")
    profile_path = get_profile_path(profile_name)  # Get profile path based on OS and profile name

    linkedin_browser = None  # Initialize outside try block for proper cleanup
    
    try:
        logging.info("Starting LinkedIn automation script.")
        linkedin_browser = LinkedInAutomation(profile_path=profile_path)  # Initialize LinkedIn automation
        linkedin_browser.open_linkedin()
        # Check if already logged in by verifying current URL
        if not linkedin_browser.isLogin():
            linkedin_browser.login(USERNAME, PASSWORD)  # Log in to LinkedIn
        
        linkedin_browser.search(keyword, datePosted=date_posted, sortedBy=sort_by)

    except KeyboardInterrupt:
        logging.warning("Script interrupted by the user.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        logging.debug(traceback.format_exc())  # Log full traceback
    finally:
        # input()
        if linkedin_browser:
            linkedin_browser.close_browser()  # Ensure the browser is closed safely
        logging.info("Script execution completed.")

if __name__ == "__main__":
    main()

# https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=uipath%20hiring&sortBy=%22relevance%22