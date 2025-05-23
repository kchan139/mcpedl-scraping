import os
import time
import random
from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from webdriver_manager.chrome import ChromeDriverManager # type: ignore

def scrape_mcpedl_addon(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        time.sleep(random.uniform(1, 3))
        
        data = {
            'url': url,
            'title': None,
            'introduction_field': None,
            'description_field': None,
            'post_tags': None,
        }
        
        # Extract title
        try:
            title_elem = driver.find_element(By.TAG_NAME, 'h1')
            data['title'] = title_elem.text.strip()
        except:
            pass
        
        # Extract introduction field content in exact order - text and image links only
        try:
            introduction_field = driver.find_element(By.CSS_SELECTOR, '.introduction-field')
            
            # Use JavaScript to extract content in order
            js_file_path = os.path.join(os.path.dirname(__file__), 'extract_content.js')
            with open(js_file_path, 'r') as f:
                js_script = f.read()

            ordered_content = driver.execute_script(js_script + "return extractContent(arguments[0]);", introduction_field)
            
            data['introduction_field'] = ordered_content
            
        except Exception as e:
            print(f"Failed to extract introduction field: {e}")
            data['introduction_field'] = None
        
        # Extract description field content in exact order - text and image links only
        try:
            description_field = driver.find_element(By.CSS_SELECTOR, '.description-field')
            
            # Use JavaScript to extract content in order
            js_file_path = os.path.join(os.path.dirname(__file__), 'extract_content.js')
            with open(js_file_path, 'r') as f:
                js_script = f.read()

            ordered_content = driver.execute_script(js_script + "return extractContent(arguments[0]);", description_field)
            
            data['description_field'] = ordered_content
            
        except Exception as e:
            print(f"Failed to extract description field: {e}")
            data['description_field'] = None
        
        # Extract post tags
        try:
            post_tags_elem = driver.find_element(By.CSS_SELECTOR, 'p.post-tags')
            data['post_tags'] = post_tags_elem.text.strip()
        except Exception as e:
            print(f"No post-tags element.")
            data['post_tags'] = None
        
        return data
    
    except Exception as e:
        print(f"Error: {e}")
        return None
    
    finally:
        driver.quit()