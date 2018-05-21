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
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'
}


def get_url_list(url="https://sh.fang.lianjia.com/"):
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

def total_page_num(url):
    html = requests.get(url, headers=header).text
    bs_obj = BeautifulSoup(html, 'html.parser')
    totalnum = int(bs_obj.find('section',{'class':'toast-inline animation inactive'}).find('span').text)
    return totalnum


def search_one_page(page_url):
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
    for i in li_list:
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
        sale_status = i.find('span', {'class': 'sale-status'}).text  # class="tag selling "
        print(sale_status)


def search_mutil_pages(url):  # 查找传入的url下的所有页面的新楼盘信息
    page_num = total_page_num(url)
    print('page_num:{}'.format(page_num))
    page_count = 0
    while True:
        page_count += 1
        page_url = '{}pg{}'.format(url,page_count)
        if search_one_page(page_url) != 'noNewPageFound':
            pass
        else:
            return None


def multiprocess_fun(url_list,function_name):
    p = Pool()
    for url in url_list:
        print('-'*20)
        print('{}新楼盘价格一览'.format(url[1]))
        print('-'*20)
        p.apply_async(function_name,args=(url[0],))
    p.close()
    p.join()


def main():
    url_list = get_url_list()
    multiprocess_fun(url_list,search_mutil_pages)


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print('Tasks run {:.2f} minutes'.format((end_time-start_time)/60))
