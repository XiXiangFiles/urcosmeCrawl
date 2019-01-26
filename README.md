# urcosme crawl
* 用途
收集https://www.urcosme.com/ 網站資料並提供推薦選項
* 資料庫設計
    1. Brand ：品牌資料表
    3. Category：分類資料表
    4. Serial：系列資料表
    5. Products： 商品資料表
<img width="400" height="400" src="https://i.imgur.com/8RpatOx.jpg"/>

* Crawl 介紹
brandNum 指的是品牌編號，若是需要進行單一品牌資料收集，則修改range 之中的number。
```python
# at crawl/crawl.py 150 line
def main():
    for brandNum in range(1,1500):
        categorySeries=crawl(brandNum,0,0)
        try:
            brandClass=Brand(categorySeries.category,categorySeries.serial)
            while brandClass.status():
                category=brandClass.popCategory()
                series=brandClass.getSerial()
                if category == 0 :
                    category=brandClass.popCategory()
                for eachSeries in series:
                    if eachSeries != 0:
                        crawl(brandNum,category,eachSeries)
        except:
            pass
```
Class Brand 用於紀錄品牌狀態的一個資料結構，Instance "status" 為紀錄是否完成收集資料。
```python
class Brand:
    category=Set()
    serial=Set()
    def __init__(self,category,serial):
        self.category=category.copy()
        self.serial=serial.copy()
    
    def popCategory(self):
        return self.category.pop()

    def popSerial(self):
        return self.serial.pop()

    def getSerial(self):
        return self.serial

    def status(self):
        if len(self.category) == 0:
            return False
        else :
            return True
```
在收集資料程式碼中「req.post()」所有運用到的，都必須串連後端web server 進行資料庫的存取。
因此「req.post()」中的URI需因主機的不同進行調整，ex http://localhost 等，web Server 程式碼為「APIs/」中
````python
def crawl(brandNumI,categoryNumI,serialNumI):
    brandClass=None
    brandset=Set()
    categoryset=Set()
    productset=Set()
    serialset=Set()
    serialArr=Set()
    categoryArr=Set()
    for pageNumI in range(1,15):
        brandNum=str(brandNumI)
        categoryNum=str(categoryNumI)
        serialNum=str(serialNumI)
        pageNum=str(pageNumI)
        print 'brandnum = {} categoryNum= {} serialNum=,{} pageNum= {}'.format(brandNum,categoryNum,serialNum,pageNum)
        print "https://www.urcosme.com/brands/{}/products?category={}&is_discontinued=false&is_limit=false&is_withdraw=false&page={}&series={}&sort=1".format(brandNumI, categoryNum, pageNumI,serialNum)
        htmlfile=urllib.urlopen("https://www.urcosme.com/brands/{}/products?category={}&is_discontinued=false&is_limit=false&is_withdraw=false&page={}&series={}&sort=1".format(brandNumI, categoryNum, pageNumI,serialNum))
        htmltext=htmlfile.read()
        soup = BeautifulSoup(htmltext)
        try:
            if soup.select('.title')[0].get_text() == "404":
                print "pass"
                break
        except:
            pass


        allcategory=soup.select("#category > option ")
        allserial=soup.select("#series > option ")
        categoryName=""
        serialName=""

        for category in allcategory :
            if categoryNumI ==0:
                categoryArr.add(int(category.get('value')))
                            
            if category.get('value') == categoryNum:
                categoryName=category.get_text()

        for serial in allserial:
            if serialNumI ==0 :
                serialArr.add(int(serial.get('value')))

            if serial.get('value') == serialNum:
                serialName=serial.get_text()
        
        if categoryNumI ==0 and serialNumI ==0:
            brandClass=Brand(categoryArr,serialArr)

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
                           
    return brandClass
````
> Note: 前端顯示需要安裝Nodejs ，進入web執行以下指令即可
```shell
    npm install
    npm start
```
