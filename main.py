import json
import os

# File to store menu items
JSON_FILE = 'favs.json'

# Items to display in the menu
items = [
    {"name": "Item 1"},
    {"name": "Item 2"},
    {"name": "Item 3o"},
]

def load_items():
    """Load menu items from the JSON file or initialize with default values."""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as file:
            existing_items = json.load(file)
            # Ensure all items have the 'favorite' field
            for item in existing_items:
                if 'favorite' not in item:
                    item['favorite'] = False

            # Create a dictionary for quick lookup by name
            existing_items_dict = {item['name']: item for item in existing_items}
            current_items_names = {item['name'] for item in items}

            # Initialize the list for displaying items
            updated_items = []
            for item in items:
                if item['name'] in existing_items_dict:
                    updated_items.append(existing_items_dict[item['name']])
                else:
                    updated_items.append({'name': item['name'], 'favorite': False})

            return updated_items
    else:
        # Add 'favorite': False to all items
        for item in items:
            item['favorite'] = False
        with open(JSON_FILE, 'w') as file:
            json.dump(items, file, indent=4)
        return items

def save_items(items):
    """Save menu items to the JSON file, preserving old items."""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as file:
            existing_items = json.load(file)
            existing_items_dict = {item['name']: item for item in existing_items}

        # Update existing items with current favorites
        for item in items:
            existing_items_dict[item['name']] = item

        with open(JSON_FILE, 'w') as file:
            json.dump(list(existing_items_dict.values()), file, indent=4)
    else:
        # If the file doesn't exist, just save the items
        with open(JSON_FILE, 'w') as file:
            json.dump(items, file, indent=4)

def display_menu(items, current_index):
    for idx, item in enumerate(items):
        heart = '❤︎' if item['favorite'] else '♡'
        indicator = '>' if idx == current_index else ' '
        print(f"{indicator} {item['name']} {heart}")

def main():
    menu_items = load_items()
    current_index = 0

    while True:
        # Display the menu
        print("\033c", end="")  # Clear the screen
        display_menu(menu_items, current_index)

        # Get user input
        user_input = input("Use 'w' for up, 's' for down, 'enter' to toggle favorite, 'q' to quit: ").strip().lower()

        if user_input == 'w' and current_index > 0:
            current_index -= 1
        elif user_input == 's' and current_index < len(menu_items) - 1:
            current_index += 1
        elif user_input == '' and menu_items:
            menu_items[current_index]["favorite"] = not menu_items[current_index]["favorite"]
            save_items(menu_items)
        elif user_input == 'q':
            break

if __name__ == "__main__":
    main()