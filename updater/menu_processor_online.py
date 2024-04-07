from menu_parser import parse_menus,process_all_menu_items

def left_shift(lst, n=1):
    return lst[n:].copy() + lst[:n].copy()



def get_current_menus():
    import requests
    from bs4 import BeautifulSoup

    url = "https://my.upatras.gr"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    paragraph_texts = [p.text for p in soup.find_all('p')] #this check is kinda good but it could get better
    food_texts=[]
    for text in paragraph_texts:
        if "Πιάτο" in text or "καφές" in text: #this check is kinda good but it could get better
            food_texts.append(text.replace("'",'"'))

    menus=food_texts[0:3].copy()  ### each menu appears 3 times so we take the first 3
    #menus=left_shift(menus,1)

    ### check for order shifts in my.upatras.gr
    while True:
        lengths=[len(i) for i in menus]
        min_length=min(lengths)
        min_index=lengths.index(min_length)
        if min_index==0:
            print("Order is in order")
            break
        else:
            print("Order is not in order, shifting..")
            menus=left_shift(menus,1)
    
    return process_all_menu_items(parse_menus(menus))


if __name__ == "__main__":
    print(get_current_menus())