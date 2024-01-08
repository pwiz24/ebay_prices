import requests
from bs4 import BeautifulSoup
import pandas as pd

searchterm = 'fender hybrid ii telecaster'

def get_data(searchterm):
    #url = f'https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw={searchterm}&_sacat=0&LH_PrefLoc=1&LH_Auction=1&rt=nc&LH_Sold=1&LH_Complete=1'
    url = f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1311&_nkw={searchterm}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup):
    productslist = []
    results = soup.find('div', {'class': 'srp-river-results clearfix'}).find_all('li',{'class':'s-item s-item__pl-on-bottom'})
    for item in results:
        product = {
            'title': item.find('div',{'class','s-item__title'}).text,
            #'soldprice': item.find('span', {'class': 's-item__price'}).text.replace('$','').replace(',','').strip(),
            'price': item.find('span', {'class': 's-item__price'}).text,
            #'solddate': item.find('span', {'class': 's-item__title--tagblock__COMPLETED'}).find('span', {'class':'POSITIVE'}).text,
            # not all items have bids, test with products that have it
            #'bids': item.find('span', {'class': 's-item__bids s-item__bidCount'}).text,
            'link': item.find('a', {'class': 's-item__link'})['href'],
        }
        productslist.append(product)
    return productslist

def output(productslist, searchterm):
    productsdf =  pd.DataFrame(productslist)
    productsdf.to_csv(searchterm + 'output.csv', index=False)
    print('Saved to CSV')
    return

soup = get_data(searchterm)
productslist = parse(soup)
#print(productslist)
output(productslist, searchterm)
