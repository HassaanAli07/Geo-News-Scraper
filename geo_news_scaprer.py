import requests as re
import os
from bs4 import BeautifulSoup

def scrape_geo_news(URL):

    All_Articles = []
    url_checks = set()

    folder_path = os.path.join("static", "images")
    os.makedirs(folder_path, exist_ok=True)

    # URL = 'https://www.geo.tv/category/sports'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    try :

        response = re.get(URL)

        soup = BeautifulSoup(response.text, 'html.parser')

        li =  soup.find_all('li', class_='border-box')
    
    except :
        print('Url not found/incorrect')
        return []

    for element in li:
        if element:
            anchor_tags = element.select('a.open-section[data-vr-contentbox-url]')
            for article_link in anchor_tags:
                article_url = article_link.get('href')
                
                if article_url in url_checks:
                    continue

                url_checks.add(article_url)

                response2 = re.get(article_url, headers=headers)
                soup = BeautifulSoup(response2.text, 'html.parser')
                div  = soup.find('div', class_='column-right')

                try:
                    title_tag = div.find('div', class_='heading_H')
                    if title_tag:
                        title = title_tag.text.strip()
                except :
                    print("Title Not Found !!")
        
                try:
                    date =  div.find('p', class_='post-date-time').text.strip()
                except :
                    print("Date Not Found !!")

                try:
                    paragraph_tag = div.find('div', class_='content-area')
                    description = paragraph_tag.find_all('p')
                    article_description = ""
                    for des in description:
                        article_description += des.text.strip() + " "

                except:
                    print('Description not Found !!')
        
                try:
                    image_tag = div.find('div', class_='medium-insert-images').find('img')
                    image_url = image_tag.get('src')
                    image_name = image_url.split('/')[-1]
                    image_path = os.path.join(folder_path, image_name)
                    if not os.path.exists(image_path):
                        image_data = re.get(image_url).content
                        with open(image_path, 'wb') as f:
                            f.write(image_data)
                    image_path_for_db = f'static/images/{image_name}'
                except:
                    image_path_for_db = ""  # Set default empty string if no image

                    # image_tag = div.find('div', class_='medium-insert-images ui-sortable').find('img')
                    # image_url = image_tag.get('src')
                    # image_name = image_url.split('/')[-1]
                    # image_path = os.path.join(folder_path, image_name)
                    # try:
                    #     if not os.path.exists(image_path):
                    #         image_data = re.get(image_url).content
                    #         with open(image_path, 'wb') as f:
                    #             f.write(image_data)
                    #             # print(f"Downloaded image to {image_path}")
                    # except Exception as e:
                    #     print(f"Failed to download image: {e}")
                
                # appending data in dictionary
                article_info = {
                    'url': article_url,
                    'title' : title,
                    'date': date,
                    'description': article_description,
                    'image_url': image_path_for_db 
                }

                All_Articles.append(article_info)
    
    return All_Articles
    




