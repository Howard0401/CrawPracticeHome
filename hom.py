import aiohttp
import asyncio
import pandas
import time
import json
from flask import Flask, request,jsonify
from bs4 import BeautifulSoup

headers = {
    'user-agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
url = "https://feebee.com.tw/"


class webItemProp():
    def __init__(self):
        self.webname = list()
        self.webprice = list()
        self.weblink = list()

class hotDataProp():
    def __init__(self):
        self.weblist = list()
wb = webItemProp()
ht = hotDataProp()

#熱門比價商品
hotName = list()
hotImg = list()
bottom=ht
#weblist = list(webitem)


hotData = {
    "proName": hotName ,
    "pronImg": hotImg,
    "bottom": bottom,  
    #"webprice":webprice,
}

# 精選今日好康
selName = list()
selImg = list()
selweb = list()
selPrice = list()
selData = {
    "proName": selName ,
    "pronImg": selImg,
    "selweb": selweb,
    "selPrice": selPrice,
}

#人氣排行榜
personName = list()
personImg = list()
personweb = list()
personPrice = list()
personData = {
    "widName": personName,
    "widImg": personImg ,
    "personweb ": personweb ,
    "personPrice": personPrice ,
}

app = Flask(__name__)

# def _init_(self, url, html):
#     self.url = url 
#     self.headers = headers
#     self.html = html 
#     self.data = ""




def _parse_results(url, html):
    # print(url)
    try: 
      # 熱門產品區
      soup = BeautifulSoup(html, 'html.parser')  
      hotproPic = soup.select(".mod_price_comparison_list > div.mod_price_comparison_product >a.link_ghost > img")
      hotprobtName= soup.select("div.mod_price_comparison_container_bottom > ol > li.mod_price_comparison_items > a")
      hotprobtprice = soup.select("div.mod_price_comparison_container_bottom > ol > li.mod_price_comparison_items > a > span.pure-u-2-5")
      
      # 精選產品區 
      selproPic = soup.select("div#today_choice > ul.mod_product > li.pure-u > a.grid_shadow > img")
      selproName=soup.select("div#today_choice > ul.mod_product > li.pure-u > a.grid_shadow > div.mod_grid_layout_info > div.mod_grid_layout_container >h4")
      selbtweb=soup.select("div#today_choice > ul.mod_product > li.pure-u > a.grid_shadow ")
      selbtprice=soup.select("div#today_choice > ul.mod_product > li.pure-u > a.grid_shadow > div.mod_grid_layout_info > div.mod_grid_layout_container_bottom > div.mod_grid_layout_container_bottom_left > span.price")

      # 人氣產品區
      personproPic=soup.select("div#category_general > div.rank_content > ol.theme_general_flag > li.pure-u > a.grid_shadow > div > img")
      personbtweb=soup.select("div#category_general > div.rank_content > ol.theme_general_flag > li.pure-u > a.grid_shadow")
      personbtprice=soup.select("div#category_general > div.rank_content > ol.theme_general_flag > li.pure-u > a.grid_shadow > div.mod_grid_layout_info > div.mod_grid_layout_container_bottom > div.price")

      #心得：選擇器 若有發現是2個以上的 詞彙的挑其中一個較獨一無二的就好，不能三個都挑，選擇器會無法判讀  ol.li
     
      #熱門產品圖片與名稱 
      for i in range(10):
       hotName.append(hotproPic[i].get('alt'))         
       hotImg.append(hotproPic[i].get('srcset')) 


       #精選產品圖片與名稱 
      for w in range(4):#len(selproPic)
       
        selImg.append(selproPic[w].get('src'))
        selName.append(selproName[w].string)
   

       #人氣產品圖片與名稱 
      for t in range(len(personproPic)):
       personImg.append(personproPic[t].get('src'))
       personName.append(personproPic[t].get('alt'))
      

      #  內容區-----------
      hotprocontain = [[0] * 3 for i in range(10)]
      for j in range(0, len(hotprobtName)):
        wb.webname.append(hotprobtName[j].get('data-store')) 
        wb.weblink.append(hotprobtName[j].get('href'))
        wb.webprice.append(hotprobtprice[j].get('content'))
        if (j % 3 == 0):
          hotprocontain[int(j / 3)][0] = [hotprobtName[int(j / 3)
             ].get('data-store'), hotprobtName[int(j / 3)].get('href'),  hotprobtprice[int(j / 3)].get('content')]
          hotprocontain[int(j / 3)][1] = [hotprobtName[int(j / 3+1)
             ].get('data-store'), hotprobtName[int(j / 3+1)].get('href'),  hotprobtprice[int(j / 3+1)].get('content')]
          hotprocontain[int(j / 3)][2] = [hotprobtName[int(j / 3+2)
             ].get('data-store'), hotprobtName[int(j / 3+2)].get('href'),  hotprobtprice[int(j / 3+2)].get('content')]
      ht.weblist=hotprocontain
      print(len(ht.weblist))
      print(len(hotData))

      # for j in range(len(hotprobtName)):
      #  webname.append(hotprobtName[j].get('data-store')) #熱門產品網站


     #精選產品價錢跟網站區
      for q in range(4):
        selweb.append(selbtweb[q].get('data-url')) 
        selPrice.append(selbtprice[q].string)
        print(selbtprice[q].string)
        

      
      #熱門產品價錢區
      # for n in range(len(hotprobtprice )):
      #  webprice.append(hotprobtprice[n].get('content')) 

       #測試

      #人氣產品區價錢跟網站  
      for q in range(len(personbtweb)):
        personweb.append(personbtweb[q].get('href')) 
        personPrice.append(personbtprice[q].string)   
    except Exception as e:
      raise e

async def fetch(session, url, headers):
    # url = url + ss
    async with  session.get(url, headers = headers, timeout = 10) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as client:
        html = await fetch(client, url, headers = headers)
        print(html)
        try:
          _parse_results(url, html)
        except Exception as e:
          raise e

loop = asyncio.get_event_loop()

@app.route('/', methods=['POST'])
def gogo():
  loop.run_until_complete(main())
  hotProduct = pandas.DataFrame(hotData)
  selProduct = pandas.DataFrame(selData)
  perProduct = pandas.DataFrame(personData)

  hotProOutput = json.loads(hotProduct.to_json(orient='records', force_ascii=False))
  selOutput = json.loads(selProduct.to_json(orient='records', force_ascii=False))
  perOutput = json.loads(perProduct.to_json(orient='records', force_ascii=False))

  output = {"hotPro": hotProOutput, "sel": selOutput, "per": perOutput}
  
  return jsonify(output) #json 物件壹定要用jsonify去做解析


@app.route('/', methods=['GET'])
def getDisplay():
    return "Please Use Post Method"


if __name__ == '__main__':
     app.run()



     