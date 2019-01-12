# coding=utf-8
import urllib
from bs4 import BeautifulSoup
import requests as req
#req.post('https://httpbin.org/post', data = {'key':'value'})

# htmlfile=urllib.urlopen("https://www.urcosme.com/brands/38/products?category=0&series=397&is_limit=false&is_discontinued=false&is_withdraw=false&sort=1")

for brandNumI in range(1,1500):
    for categoryNumI in range (0,200):
        for serialNumI in range(0,20000):
            for pageNumI in range(1,30):
                brandNum=str(categoryNumI)
                categoryNum=str(categoryNumI)
                serialNum=str(serialNumI)
                pageNum=str(pageNumI)

                htmlfile=urllib.urlopen("https://www.urcosme.com/brands/{}/products?category={}&is_discontinued=false&is_limit=false&is_withdraw=false&page={}&series={}&sort=1".format('38', '0', '1','397'))
                htmltext=htmlfile.read()
                soup = BeautifulSoup(htmltext)
                allcategory=soup.select("#category > option ")
                allserial=soup.select("#series > option ")
                categoryName=""
                serialName=""

                for category in allcategory :
                    if category.get('value') == categoryNum:
                        categoryName=category.get_text()

                for serial in allserial:
                    if serial.get('value') == serialNum:
                        serialName=serial.get_text()


                allProduct=soup.find_all("div", attrs={"class": "uc-product-item"})
                for product in allProduct :
                    img=product.select(".product-image > a > img")[0].get('src')
                    brandName=product.select(".product-infomation > .brand-name > a")[0].get_text()
                    brandId=product.select(".product-infomation > .brand-name > a")[0].get('href').split('/')
                    brandId=brandId[2]
                    requestBrand=req.post('http://140.119.163.195/urcosmeAPI/brands.php', data = {'b_id':brandNum,'name':brandName})
                    print "requestBrand http status : %s " % requestBrand.status_code

                    
                    productName=product.select(".product-infomation > .product-name > a")[0].get_text()
                    productScore=product.select(".product-infomation > .product-score >.product-score-text")[1].get_text()

                    requestCategory=req.post('http://140.119.163.195/urcosmeAPI/categories.php', data = {'c_id':categoryNum,'b_id':brandNum ,'brandName':brandName,'className':categoryName}) 
                    print "requestCategory http status : %s " % requestCategory.status_code

                    requestSerial=req.post('http://140.119.163.195/urcosmeAPI/serial.php', data = {'s_id':serialNum,'serialName':serialName ,'brandName':brandName,'className':categoryName}) 
                    print "requestSerial http status : %s " % requestSerial.status_code

                   
                    
                    articalLink=product.select(".product-infomation > .product-review-count > a")[0].get('href')
                    priceDate=product.select(".product-infomation > .product-market-date > span")
                    price=""
                    date=""
                    for element in priceDate:
                        if element.get_text().find(u'價格'):
                            date=element.get_text().split(u'：')
                            try:
                                date=date[1]
                                #print date
                            except:
                                pass
                                #print("An exception occurred")

                        if element.get_text().find(u'上市日期'):
                            price=element.get_text().split(u'：')
                            try:
                                price=price[1]
                            except:
                                pass

                    requestProducts=req.post('http://140.119.163.195/urcosmeAPI/products.php', data = {'s_id':serialNum,'productName':productName,'grade':productScore,'articalLink':'https://www.urcosme.com%s'% articalLink,'price':price,'brandName':brandName,'serialName':serialName,'className':categoryName,'marketDate':date,'$info':'NULL'}) 
                    print "requestProducts  http status : %s" % requestProducts.status_code

