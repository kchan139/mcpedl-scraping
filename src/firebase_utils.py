import firebase_admin
from firebase_admin import credentials, db
from bs4 import BeautifulSoup
import json
import os


def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    # Check if Firebase is already initialized
    if not firebase_admin._apps:
        # You need to put your service account key JSON file in the project root
        # Download it from Firebase Console -> Project Settings -> Service Accounts
        cred = credentials.Certificate("../top-secret.json")

        firebase_admin.initialize_app(
            cred, {"databaseURL": "https://mcpe-addon.firebaseio.com"}
        )


def clean_html(content):
    """Clean HTML content and return plain text"""
    soup = BeautifulSoup(str(content), "html.parser")
    clean_content = soup.get_text(separator="\n", strip=True)
    return clean_content


def process_content_fields(introduction_field, description_field):
    """Process introduction and description fields into desData array"""
    content_to_skip = [
        "Spoiler",
    ]

    # Convert to lowercase for comparison
    content_to_skip = [item.lower() for item in content_to_skip]

    content_items = []

    # Process introduction field
    if introduction_field:
        for item in introduction_field:
            if item["type"] == "text":
                if item["content"].lower() in content_to_skip:
                    continue
                content_items.append(item["content"])
            elif item["type"] in ["image", "youtube"]:
                content_items.append(f"{item['url']}")

    # Process description field
    if description_field:
        for item in description_field:
            if item["type"] == "text":
                if item["content"].lower() in content_to_skip:
                    continue
                content_items.append(item["content"])
            elif item["type"] in ["image", "youtube"]:
                content_items.append(f"{item['url']}")

    # Clean HTML from each content item
    cleaned_content = []
    for item in content_items:
        cleaned_item = clean_html(item)
        if cleaned_item.strip():  # Only add non-empty content
            cleaned_content.append(cleaned_item)

    return cleaned_content


def determine_category(url, title, post_tags):
    """Determine if the addon is addon, texture, or map based on URL, title, or tags"""
    url_lower = url.lower()
    title_lower = title.lower() if title else ""
    tags_lower = post_tags.lower() if post_tags else ""

    # Check for textures/resource packs
    texture_keywords = ["texture", "resource pack", "skin", "shader"]
    if any(
        keyword in url_lower or keyword in title_lower or keyword in tags_lower
        for keyword in texture_keywords
    ):
        return "textures"

    # Check for maps
    map_keywords = ["map", "world", "seed"]
    if any(
        keyword in url_lower or keyword in title_lower or keyword in tags_lower
        for keyword in map_keywords
    ):
        return "maps"

    # Default to addons
    return "addons"


def upload_to_firebase(data, addon_id=None, category=None):
    """Upload scraped data to Firebase Realtime Database"""
    try:
        initialize_firebase()

        # Get database reference
        ref = db.reference()

        # Process the data
        title = data.get("title", "")
        post_tags = data.get("post_tags", "")
        introduction_field = data.get("introduction_field", [])
        description_field = data.get("description_field", [])

        # Process content fields
        des_data = process_content_fields(introduction_field, description_field)

        # Use provided category or determine automatically
        if not category:
            category = determine_category(data.get("url", ""), title, post_tags)

        # Create addon entry
        addon_entry = {
            "activated": 1,
            "desData": des_data,
            "introduction": title,
            "tag": post_tags if post_tags else "",
        }

        # Generate addon ID if not provided
        if not addon_id:
            # Use a timestamp-based ID or generate from title
            import time

            addon_id = f"addon_{int(time.time())}"

        # Upload to Firebase
        ref.child(category).child(addon_id).set(addon_entry)

        print(f"Successfully uploaded to Firebase under {category}/{addon_id}")
        print(f"Title: {title}")
        print(f"Category: {category}")
        print(f"Content items: {len(des_data)}")

        return True

    except Exception as e:
        print(f"Error uploading to Firebase: {e}")
        return False


def get_firebase_data(category=None, addon_id=None):
    """Retrieve data from Firebase (useful for testing)"""
    try:
        initialize_firebase()
        ref = db.reference()

        if category and addon_id:
            return ref.child(category).child(addon_id).get()
        elif category:
            return ref.child(category).get()
        else:
            return ref.get()

    except Exception as e:
        print(f"Error retrieving from Firebase: {e}")
        return None
