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
