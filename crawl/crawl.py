# coding=utf-8
import urllib
from bs4 import BeautifulSoup
import requests as req
#req.post('https://httpbin.org/post', data = {'key':'value'})

htmlfile=urllib.urlopen("https://www.urcosme.com/brands/38/products?category=0&series=397&is_limit=false&is_discontinued=false&is_withdraw=false&sort=1")
htmltext=htmlfile.read()
soup = BeautifulSoup(htmltext)
allProduct=soup.find_all("div", attrs={"class": "uc-product-item"})


for product in allProduct :
    img=product.select(".product-image > a > img")[0].get('src')
    brandName=product.select(".product-infomation > .brand-name > a")[0].get_text()
    brandId=product.select(".product-infomation > .brand-name > a")[0].get('href').split('/')
    brandId=brandId[2]
    productName= brandName=product.select(".product-infomation > .product-name > a")[0].get_text()
    productScore=brandName=product.select(".product-infomation > .product-score >.product-score-text")[1].get_text() 
    articalLink=product.select(".product-infomation > .product-review-count > a")[0].get('href')
    priceDate=product.select(".product-infomation > .product-market-date > span")
    price=""
    date=""
    for element in priceDate:
        if element.get_text().find(u'價格'):
            date=element.get_text().split(u'：')
            try:
                date=date[1]
                print date
            except:
                print("An exception occurred")

        if element.get_text().find(u'上市日期'):
            price=element.get_text().split(u'：')
            try:
                price=price[1]
                print price
            except:
                print("An exception occurred")

