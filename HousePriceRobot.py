import requests
from bs4 import BeautifulSoup
import time
from multiprocessing import Pool
from sqlalchemy import Column, String, Integer,Text,create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://root:heyaoxu555@127.0.0.1:3306/wanshiwu_demo')
DBSession = sessionmaker(bind=engine)


class NewHouse(Base):
    __tablename__ = 'newhouse'
    id = Column(Integer,primary_key=True,autoincrement=True)
    city = Column(String(50),nullable=False)
    district = Column(String(100))
    town = Column(String(100))
    address = Column(Text)
    building_name=Column(String(100),nullable=False)
    price = Column(String(100),nullable=False)
    status = Column(String(20))


header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'
}


def get_url_list(url="https://sh.fang.lianjia.com/"):  # 获取链家网各城市新楼盘信息的url列表
    html = requests.get(url).text
    bs_obj = BeautifulSoup(html, "html.parser")
    div_list = bs_obj.find_all('div', {'class': 'city-enum fl'})
    url_list = []
    for i in div_list:
        a_list = i.find_all('a')
        for j in a_list:
            a_url = j.get('href')
            a_text = j.text
            if a_url[-16:] == 'fang.lianjia.com':
                a_url = 'https:' + a_url + '/loupan/'
                a_tuple = (a_url, a_text)
                url_list.append(a_tuple)
    return url_list  # 返回由链接及城市名的元组组成的列表 eg:[(url,西安),...]


def total_house_num(url):    # 返回该城市
    html = requests.get(url, headers=header).text
    bs_obj = BeautifulSoup(html, 'html.parser')
    totalnum = int(bs_obj.find('section',{'class':'toast-inline animation inactive'}).find('span').text)
    return totalnum


def search_one_page(page_url,city_name,count):
    try:
        html = requests.get(page_url, headers=header).text
    except TimeoutError:
        print('TimeoutError:{}'.format(page_url))
        return None
    bs_obj = BeautifulSoup(html, 'html.parser')
    if bs_obj.find('div', {'class': 'no-result-wrapper show'}) is not None:  # 当搜索到无结果页面时，提示没有新的子页面
        print(bs_obj.find('div', {'class': 'noresult'}))
        return 'noNewPageFound'
    li_list = bs_obj.find_all('li', {'class': 'resblock-list'})
    info_list=[]
    for i in li_list: # [city,district,town,address,building_name,price,status]
        count += 1
        city = city_name
        span_list = i.find('div',{'class':'resblock-location'}).find_all('span')
        district = span_list[0].text
        town = span_list[1].text
        address = i.find('div',{'class':'resblock-location'}).find('a').text
        building_name = i.find('a', {'class': 'name'}).text
        try:
            price_num = i.find('span', {'class': 'number'}).text
        except:
            price_num = ''
        try:
            price_unit = i.find('span', {'class': 'desc'}).text
            price_unit = price_unit.lstrip()
        except:
            price_unit = ''
        price = '{}{}'.format(price_num,price_unit)
        status = i.find('span', {'class': 'sale-status'}).text
        #print('city:{} distract:{} town:{} address:{} building_name:{} pirce:{} status:{}'.format(city,district,town,address,building_name,price,status))
        list_temp = [city,district,town,address,building_name,price,status]
        info_list.append(list_temp)
    return info_list,count



def search_mutil_pages(url,city_name):  # 查找传入的url下的所有页面的新楼盘信息
    house_num = total_house_num(url)
    print('house_num:{}'.format(house_num))
    count = 0
    page_count = 0
    while count <= house_num:
        page_count += 1
        page_url = '{}pg{}'.format(url,page_count)
        print(page_url,city_name)
        page_info = search_one_page(page_url, city_name, count)
        if page_info != 'noNewPageFound':
            info_list = page_info[0]
            count=page_info[1]
            yield info_list
        else:
            break
#     city = Column(String(50),nullable=False)
#     district = Column(String(100))
#     town = Column(String(100))
#     address = Column(Text)
#     building_name=Column(String(100),nullable=False)
#     price = Column(String(100),nullable=False)
#     status = Column(String(20))


def db_insert(url):
    session = DBSession()
    for info_list in search_mutil_pages(url[0],url[1]):
        for house_info in info_list:
            filter = session.query(NewHouse).filter(NewHouse.building_name == house_info[4]).first()
            if filter is None:
                print(u'准备将该条数据插入数据库:/n{}'.format(house_info))
                new_house = NewHouse(city=house_info[0],district=house_info[1],town=house_info[2],address=house_info[3],building_name=house_info[4],price=house_info[5],status=house_info[6])
                session.add(new_house)
                print('数据添加成功')
    session.commit()
    session.close()


def multiprocess_fun(url_list,function_name):
    p = Pool()
    for url in url_list:
        print('-'*20)
        print('{}新楼盘价格一览'.format(url[1]))
        print('-'*20)
        p.apply_async(function_name,args=(url,))
    p.close()
    p.join()


def main():
    url_list = get_url_list()
    multiprocess_fun(url_list,db_insert)


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print('Tasks run {:.2f} minutes'.format((end_time-start_time)/60))
