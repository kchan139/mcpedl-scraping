import sys
import json
from src.scrape import *
from src.firebase_utils import upload_to_firebase


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <url> [category] [addon_id]")
        print("Category: addons, textures, maps")
        print(
            "Example: python3 main.py https://mcpedl.com/the-fates-intertwined/ addons my_addon_1"
        )
        return

    url = sys.argv[1]
    category = sys.argv[2] if len(sys.argv) > 2 else None
    addon_id = sys.argv[3] if len(sys.argv) > 3 else None

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

    print(f"Title: {data['title']}")

    # Upload directly to Firebase
    success = upload_to_firebase(data, addon_id, category)

    if success:
        print("Data successfully uploaded to Firebase!")
    else:
        print("Failed to upload to Firebase.")

        # Optionally save to local JSON as backup
        output_filename = "output/mcpedl_data.json"
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Data saved locally to: {output_filename}")


if __name__ == "__main__":
    main()
