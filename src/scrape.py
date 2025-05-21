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
            'description_field': None,
            'images': [],
        }
        
        # Extract title
        try:
            title_elem = driver.find_element(By.TAG_NAME, 'h1')
            data['title'] = title_elem.text.strip()
        except:
            pass
        
        # Extract description field content in exact order - text and image links only
        try:
            description_field = driver.find_element(By.CSS_SELECTOR, '.description-field')
            
            # Use JavaScript to extract content in order
            ordered_content = driver.execute_script("""
                function extractContent(element) {
                    let result = [];
                    
                    // Process all child nodes recursively
                    function processNode(node) {
                        if (node.nodeType === Node.TEXT_NODE) {
                            const text = node.textContent.trim();
                            if (text) result.push({ type: 'text', content: text });
                        } else if (node.nodeType === Node.ELEMENT_NODE) {
                            // Handle images
                            if (node.tagName === 'IMG') {
                                const src = node.src;
                                if (src && !src.startsWith('data:image/png;')) {
                                    result.push({ type: 'image', url: src });
                                }
                            }
                            // Handle iframes (YouTube embeds)
                            else if (node.tagName === 'IFRAME') {
                                const src = node.src;
                                if (src && (src.includes('youtube.com') || src.includes('youtu.be'))) {
                                    result.push({ type: 'youtube', url: src });
                                }
                            }
                            // Handle links to YouTube
                            else if (node.tagName === 'A') {
                                const href = node.href;
                                if (href && (href.includes('youtube.com') || href.includes('youtu.be'))) {
                                    result.push({ type: 'youtube_link', url: href, text: node.textContent.trim() });
                                }
                            }
                            // Process children recursively
                            for (const child of node.childNodes) {
                                processNode(child);
                            }
                        }
                    }
                    
                    // Start processing from the element
                    for (const child of element.childNodes) {
                        processNode(child);
                    }
                    
                    return result;
                }
                
                return extractContent(arguments[0]);
            """, description_field)
            
            data['description_field'] = ordered_content
            
        except Exception as e:
            print(f"Failed to extract description field: {e}")
            data['description_field'] = None
        
        return data
    
    except Exception as e:
        print(f"Error: {e}")
        return None
    
    finally:
        driver.quit()