# coding=utf-8
import urllib
import threading as thread
from bs4 import BeautifulSoup
import requests as req
from sets import Set
#req.post('https://httpbin.org/post', data = {'key':'value'})

# htmlfile=urllib.urlopen("https://www.urcosme.com/brands/38/products?category=0&series=397&is_limit=false&is_discontinued=false&is_withdraw=false&sort=1")

def crawl(start,end):
    brandset=Set()
    categoryset=Set()
    productset=Set()
    serialset=Set()
    for brandNumI in range(start,end):
        productset.clear()
        categoryset.clear()
        serialset.clear()
        for categoryNumI in range (0,200):

            for serialNumI in range(0,12500):
                for pageNumI in range(1,20):
                    brandNum=str(brandNumI)
                    categoryNum=str(categoryNumI)
                    serialNum=str(serialNumI)
                    pageNum=str(pageNumI)

                    print 'brandnum = {} categoryNum= {} serialNum=,{} pageNum= {}'.format(brandNum,categoryNum,serialNum,pageNum)
                    print "https://www.urcosme.com/brands/{}/products?category={}&is_discontinued=false&is_limit=false&is_withdraw=false&page={}&series={}&sort=1".format(brandNumI, categoryNum, pageNumI,serialNum)
                    htmlfile=urllib.urlopen("https://www.urcosme.com/brands/{}/products?category={}&is_discontinued=false&is_limit=false&is_withdraw=false&page={}&series={}&sort=1".format(brandNumI, categoryNum, pageNumI,serialNum))
                    htmltext=htmlfile.read()
                    soup = BeautifulSoup(htmltext)
                    if soup.select('.title')[0].get_text() == "404":
                        print "pass"
                        flag="false"
                        brandNumI=brandNumI+1
                        serialNumI=0
                        categoryNum=0
                        serialNum=0
                        break

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
                    if len(allProduct) == 0:
                        break

                    for product in allProduct :
                        img=product.select(".product-image > a > img")[0].get('src')
                        brandName=product.select(".product-infomation > .brand-name > a")[0].get_text()
                        brandId=product.select(".product-infomation > .brand-name > a")[0].get('href').split('/')
                        brandId=brandId[2]
                        if str({'b_id':brandNum,'name':brandName})  in brandset:
                            pass
                        else :
                            requestBrand=req.post('http://140.119.163.195/urcosmeAPI/brands.php', data = {'b_id':brandNumI,'name':brandName})
                            print "requestBrand http status : %s " % requestBrand.status_code
                            # print str({'b_id':brandNum,'name':brandName})
                            brandset.add(str({'b_id':brandNum,'name':brandName}))
                            
                        
                        productName=product.select(".product-infomation > .product-name > a")[0].get_text()
                        productScore=product.select(".product-infomation > .product-score >.product-score-text")[1].get_text()

                        if str({'c_id':categoryNum,'b_id':brandNum ,'brandName':brandName,'className':categoryName}) in categoryset : 
                            pass
                        else:
                            requestCategory=req.post('http://140.119.163.195/urcosmeAPI/categories.php', data = {'c_id':categoryNum,'b_id':brandNum ,'brandName':brandName,'className':categoryName}) 
                            print "requestCategory http status : %s " % requestCategory.status_code
                            categoryset.add(str({'c_id':categoryNum,'b_id':brandNum ,'brandName':brandName,'className':categoryName}))
                            # print ('test- %s' %(requestCategory.text))

                        if str({'s_id':serialNum,'serialName':serialName ,'brandName':brandName,'className':categoryName}) in serialset:
                            pass
                        else:
                            requestSerial=req.post('http://140.119.163.195/urcosmeAPI/serial.php', data = {'s_id':serialNum,'serialName':serialName ,'brandName':brandName,'className':categoryName}) 
                            print "requestSerial http status : %s " % requestSerial.status_code
                            serialset.add(str({'s_id':serialNum,'serialName':serialName ,'brandName':brandName,'className':categoryName}))
                            # print ("s_id=%s serialName =%s brandName=%s className=%s" % (serialNum,serialName,brandName,categoryName))

                        articalLink=product.select(".product-infomation > .product-review-count > a")[0].get('href')
                        priceDate=product.select(".product-infomation > .product-market-date > span")
                        price=""
                        date=""
                        for element in priceDate:
                            if element.get_text().find(u'價格'):
                                date=element.get_text().split(u'：')
                                try:
                                    date=date[1]
                                    # print date
                                except:
                                    pass
                                    #print("An exception occurred")

                            if element.get_text().find(u'上市日期'):
                                price=element.get_text().split(u'：')
                                try:
                                    price=price[1]
                                except:
                                    pass

                        if str({'articalLink':'https://www.urcosme.com%s'% articalLink})in productset:
                            pass
                        else:
                            requestProducts=req.post('http://140.119.163.195/urcosmeAPI/products.php', data = {'s_id':serialNum,'productName':productName,'grade':productScore,'articalLink':'https://www.urcosme.com%s'% articalLink,'price':price,'brandName':brandName,'serialName':serialName,'className':categoryName,'marketDate':date,'info':'NULL'}) 
                            productset.add(str({'articalLink':'https://www.urcosme.com%s'% articalLink})) 
                            print "requestProducts http status : %s " % requestProducts.status_code
                        # print " : %s " % requestProducts.text

def main():
    t = thread.Thread(target = crawl(0,100))
    t.start()

main()
                        
