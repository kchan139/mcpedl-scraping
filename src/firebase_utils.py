import firebase_admin
from firebase_admin import credentials, db
from bs4 import BeautifulSoup
import json
import os


def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    # Check if Firebase is already initialized
    if not firebase_admin._apps:
        # Download it from Firebase Console -> Project Settings -> Service Accounts
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, "..", "top-secret.json")
        cred = credentials.Certificate(json_path)

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

def process_post_tags(post_tags, category):
    """Process post tags to extract and format tag list"""
    if not post_tags:
        return "16x, " if category == "textures" else ", "

    # Remove "Tags: " prefix if present
    if post_tags.startswith("Tags:"):
        tags_part = post_tags[6:]
    else:
        tags_part = post_tags

    # Split by spaces and join with commas
    tags = tags_part.split()
    if tags:
        return ", ".join(tags) + ", "
    else:
        return ", "

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

        # Process post tags
        processed_tags = process_post_tags(post_tags, category)

        # Use provided category or determine automatically
        if not category:
            category = determine_category(data.get("url", ""), title, post_tags)

        # Create addon entry
        addon_entry = {
            "activated": 1,
            "desData": des_data,
            "download": {
                category: ""
            },
            "introduction": title,
            "image": "",
            "tag": processed_tags
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
