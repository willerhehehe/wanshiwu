import requests
from bs4 import BeautifulSoup
import sqlalchemy

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Host': 'sh.ziroom.com',
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'
}


def get_url_list():
    url = "https://sh.fang.lianjia.com/"
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


def search_data(city_name, url='https://xa.fang.lianjia.com/loupan/'):
    html = requests.get(url, headers=header).text
    bs_obj = BeautifulSoup(html, 'html.parser')
    li_list = bs_obj.find_all('li', {'class': 'resblock-list-item post_ulog_exposure_scroll'})
    for i in li_list:
        name = i.find('h3', {'class': 'name'}).text
        try:
            price_num = i.find('span', {'class': 'price_num'}).text
        except:
            price_num = ''
        price = price_num + i.find('span', {'class': 'price_bunch'}).text
        #区域划分
    return None


if __name__ == '__main__':
    url_list1 = get_url_list()
    print(search_data(url_list1[0][1], url_list1[0][0]))
