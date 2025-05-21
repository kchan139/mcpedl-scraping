import sys
import json
from src.scrape import *
from src.utils import extract_to_txt

def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print("Usage: python3 main.py <url>")
        print("Example: python3 main.py https://mcpedl.com/the-fates-intertwined/")
        return
    
    print(f"Scraping: {url}")
    
    data = scrape_mcpedl_addon(url)
    
    if not data:
        print("Failed to scrape the page.")
        return
    
    output_filename = "output/mcpedl_data.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("\nScraping Summary:")
    print(f"Title: {data['title']}")
    print(f"Data saved to: {output_filename}")

    extract_to_txt(output_filename)

if __name__ == "__main__":
    main()