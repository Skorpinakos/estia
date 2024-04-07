import re

def split_string_by_delimiters(string, delimiters):
    # Escape special characters in delimiters and join them into a regex pattern
    regex_pattern = '|'.join([re.escape(delimiter) for delimiter in delimiters])
    
    # Split the string by the constructed RegExp
    return list(filter(bool, re.split(regex_pattern, string)))


def process_string(input_string):
    # Replace all \n with spaces and remove multiple spaces
    updated_string = re.sub(r'\s+', ' ', input_string.replace('\n', ' '))
    
    # Find all indexes where "ή" appears followed by a space and a Greek capital letter and replace with "$"
    updated_string = re.sub(r'ή (?=[Α-Ω])', '$', updated_string)
    
    # Replace parentheses with spaces
    return updated_string.replace("(", " ").replace(")", " ")


def parse_menus(menus_text):
    menus_structured = {}

    breakfast = menus_text[0].lower()
    lunch = process_string(menus_text[1]).lower()
    dinner = process_string(menus_text[2]).lower()

    breakfast_items = breakfast.split(',')
    breakfast_items = [item.strip() for item in breakfast_items]
    breakfast_drinks = breakfast_items[:4]
    if breakfast_items[-1] != "τυρί":
        breakfast_main = breakfast_items[-1]
        breakfast_slices = breakfast_items[4:-1]
    else:
        breakfast_main = breakfast_items[-2] + "-" + breakfast_items[-1]
        breakfast_slices = breakfast_items[4:-2]
    breakfast_parts = [breakfast_main, ', '.join(breakfast_slices), ', '.join(breakfast_drinks)]

    split_words = ["πρώτο πιάτο", "κυρίως πιάτο", "μπουφές σαλάτα", "επιδόρπιο"]

    lunch = lunch.replace("-", " ").replace("\n", " ").replace(":", "")
    lunch_parts = [item.strip() for item in split_string_by_delimiters(lunch, split_words)]

    dinner = dinner.replace("-", " ").replace("\n", " ").replace(":", "")
    dinner_parts = [item.strip() for item in split_string_by_delimiters(dinner, split_words)]

    menus_structured = {"lunch": lunch_parts, "dinner": dinner_parts, "breakfast": breakfast_parts}
    return menus_structured

def refine_commas(input_string):
    # Removes spaces before commas, ensures one space after each comma,
    # deletes trailing commas only followed by whitespaces, and trims the string.
    input_string = re.sub(r'\s*,\s*', ', ', input_string)
    input_string = re.sub(r',+\s*$', '', input_string)
    return input_string.strip()

def capitalize_first_letter(string):
    # Capitalizes the first letter of the string, after trimming.
    return string.strip()[0].upper() + string.strip()[1:] if string else ''

def capitalize_after_br(html_string):
    # Capitalizes the letter immediately following every <br><br>.
    def capitalize_match(match):
        return match.group(1) + match.group(2).upper()
    return re.sub(r'(<br><br>)(.)', capitalize_match, html_string)

def process_menu_item_text(item):
    # Processes a single menu item string with the defined operations.
    processed_item = capitalize_first_letter(item)
    #print(processed_item)
    processed_item = processed_item.replace('$', '<br><br>')
    processed_item = capitalize_after_br(processed_item)
    processed_item = refine_commas(processed_item)
    processed_item = processed_item.replace('<br><br>', '</p><hr><p>')
    return processed_item

def process_all_menu_items(menus):
    # Processes all menu items given a dictionary of meal types and items.
    processed_menus = {}
    for meal_type, menu_items in menus.items():
        processed_menus[meal_type] = [process_menu_item_text(item) for item in menu_items]
    return processed_menus