# Les 04
# Author: Red-F0X (Panin Stanislav)
# Data create: 11.09.2021

from lxml import html
import requests
import unicodedata


def get_news():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.159 Safari/537.36'
    }
    r_lenta = requests.get('https://lenta.ru/', headers=headers)
    r_lenta.encoding = 'utf8'
    lenta = html.fromstring(r_lenta.text)
    lenta.make_links_absolute('https://lenta.ru/')
    lenta_news = lenta.xpath('''(//section[@class="row b-top7-for-main js-top-seven"]//div[@class="first-item"]/h2 |
                                        //section[@class="row b-top7-for-main js-top-seven"]//div[@class="item"])/a/text()''')
    lenta_nlinks = lenta.xpath('''(//section[@class="row b-top7-for-main js-top-seven"]//div[@class="first-item"]/h2 |
                                        //section[@class="row b-top7-for-main js-top-seven"]//div[@class="item"])/a/@href''')
    lenta_news = [unicodedata.normalize("NFKD", el) for el in lenta_news]
    result_lenta_news = {}
    for item in range(len(lenta_nlinks)):
        request = requests.get(lenta_nlinks[item])
        root = html.fromstring(request.text)
        result_lenta_news[lenta_news[item]] = lenta_nlinks[item], ''.join(root.xpath('//time[@class="g-date"]/text()'))

    r_ya = requests.get('https://yandex.ru/', headers=headers)
    r_ya.encoding = 'utf8'
    yandex = html.fromstring(r_ya.text)
    yandex.make_links_absolute('https://yandex.ru/')
    ya_news = yandex.xpath('//*[@id="news_panel_news"]/ol/li/a/span/span/text()')
    ya_news = [unicodedata.normalize("NFKD", el) for el in ya_news]
    result_ya_news = dict(zip(ya_news, yandex.xpath('//*[@id="news_panel_news"]/ol/li/a/@href')))

    r_mail = requests.get('https://mail.ru/', headers=headers)
    r_mail.encoding = 'utf8'
    mail = html.fromstring(r_mail.text)
    mail.make_links_absolute('https://mail.ru/')
    mail_news = mail.xpath('//div[@class="grid_newscol svelte-1lkwxz2"]'
                           '/div[@class="grid__ccol svelte-1lkwxz2"]/ul/li/div/a/text()')
    mail_nlinks = mail.xpath('//div[@class="grid_newscol svelte-1lkwxz2"]'
                             '/div[@class="grid__ccol svelte-1lkwxz2"]/ul/li/div/a/@href')
    mail_news = [unicodedata.normalize("NFKD", el) for el in mail_news]
    result_mail_news = {}
    for item in range(len(mail_nlinks)):
        request = requests.get(mail_nlinks[item], headers=headers)
        root = html.fromstring(request.text)
        result_mail_news[mail_news[item]] = mail_nlinks[item], ''.join(
            root.xpath('//span[@class="note__text breadcrumbs__text js-ago"]/@datetime'))

    return result_lenta_news, result_mail_news, result_ya_news


if __name__ == '__main__':
    print(get_news())
