import aiohttp
import asyncio
import pandas
import time
import json
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup


class hotData():
    def __init__(self, hotName, hotImg, webItems):
        self.Name = hotName
        self.Img = hotImg
        self.webItems = webItems

#存到商品中的類別 包含商品名稱 價錢及導向連結
class webItem():
    def __init__(self):
        self.webname = list()
        self.webprice = list()
        self.weblink = list()


class SetData():
    def __init__(self, name, img, web, price):
        self.Name = name
        self.Img = img
        self.Web = web
        self.Price = price


headers = {
    'user-agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
url = "https://feebee.com.tw/"

# 建立Flask app
app = Flask(__name__)


def _parse_results(url, html):
    # print(url)
    try:
        # 非常醜的選擇器..
        # 熱門產品區
        soup = BeautifulSoup(html, 'html.parser')
        hotproPic = soup.select(
            ".mod_price_comparison_list > div.mod_price_comparison_product >a.link_ghost > img")
        hotprobtName = soup.select(
            "div.mod_price_comparison_container_bottom > ol > li.mod_price_comparison_items > a")
        hotprobtprice = soup.select(
            "div.mod_price_comparison_container_bottom > ol > li.mod_price_comparison_items > a > span.pure-u-2-5")

        # 精選產品區
        selproPic = soup.select(
            "div#today_choice > ul.mod_product > li.pure-u > a.grid_shadow > img")
        selproName = soup.select(
            "div#today_choice > ul.mod_product > li.pure-u > a.grid_shadow > div.mod_grid_layout_info > div.mod_grid_layout_container >h4")
        selbtweb = soup.select(
            "div#today_choice > ul.mod_product > li.pure-u > a.grid_shadow ")
        selbtprice = soup.select(
            "div#today_choice > ul.mod_product > li.pure-u > a.grid_shadow > div.mod_grid_layout_info > div.mod_grid_layout_container_bottom > div.mod_grid_layout_container_bottom_left > span.large")

        # 人氣產品區
        personproPic = soup.select(
            "div#category_general > div.rank_content > ol.theme_general_flag > li.pure-u > a.grid_shadow > div > img")
        personbtweb = soup.select(
            "div#category_general > div.rank_content > ol.theme_general_flag > li.pure-u > a.grid_shadow")
        personbtprice = soup.select(
            "div#category_general > div.rank_content > ol.theme_general_flag > li.pure-u > a.grid_shadow > div.mod_grid_layout_info > div.mod_grid_layout_container_bottom > div.price")

        # 心得：選擇器 若有發現是2個以上的 詞彙的挑其中一個較獨一無二的就好，不能三個都挑，選擇器會無法判讀  ol.li
        # 初始化熱門區每張圖片下面的各三項
        wb = webItem()
        # ht = hotData()
        lis = [[0] * 1 for i in range(10)]
        # create hot,sel,person,instance
        hot = hotData(list(), list(), lis)
        sel = SetData(list(), list(), list(), list())
        person = SetData(list(), list(), list(), list())
        # 熱門產品圖片與名稱
        for i in range(10):
            hot.Name.append(hotproPic[i].get('alt'))
            hot.Img.append(hotproPic[i].get('srcset'))

            # 精選產品圖片與名稱
        for w in range(4):  # len(selproPic)

            sel.Img.append(selproPic[w].get('src'))
            sel.Name.append(selproName[w].string)

            # 人氣產品圖片與名稱
        for t in range(len(personproPic)):
            person.Img.append(personproPic[t].get('src'))
            person.Name.append(personproPic[t].get('alt'))

        #  內容區-----------
        # Container [[0,0,0]...[0,0,0]]每個0裡面都是放[網站,連結,價錢]
        # formatContainer = [[0] * 3 for i in range(10)]
        for j in range(0, len(hotprobtName)):
            wb.webname.append(hotprobtName[j].get('data-store'))  # 熱門產品網站
            wb.weblink.append(hotprobtName[j].get('href'))  # 熱門網站導向連結
            wb.webprice.append(hotprobtprice[j].get('content'))  # 熱門產品價錢區
        # print(wb.webname)
        formatContainer = [[0] * 3 for i in range(10)]
        for n in range(len(formatContainer)):
            # formatContainer[n][0] = [wb.webname[n*3],
            #                          wb.webname[n*3+1], wb.webname[n*3+2]]
            # formatContainer[n][1] = [wb.weblink[n*3],
            #                          wb.weblink[n*3+1], wb.weblink[n*3+2]]
            # formatContainer[n][2] = [wb.webprice[n*3],
            #                          wb.webprice[n*3+1], wb.webprice[n*3+2]]
            formatContainer[n][0] = {"name":wb.webname[n*3],
                                     "link":wb.weblink[n*3],"price":wb.webprice[n*3]}
            formatContainer[n][1] = {"name":wb.webname[n*3+1],
                                     "link":wb.weblink[n*3+1], "price": wb.webprice[n*3+1]}
            formatContainer[n][2] = {"name":wb.webname[n*3+2],
                                     "link":wb.weblink[n*3+2], "price":wb.webprice[n*3+2]}
            
        # print(formatContainer)
        kkk = []
        for n in range(len(formatContainer)):
            kkk.append(formatContainer[n])
        hot.hotData = kkk
            # if (j % 3 == 0):
            #     formatContainer[int(j / 3)][0] = [hotprobtName[int(j / 3)
            #                                                    ].get('data-store'), hotprobtName[int(j / 3)].get('href'),  hotprobtprice[int(j / 3)].get('content')]
            #     formatContainer[int(j / 3)][1] = [hotprobtName[int(j / 3+1)
            #                                                    ].get('data-store'), hotprobtName[int(j / 3+1)].get('href'),  hotprobtprice[int(j / 3+1)].get('content')]
            #     formatContainer[int(j / 3)][2] = [hotprobtName[int(j / 3+2)
            #                                                    ].get('data-store'), hotprobtName[int(j / 3 + 2)].get('href'), hotprobtprice[int(j / 3 + 2)].get('content')]


        
        # 依序放入熱門商品中
        for n in range(len(formatContainer)):
            hot.webItems[n] = formatContainer[n]

       # 精選產品價錢跟網站區
        for q in range(4):  # 這邊price時而抓到時而抓不到 待修 #常跑出來莫名其妙的5折起之類的東西
            sel.Web.append(selbtweb[q].get('data-url'))
            sel.Price.append(selbtprice[q].string)
            # print(selbtprice[q].string)

        # 人氣產品區價錢跟網站
        for q in range(len(personbtweb)):
            person.Web.append(personbtweb[q].get('href'))
            person.Price.append(personbtprice[q].string)
        # 使用pandas轉換成我們要的格式
        hotProduct = pandas.DataFrame(
            {"hotName": hot.Name, "hotImg": hot.Img, "hotlist": hot.webItems})
        selProduct = pandas.DataFrame(
            {"selName": sel.Name, "selImg": sel.Img, "selPrice": sel.Price, "selWeb": sel.Web})
        perProduct = pandas.DataFrame(
            {"personName": person.Name, "personImg": person.Img, "personPrice": person.Price, "personImg": person.Img})
        hotProOutput = json.loads(hotProduct.to_json(
            orient='records', force_ascii=False))
        selOutput = json.loads(selProduct.to_json(
            orient='records', force_ascii=False))
        perOutput = json.loads(perProduct.to_json(
            orient='records', force_ascii=False))
        output = {"hotPro": hotProOutput,
                  "select": selOutput, "person": perOutput}
        return output
    except Exception as e:
        raise e


async def fetch(session, url, headers):
    # url = url + ss
    async with session.get(url, headers=headers, timeout=10) as response:
        return await response.text()


async def main():
    async with aiohttp.ClientSession() as client:
        html = await fetch(client, url, headers=headers)
        # print(html)
        try:
            output = _parse_results(url, html)
            return output
        except Exception as e:
            raise e

# 建立asyncio讀取迴圈
loop = asyncio.get_event_loop()
# output = loop.run_until_complete(main())  # 做完main這件事就關掉

@app.route('/', methods=['POST'])
def gogo():
    output = loop.run_until_complete(main())  # 做完main這件事就關掉
    return jsonify(output)  # 因為Flask預設輸出的型別是string,所以要回傳json物件的話，要用jsonify去做解析


@app.route('/', methods=['GET'])
def getDisplay():
    return "Please Use Post Method"


if __name__ == '__main__':
    app.run()


# import aiohttp
# import asyncio
# import pandas
# import time
# import json
# from flask import Flask, request, jsonify
# from bs4 import BeautifulSoup


# class hotData():
#     def __init__(self, hotName, hotImg, webItems):
#         self.Name = hotName
#         self.Img = hotImg
#         self.webItems = webItems


# # To put objects in hotdata.ht
# class webItem():
#     def __init__(self):
#         self.webname = list()
#         self.webprice = list()
#         self.weblink = list()


# class SetData():
#     def __init__(self, name, img, web, price):
#         self.Name = name
#         self.Img = img
#         self.Web = web
#         self.Price = price


# class outputWebItem():
#     def __init__(self):
#         self.webname = list()
#         self.webprice = list()
#         self.weblink = list()


# headers = {
#     'user-agent':
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
# }
# url = "https://feebee.com.tw/"

# # 建立Flask app
# app = Flask(__name__)


# def _parse_results(url, html):
#     # print(url)
#     try:
#         # 非常醜的選擇器..
#         # 熱門產品區
#         soup = BeautifulSoup(html, 'html.parser')
#         hotproPic = soup.select(
#             ".mod_price_comparison_list > div.mod_price_comparison_product >a.link_ghost > img")
#         hotprobtName = soup.select(
#             "div.mod_price_comparison_container_bottom > ol > li.mod_price_comparison_items > a")
#         hotprobtprice = soup.select(
#             "div.mod_price_comparison_container_bottom > ol > li.mod_price_comparison_items > a > span.pure-u-2-5")

#         # 精選產品區
#         selproPic = soup.select(
#             "div#today_choice > ul.mod_product > li.pure-u > a.grid_shadow > img")
#         selproName = soup.select(
#             "div#today_choice > ul.mod_product > li.pure-u > a.grid_shadow > div.mod_grid_layout_info > div.mod_grid_layout_container >h4")
#         selbtweb = soup.select(
#             "div#today_choice > ul.mod_product > li.pure-u > a.grid_shadow ")
#         selbtprice = soup.select(
#             "div#today_choice > ul.mod_product > li.pure-u > a.grid_shadow > div.mod_grid_layout_info > div.mod_grid_layout_container_bottom > div.mod_grid_layout_container_bottom_left > span.large")

#         # 人氣產品區
#         personproPic = soup.select(
#             "div#category_general > div.rank_content > ol.theme_general_flag > li.pure-u > a.grid_shadow > div > img")
#         personbtweb = soup.select(
#             "div#category_general > div.rank_content > ol.theme_general_flag > li.pure-u > a.grid_shadow")
#         personbtprice = soup.select(
#             "div#category_general > div.rank_content > ol.theme_general_flag > li.pure-u > a.grid_shadow > div.mod_grid_layout_info > div.mod_grid_layout_container_bottom > div.price")

#         # 心得：選擇器 若有發現是2個以上的 詞彙的挑其中一個較獨一無二的就好，不能三個都挑，選擇器會無法判讀  ol.li
#         # 初始化熱門區每張圖片下面的各三項
#         wb = webItem()
#         # ht = hotData()
#         lis = [[0] * 1 for i in range(10)]
#         # create hot,sel,person,instance
#         hot = hotData(list(), list(), lis)
#         sel = SetData(list(), list(), list(), list())
#         person = SetData(list(), list(), list(), list())
#         # 熱門產品圖片與名稱
#         for i in range(10):
#             hot.Name.append(hotproPic[i].get('alt'))
#             hot.Img.append(hotproPic[i].get('src'))
#         # print(hot.Img)
#         # 精選產品圖片與名稱
#         for w in range(len(selproPic)):  # len(selproPic)

#             sel.Img.append(selproPic[w].get('src'))
#             sel.Name.append(selproName[w].string)

#             # 人氣產品圖片與名稱
#         for t in range(len(personproPic)):
#             person.Img.append(personproPic[t].get('src'))
#             person.Name.append(personproPic[t].get('alt'))

#         #  內容區-----------
#         # Container [[0,0,0]...[0,0,0]]每個0裡面都是放[網站,連結,價錢]
#         formatContainer = [[0]*3 for i in range(10)]
#         # formatContainer = [[0] * 3 for i in range(10)]
#         # print(formatContainer)
#         for j in range(0, len(hotprobtName)):
#             wb.webname.append(hotprobtName[j].get('data-store'))  # 熱門產品網站
#             wb.weblink.append(hotprobtName[j].get('href'))  # 熱門網站導向連結
#             wb.webprice.append(hotprobtprice[j].get('content'))  # 熱門產品價錢區
#             if (j % 3 == 0):
#                 formatContainer[int(j / 3)][0] = {"first_shop":hotprobtName[int(j / 3)
#                                                                             ].get('data-store'), "first_link": hotprobtName[int(j / 3)].get('href'), "first_price": hotprobtprice[int(j / 3)].get('content')}
#                 formatContainer[int(j / 3)][1] = {"second_shop": hotprobtName[int(j / 3+1)
#                                                                               ].get('data-store'), "second_link": hotprobtName[int(j / 3+1)].get('href'), "second_price": hotprobtprice[int(j / 3+1)].get('content')}
#                 formatContainer[int(j / 3)][2] = {"third_shop": hotprobtName[int(j / 3+2)
#                                                                              ].get('data-store'), "third_link": hotprobtName[int(j / 3 + 2)].get('href'), "third_price": hotprobtprice[int(j / 3 + 2)].get('content')}
#                 # formatContainer[int(j / 3)].append(hotprobtName[int(j / 3)].get('data-store'))
#                 # formatContainer[int(j / 3)].append(hotprobtName[int(j / 3)].get('href'))
#                 # formatContainer[int(j / 3)].append(hotprobtprice[int(j / 3)].get('content'))
#                 # formatContainer[int(j / 3)].append(hotprobtName[int(j / 3+1)].get('data-store'))
#                 # formatContainer[int(j / 3)].append(hotprobtName[int(j / 3+1)].get('href'))
#                 # formatContainer[int(j / 3)].append(hotprobtprice[int(j / 3+1)].get('content'))
#                 # formatContainer[int(j / 3)].append(hotprobtName[int(j / 3+2)].get('data-store'))
#                 # formatContainer[int(j / 3)].append(hotprobtName[int(j / 3+2)].get('href'))
#                 # formatContainer[int(j / 3)].append(hotprobtprice[int(j / 3+2)].get('content'))
#         # print(formatContainer)
#         # print(len(formatContainer))
#         hot.webItems = formatContainer
#         # hot.webItems = []
#         for n in range(len(formatContainer)):
#             hot.webItems = formatContainer[n]
#         print(hot.webItems)
#         # print(aa.webname)
#         # print(aa.weblink)
#         # print(aa.webprice)
#         # for n in range(len(hot.webItems)):

#        # 精選產品價錢跟網站區
#         for q in range(len(selbtweb)):  # 這邊price時而抓到時而抓不到 待修 #常跑出來莫名其妙的5折起之類的東西
#             sel.Web.append(selbtweb[q].get('data-url'))
#             sel.Price.append(selbtprice[q].string)
#             # print(selbtprice[q].string)

#         # 人氣產品區價錢跟網站
#         for q in range(len(personbtweb)):
#             person.Web.append(personbtweb[q].get('href'))
#             person.Price.append(personbtprice[q].string)
#         # print(hot.Img)
#         # 使用pandas轉換成我們要的格式
#         hotProduct = pandas.DataFrame(
#             {"hotName": hot.Name, "hotImg": hot.Img, "hotlist": hot.webItems})
#         # print(hot.webItems)
#         selProduct = pandas.DataFrame(
#             {"selName": sel.Name, "selImg": sel.Img, "selPrice": sel.Price, "selWeb": sel.Web})
#         perProduct = pandas.DataFrame(
#             {"personName": person.Name, "personImg": person.Img, "personPrice": person.Price, "personImg": person.Img})
#         hotProOutput = json.loads(hotProduct.to_json(
#             orient='records', force_ascii=False))
#         selOutput = json.loads(selProduct.to_json(
#             orient='records', force_ascii=False))
#         perOutput = json.loads(perProduct.to_json(
#             orient='records', force_ascii=False))
#         output = {"hotPro": hotProOutput,
#                   "select": selOutput, "person": perOutput}
#         return output
#     except Exception as e:
#         raise e


# async def fetch(session, url, headers):
#     # url = url + ss
#     async with session.get(url, headers=headers, timeout=10) as response:
#         return await response.text()


# async def main():
#     async with aiohttp.ClientSession() as client:
#         html = await fetch(client, url, headers=headers)
#         # print(html)
#         try:
#             output = _parse_results(url, html)
#             return output
#         except Exception as e:
#             raise e

# # 建立asyncio讀取迴圈
# loop = asyncio.get_event_loop()
# output = loop.run_until_complete(main())  # 做完main這件事就關掉

# @app.route('/', methods=['POST'])
# def gogo():
#     output = loop.run_until_complete(main())  # 做完main這件事就關掉
#     return jsonify(output)  # 因為Flask預設輸出的型別是string,所以要回傳json物件的話，要用jsonify去做解析


# @app.route('/', methods=['GET'])
# def getDisplay():
#     return "Please Use Post Method"


# if __name__ == '__main__':
#     app.run()
