import sys
import json
from src.scrape import *
from src.firebase_utils import upload_to_firebase


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <category> <category_id> <url>")
        print("Category: addons, textures, maps")
        print(
            "Example: python3 main.py addons addon1 https://mcpedl.com/the-fates-intertwined/"
        )
        return

    category = sys.argv[1]
    category_id = sys.argv[2] if len(sys.argv) > 2 else None
    url = sys.argv[3] if len(sys.argv) > 3 else None

    # Validate category if provided
    valid_categories = ["addons", "textures", "maps"]
    if category and category not in valid_categories:
        print(f"Invalid category. Must be one of: {', '.join(valid_categories)}")
        return

    print(f"Scraping: {url}")

    data = scrape_mcpedl_addon(url)

    if not data:
        print("Failed to scrape the page.")
        return

    # print(f"Title: {data['title']}")

    # Upload directly to Firebase
    success = upload_to_firebase(data, category_id, category)

    if success:
        print("Data successfully uploaded to Firebase!")
    else:
        print("Failed to upload to Firebase.")

        # Save URL + addonID as plain text backup (append)
        backup_filename = "output/failed_uploads.txt"
        with open(backup_filename, "a", encoding="utf-8") as f:
            f.write(f"{category_id} | {url}\n")
        print(f"Backup saved to: {backup_filename}")


if __name__ == "__main__":
    main()
