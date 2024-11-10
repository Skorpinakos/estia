from menu_parser import parse_menus,process_all_menu_items
import re

def add_space_before_caps(strings):
    # Define a function to insert spaces before capital letters, including Greek uppercase
    def insert_space(s):
        return re.sub(r'(?<!^)(?=[A-ZΑ-Ω])', ' ', s)

    # Apply the function to each string in the list
    return [insert_space(string) for string in strings]

def find_word_order(texts, word1, word2, word3):
    #print(texts)
    #print(texts)
    # Find the first index of each word in the list of texts
    index_word1 = next((i for i, text in enumerate(texts) if word1 in text), None)
    index_word2 = next((i for i, text in enumerate(texts) if word2 in text), None)
    index_word3 = next((i for i, text in enumerate(texts) if word3 in text), None)
    print(index_word3)
    print(word3)
    #print(text)
    # Combine indexes into a list of tuples (index, word_number)
    indexes = [(index_word1, 0), (index_word2, 1), (index_word3, 2)]
    print(indexes)


    # Sort the indexes based on their positions
    indexes.sort()

    # Create an array representing the order of appearance
    order = [None] * 3
    for order_position, (_, word_num) in enumerate(indexes):
        order[word_num] = order_position

    return order


def get_current_menus():
    import requests
    from bs4 import BeautifulSoup

    url = "https://my.upatras.gr"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title_texts = add_space_before_caps([h1.text for h1 in soup.find_all('h1')]) #this check is kinda good but it could get better
    title_texts_filtered=[]
    for i in title_texts:
        if any(substring in i for substring in ["Πρωινό","Γεύμα","Δείπνο"]): 
            title_texts_filtered.append(i)
    title_texts=title_texts_filtered
    
    order=find_word_order(title_texts,"Πρωινό","Γεύμα","Δείπνο")


    paragraph_texts = add_space_before_caps([p.text for p in soup.find_all('p')]) #this check is kinda good but it could get better
    print(paragraph_texts)

    food_texts=[]
    for text in paragraph_texts:
        if "Πιάτο" in text or "καφές" in text: #this check is kinda good but it could get better
            food_texts.append(text.replace("'",'"'))

    menus=food_texts[0:3].copy()  ### each menu appears 3 times so we take the first 3

    menus_ordered=["","",""]
    for i in range(3):
        menus_ordered[i]=menus[order[i]]


    
    return process_all_menu_items(parse_menus(menus_ordered))


if __name__ == "__main__":
    print(get_current_menus())