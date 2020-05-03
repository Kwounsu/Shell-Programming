#!/usr/bin/python3.5

from bs4 import BeautifulSoup
import requests
import csv
import datetime

url_list = []
item_list = []
page_ctr = 0
item_ctr = 0

for i in range(1,18):
 url_list.append('https://www.walmart.com/search/?page=' + str(i) + '&ps=40&query=nintendo+switch+games')

for url in url_list:
 page_ctr = page_ctr + 1
 result = requests.get(url)
 c = result.content
 soup = BeautifulSoup(c, 'lxml')
 summary = soup.find('div', {'class':'search-product-result', 'id':'searchProductResult'})
 page_list = summary.findAll('li')
 for page in page_list:
  item_ctr = item_ctr + 1
  mytuple = ()

  #to get the item name
  title = page.find('a', {'class': 'product-title-link'}).text
#  print('title = ',title)
  mytuple = mytuple + (title,)

  # to get the item price
  price_summary = page.find('span', {'class' : 'price display-inline-block arrange-fit price price-main'})
  rating_summary = page.find('span', {'class' : 'visuallyhidden hiddenStarLabel'})
  if price_summary is None:
   mytuple = mytuple + ('$-1',)
  else:
   if price_summary.find('span', {'class': 'visuallyhidden'}) is not None:
    price = price_summary.find('span', {'class': 'visuallyhidden'}).text
#    print('price = ',price)
    mytuple = mytuple + (price,)
   else:
    mytuple = mytuple + ('$-1',)

  # to get rating and review count
  if rating_summary is None:
   mytuple = mytuple + ('No reviews',)
  else:
   if rating_summary.find('span', {'class': 'seo-avg-rating'}) is not None:
    rating = rating_summary.find('span', {'class': 'seo-avg-rating'}).text
#    print('rating = ',rating)
    mytuple = mytuple + (rating,)
   else:
    mytuple = mytuple + ('0',)
   if rating_summary.find('span', {'class': 'seo-review-count'}) is not None:
    review = rating_summary.find('span', {'class': 'seo-review-count'}).text
#    print('review count = ',review)
    mytuple = mytuple + (review,)
   else:
    mytuple = mytuple + ('0',)

  # Append item to the list
  item_list.append(mytuple)

#print('Number of Pages found = ',page_ctr,' and number of items found = ',item_ctr)
sorted_list = sorted(item_list, key=lambda x: float(x[1][1:]))

# Write CSV file
now = datetime.datetime.now()
oddorevenHour = now.hour % 2

with open('Walmart'+str(oddorevenHour)+'.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['title','price','rating','reviews'])
    for row in mytuple:
        csv_out.writerow(row)

with open('Walmart'+str(oddorevenHour)+'.csv', 'w', newline='') as f:
	fieldnames = ['title','price','rating','reviews']
	writer = csv.DictWriter(f, fieldnames=fieldnames)
	writer.writeheader()
	for i in range(0,item_ctr):
		if sorted_list[i][1] == '$-1':
			writer.writerow({'title' : sorted_list[i][0], 'price' : 'In-store purchase only', 'rating' : sorted_list[i][2], 'reviews' : sorted_list[i][3]})
		else:
			writer.writerow({'title' : sorted_list[i][0], 'price' : sorted_list[i][1], 'rating' : sorted_list[i][2], 'reviews' : sorted_list[i][3]})
