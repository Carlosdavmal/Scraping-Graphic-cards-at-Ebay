import requests
import csv
from bs4 import BeautifulSoup


def get_page(url):
    response = requests.get(url)

    if not response.ok:
        print('Ebay is: ', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup

def get_data(soup):
    try:
        name = soup.find('h1', id ='itemTitle').find('a').get('data-mtdes').strip().replace('Detalles acerca de ','').replace('\xa0', '',)
    except:
        name = ''
    
    try:
        try:
            p = soup.find('span', id='prcIsum').text.strip()
            

        except:
            p = soup.find('span', id='prcIsum_bidPrice').text.strip()
        prices, currency = p.split(' ')

    except:
        currency = ''
        prices = ''

    try:
        time_left = soup.find('span', id='vi-cdown_timeLeft').text.strip()
        
    except:
        time_left = ''
        

    data = {'name': name,
            'prices': prices,
            'currency': currency,
            'time_left': time_left
            }

    return data
    
def get_list_data(soup):
    try:
        links = soup.find_all('a', class_='s-item__link')

    except:
        links = []

    
    urls = [item.get('href') for item in links]
    return urls

def csv_file(data, url):
    with open('RTX_scraped.csv', 'a', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        row = [data['name'], data['prices'], data['currency'], data['time_left'], url]
       
        writer.writerow(row)

def main():
    url ='https://www.ebay.com/sch/i.html?&_nkw=Rtx&_pgn=1'
    
    products = get_list_data(get_page(url))

    for link in products:
        data = get_data(get_page(link))
        csv_file(data, link)
    print(get_data)
if __name__ == '__main__':
    main()