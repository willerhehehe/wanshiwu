import requests
from bs4 import BeautifulSoup
import time
from multiprocessing import Pool

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
    totalnum = int(bs_obj.find('section',{'class':'toast-inline animation inactive'}).find('span').text)
    count=0
    page_count=0
    while count<= totalnum:
        page_count+=1
        print('page_count:{}'.format(page_count))
        page_url='{0}pg{1}/'.format(url,page_count)
        print(page_url)
        try:
            html = requests.get(page_url, headers=header).text
        except TimeoutError:
            continue
        bs_obj = BeautifulSoup(html, 'html.parser')
        if bs_obj.find('div',{'class':'no-result-wrapper show'}) is not None:  #当搜索到无结果页面时，终止循环
            print(bs_obj.find('div',{'class':'noresult'}))
            break
        li_list = bs_obj.find_all('li', {'class': 'resblock-list'})
        for i in li_list:
            count+=1
            name = i.find('a', {'class': 'name'}).text
            print(name)
            try:
                price_num = i.find('span', {'class': 'number'}).text
            except:
                price_num = ''
            try:
                price_unit = i.find('span', {'class': 'desc'}).text
            except:
                price_unit = ''
            price = price_num + price_unit
            print(price)
            sale_status = i.find('span',{'class':'sale-status'}).text# class="tag selling "
            print(sale_status)
    print('count:{}'.format(count))

            #区域划分
    return None


if __name__ == '__main__':
    start_time = time.time()
    url_list1 = get_url_list()
    p=Pool()
    for url in url_list1:
        print('-'*20)
        print('{}新楼盘价格一览'.format(url[1]))
        print('-'*20)
        p.apply_async(search_data,args=(url[1],url[0]))
    p.close()
    p.join()
    end_time = time.time()
    print('Tasks run {:.2f} minutes'.format((end_time-start_time)/60))
