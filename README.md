# MCPEDL Scraper

A lightweight Python utility for scraping addon information from MCPEDL (Minecraft PE/Bedrock Edition downloads) website.

## Features

- Scrapes addon pages from mcpedl.com
- Extracts title, description text, and media URLs
- Saves data as structured JSON
- Converts content to plain text format

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/kchan139/mcpedl-scraping.git
   cd kchan139-mcpedl-scraping
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the scraper with a MCPEDL URL:

```
python main.py https://mcpedl.com/addon-name/
```

Output files will be stored in the `output` directory:
- `mcpedl_data.json` - Complete structured data
- `mcpedl_data.txt` - Simplified text version with title, URL, and content


## Requirements

- Python 3.6+
- Chrome/Chromium browser (for Selenium WebDriver)

## Legal Notice

This tool is for personal use only. Please respect MCPEDL's Terms of Service and use responsibly with reasonable request rates. Content from MCPEDL may be subject to copyright protection. The author assumes no liability for misuse of this tool.