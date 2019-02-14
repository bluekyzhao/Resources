from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
# requests.get 如果使用 http代理 去访问 https的网站，代理会被自动丢弃。


class ActiveProxy:
    """
    目前支持从西刺爬取代理IP，默认仅仅爬取第一页高匿。
    想爬取其他，修改 self.crawl_url ，或者继承并自定义crawl_xici()

    """

    def __init__(self):
        self.crawl_url = 'https://www.xicidaili.com/nn/1'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36'}

    def crawl_xici(self):
        """西刺代理,爬取高匿
        return a list which contains all proxy
        """
        all_proxy_list = []
        res = requests.get(self.crawl_url, headers=self.headers)
        soup = BeautifulSoup(res.text, 'lxml')
        # 西刺那个表格，第一行是文字说明，不要，从1开始
        tr_list = soup.find_all('tr')[1:]
        for line in tr_list:
            ip = line.contents[3].string
            port = line.contents[5].string
            proxy_type = line.contents[11].string
            all_proxy_list.append(f'{ip}-{port}-{proxy_type}')
        # all_proxy_list : ['1.1.1.1-23-HTTP','1.2.1.1-233-HTTP']
        return all_proxy_list

    def vertify_proxy(self, ll):
        """
        传递进来一个list,格式类似 ['1.1.1.1','33','HTTP']
        """
        ip = ll[0]
        port = ll[1]
        proxy_type = ll[2]

        if self.only_vertify(ip, port, proxy_type):
            return([ip, port, proxy_type])

    def only_vertify(self, ip, port, proxy_type, timeout=10):
        proxy_server = f'{proxy_type}://{ip}:{port}'
        if proxy_type == 'HTTP':
            url = "http://www.baidu.com/"
            proxies = {'http': proxy_server}
        elif proxy_type == 'HTTPS':
            url = "https://www.baidu.com/"
            proxies = {'https': proxy_server}
        else:
            return False
        try:
            res = requests.get(url, proxies=proxies,
                               headers=self.headers, timeout=timeout)
        except:
            return False
        return res.status_code == 200

    def get_proxy(self):
        # return type : list
        print('正在使用多线程验证，请等待………………')
        pl = self.crawl_xici()
        with ThreadPoolExecutor(max_workers=50) as ex:
            rr = ex.map(self.vertify_proxy, [proxy.split('-') for proxy in pl])

        result = []
        for i in rr:
            if i is not None:
                result.append(i)
        return result


if __name__ == '__main__':
    aa = ActiveProxy()
    res = aa.get_proxy()

    print(res)
