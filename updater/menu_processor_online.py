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
            food_texts.append(text)

    menus=food_texts[0:3]  ### each menu appears 3 times so we take the first 3
    return menus


if __name__ == "__main__":
    print(get_current_menus())