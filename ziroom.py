#coding:utf-8
from bs4 import BeautifulSoup
from urllib.parse import quote
import requests
import re
'''
位置：按照地铁站遍历，自动给出每处地铁站附近性价比最高房源，同时给出标准差评分
变量：距离地铁站距离<1000m 价格<2000 面积>10m
抓数据
不限+友家合租url='http://sh.ziroom.com/z/nl/z2.html'
地铁：1号线 http://sh.ziroom.com/z/nl/z2-s1%E5%8F%B7%E7%BA%BF.html # {%E5%8F%B7%E7%BA%BF:号线}
8号线 杨思 价格区间0-2000 http://sh.ziroom.com/z/nl/z2-r0TO2000-s8%E5%8F%B7%E7%BA%BF-t%E6%9D%A8%E6%80%9D.html
'''
#url构建：

def fun_url(line_num=8,station='杨思',price_low='0',price_high='5000'):
	station=quote(station,'utf-8')
	url='http://sh.ziroom.com/z/nl/z2-r{0}TO{1}-s{2}%E5%8F%B7%E7%BA%BF-t{3}.html'.format(price_low,price_high,line_num,station)
	return url

header={
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
	'Cache-Control': 'max-age=0',
	'Connection': 'keep-alive',
	'Host': 'sh.ziroom.com',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'
}



def robot(url):
	content=content=requests.get(url,headers=header).content
	bsObj=BeautifulSoup(content,'html.parser')
	li=bsObj.find_all("li",class_= "clearfix")
	list=[]
	for i in li:
		list_temp=[]
		list_temp.append(i.find("h3").text) #biaoti title
		list_temp.append(i.find("h4").find("a")['href'][2:])#href
		list_temp.append(i.find("div",class_="img pr").find("img")['_src'][2:])#img_href
		space=i.find("div",class_="detail").find("span").text.split(" ")[0]
		list_temp.append(re.search("\d+",space).group())#space
		distance=i.find("div",class_="detail").find_all("p")[1].find("span").text
		list_temp.append(int(re.search("站\d+",distance).group()[1:]))#distance
		price=i.find("p",class_="price").text
		list_temp.append(int(re.search("\d+",price).group()))#price
		list_temp.append(i.find("h4").find("a").text)#address
		list.append(list_temp)
	return list

def main(line_num,station,price_low,price_high):
	url=fun_url(line_num,station,price_low,price_high)
	content=requests.get(url,headers=header).content
	bsObj=BeautifulSoup(content,'html.parser')
	try:
		total_page=int(re.search("\d+",bsObj.find("div",class_="pages").find("span").text).group())
	except AttributeError:
		total_page=1
	list_total=[]
	for i in range(1,total_page+1):
		url1=url+'?p='+str(i)
		print(url1)
		list=robot(url1)
		list_total=list_total+list
	list_total=sorted(list_total,key=lambda t:t[5]/float(t[3]))
	return list_total

'''
list_total[0]=['友家 · 上南路3520弄6居室-南卧', 'sh.ziroom.com/z/vr/61103599.html', 'img.ziroom.com/pic/house_images/g2/M00/66/F0/ChAFfVq8xpWALPT7ABRb9gPZjbA175.JPG_C_264_198_Q80.jpg', '11.3', 995, 1830, '[浦东三林] 8号线杨思']

'''

'''
<li class="clearfix">
<div class="img pr">
<a href="//sh.ziroom.com/z/vr/61182626.html" target="_blank"><img _src="//img.ziroom.com/pic/house_images/g2/M00/92/06/ChAFD1rYqlyAO9O1ABJPYxVjrt8883.JPG_C_264_198_Q80.jpg" _webpsrc="//img.ziroom.com/pic/house_images/g2/M00/92/06/ChAFD1rYqlyAO9O1ABJPYxVjrt8883.JPG_C_264_198_Q80.webp" alt="杨思路502弄" src="//static8.ziroom.com/phoenix/pc/images/list/loading.jpg"/></a>
</div>
<div class="txt">
<h3><a class="t1" href="//sh.ziroom.com/z/vr/61182626.html" target="_blank">整租 · 杨思路502弄1居室-南</a></h3>
<h4><a href="//sh.ziroom.com/z/vr/61182626.html" target="_blank">[浦东三林] 8号线杨思</a></h4>
<div class="detail">
<p>
<span>41 ㎡</span>|
<span>04/6层</span>|
<span>1室1厅</span>
</p>
<p><span>距8号线杨思站46米</span></p>
</div>
<p class="room_tags clearfix">
<span class="subway">离地铁近</span>
<span class="balcony">独立阳台</span>
<span class="style">整租4.0 清语</span>
</p>
</div>
<div class="priceDetail">
<p class="price">
                                                                    ￥ 4190                                                                <span class="gray-6">(每月)</span>
</p>
<p class="more"><a href="//sh.ziroom.com/z/vr/61182626.html" target="_blank">查看更多</a></p>
</div>
</li>
'''
