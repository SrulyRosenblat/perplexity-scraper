import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options 
from bs4 import BeautifulSoup
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import uuid
import os
from datetime import datetime

# Use a service account.
cred = credentials.Certificate('ai-tracker-a9223-firebase-adminsdk-k10ou-d2c81b8165.json')

app = firebase_admin.initialize_app(cred,{
    'storageBucket': 'ai-tracker-a9223.appspot.com'
})

db = firestore.client()
collection = db.collection('data')
bucket = storage.bucket()

def upload_images(filenames):
    urls = []
    for filename in filenames:
        blob = bucket.blob(f'images/{os.path.basename(filename)}-{uuid.uuid4()}')
        blob.upload_from_filename(filename)
        blob.make_public()
        urls.append(blob.public_url)
    return urls


def clickViewMore(driver):
    """
    Clicks the "View more" element on the page.

    Args:
        driver (selenium.webdriver): The WebDriver instance.

    Returns:
        None

    Raises:
        Exception: If the element is not found or cannot be clicked.
    """
    try:
        # Locate and click the "View more" element
        view_more_element = driver.find_element(By.XPATH, '//div[contains(text(), "View") and contains(text(), "more")]')
        view_more_element.click()
    except Exception as e:
        print(f"Error clicking 'View more' element: {e}")

def extractTextFromAnswer(driver):
    """
    Extracts the text from the answer element on the page.

    Args:
        driver (selenium.webdriver): The WebDriver instance.

    Returns:
        str: The extracted text from the answer element, or None if not found.

    Raises:
        Exception: If the answer element is not found or cannot be accessed.
    """
    try:
        # Locate the answer element and extract its text
        div_element = driver.find_element(By.XPATH, '//div[contains(@class, "relative default font-sans text-base")]')
        return div_element.text
    except Exception as e:
        print(f"Error extracting answer text: {e}")
        return None

def save_screenshot(driver, path: str = 'tmp/screenshot.png') -> None:
    """
    Takes a full-page screenshot and saves it to the specified path.

    Args:
        driver (selenium.webdriver): The WebDriver instance.
        path (str): The file path where the screenshot will be saved.

    Returns:
        None

    Raises:
        Exception: If there's an error during the screenshot process.
    """
    try:
        original_size = driver.get_window_size()
        required_width = driver.execute_script('return document.body.scrollWidth')
        required_height = driver.execute_script('return document.body.scrollHeight')
        
        # Resize window to capture full page
        driver.set_window_size(required_width, required_height + required_height * .2)
        
        # Take screenshot
        driver.find_element('tag name', 'body').screenshot(path)
        
        # Reset window size
        driver.set_window_size(original_size['width'], original_size['height'])
    except Exception as e:
        print(f"Error saving screenshot: {e}")

def extractLinksAndTitles(driver):
    """
    Extracts the links and titles from the page source.

    Args:
        driver (selenium.webdriver): The WebDriver instance.

    Returns:
        list: A list of dictionaries containing 'title', 'url', and 'snippet' for each item.

    Raises:
        Exception: If there's an error during the extraction process.
    """
    try:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        list_items = soup.find_all('a', class_='group flex w-full cursor-pointer items-stretch h-full')

        results = []
        for item in list_items:
            url = item.get('href')
            title = item.find('div', class_='line-clamp-3').get_text(strip=True)
            
            if not title[0].isdigit():
                continue
            title = title[2:]
            
            snippet = item.find('div', class_='line-clamp-4')
            snippet = snippet.get_text(strip=True) if snippet else None
            
            results.append({
                'title': title,
                'url': url,
                'snippet': snippet
            })
        return results
    except Exception as e:
        print(f"Error extracting links and titles: {e}")
        return []

def extractOptions(driver):
    """
    Extracts the options from the page.

    Args:
        driver (selenium.webdriver): The WebDriver instance.

    Returns:
        list: A list of option texts.

    Raises:
        Exception: If there's an error during the extraction process.
    """
    try:
        option_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "group flex cursor-pointer items-center justify-between py-sm")]//div[contains(@class, "default font-sans text-base font-medium text-textMain dark:text-textMainDark")]')
        return [element.text for element in option_elements]
    except Exception as e:
        print(f"Error extracting options: {e}")
        return []

def waitForButtonToAppearAndDisappear(driver, timeout=10):
    """
    Waits for a specific button to appear on the page.

    Args:
        driver (selenium.webdriver): The WebDriver instance.
        timeout (int): Maximum time to wait for the button, in seconds.

    Returns:
        None

    Raises:
        Exception: If the button doesn't appear within the timeout period.
    """
    try:
        button_locator = (By.XPATH, '//button[contains(@class, "bg-offsetPlus") and contains(@class, "cursor-point") and contains(@class, "aspect-square")]')
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(button_locator))
    except Exception as e:
        print(f"Error waiting for button: {e}")

def extractAllSources(driver):
    """
    Extracts all sources from the page.

    Args:
        driver (selenium.webdriver): The WebDriver instance.

    Returns:
        list: A list of dictionaries containing 'source_name', 'snippet', and 'link' for each source.

    Raises:
        Exception: If there's an error during the extraction process.
    """
    try:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        source_divs = soup.find_all('div', class_='flex w-full flex-row-reverse gap-sm')

        sources = []
        for div in source_divs:
            link_tag = div.find('a', href=True)
            link = link_tag['href'] if link_tag else None
            
            snippet_div = div.find('div', class_='line-clamp-4')
            snippet = snippet_div.text.strip() if snippet_div else None
            
            source_name_div = div.find('div', class_='line-clamp-1')
            source_name = source_name_div.text.strip() if source_name_div else None
            
            sources.append({
                'source_name': source_name,
                'snippet': snippet,
                'link': link
            })
        return sources
    except Exception as e:
        print(f"Error extracting sources: {e}")
        return []

def run_scraper(text):
    """
    Runs the scraper to extract information from Perplexity AI based on the given text.

    Args:
        text (str): The question or prompt to input into Perplexity AI.

    Returns:
        None

    Raises:
        Exception: If there's an error during the scraping process.
    """
    # Set up Chrome options
    options = Options()
    options.headless = True
    options.add_argument("--headless")
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(options=options)
    try:
        driver.maximize_window()
        driver.get("https://www.perplexity.ai/")
        
        # Wait for page to load
        print("Step 1/8: Loading page...")
        time.sleep(10)
        
        # Find textarea and input question
        print("Step 2/8: Finding textarea and inputting question...")
        textarea = driver.find_element(By.XPATH, '//textarea[@placeholder="Ask anything..."]')
        textarea.send_keys(text)
        textarea.send_keys(Keys.RETURN)
        
        # Wait for answer to load
        print("Step 3/8: Waiting for answer to load...")
        waitForButtonToAppearAndDisappear(driver, 99)
        time.sleep(40)
        
        # Extract answer and take screenshot
        print("Step 4/8: Extracting answer and taking screenshot...")
        answer = extractTextFromAnswer(driver)
        save_screenshot(driver, 'tmp/full_page.png')
        
        # Extract options and sources
        print("Step 5/8: Extracting options...")
        options = extractOptions(driver)
        print("Step 6/8: Clicking 'View more' and waiting...")
        clickViewMore(driver)
        time.sleep(2)
        print("Step 7/8: Extracting sources and taking screenshot...")
        sources = extractAllSources(driver)
        save_screenshot(driver, 'tmp/sources_page.png')
        
        # Save results to JSON file
        print("Step 8/8: Saving results to JSON file...")
        url = driver.current_url
        title = driver.title
        urls = upload_images([f'tmp/full_page.png',f'tmp/sources_page.png'])
        collection.add({
            'title': title,
            'url': url,
            'image_urls': urls,
            'options': options,
            'sources': sources,
            'question': text,
            'answer':answer,
            'timestamp': datetime.now().isoformat()
        })



    except Exception as e:
        print(f"Error in run_scraper: {e}")
    finally:
        driver.quit()


