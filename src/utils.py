import os
import json

def extract_to_txt(filename, output_dir="output"):    
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(filename))[0]}.txt")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # Extract title and URL
        title = json_data["title"]
        url = json_data["url"]
        
        # Extract content from description_field
        content_to_skip = [
            # Hard coded
            "Spoiler", ',', '.'
        ]
        content_items = []
        for item in json_data["description_field"]:
            if item["type"] == "text":
                if item["content"] in content_to_skip:
                    continue
                content_items.append(item["content"])
            elif item["type"] in ["image", "youtube"]:
                content_items.append(f"{item['url']}")
        
        content = "\n".join(content_items)
        
        # Write to text file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"Title: {title}\n")
            f.write(f"URL: {url}\n")
            f.write("\nContent:\n")
            f.write(content)
        
        print(f"Data successfully written to {output_file}")
        return True
    
    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")
        return False