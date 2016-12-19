# -*- coding: utf-8 -*-
import json
import re
import requests
import scrapy
import scrapy.spiders

import JDSpider.items

from scrapy.selector import Selector


class JdSpider(scrapy.spiders.CrawlSpider):
    name = "JDSpider"
    redis_key = "JDSpider:start_urls"
    start_urls = ["http://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-10001#comfort"]

    def parse(self, response):
        item = JDSpider.items.JdspiderItem()
        selector = Selector(response)
        # 下载一份html文件，用以分析
        with open('jd_book_1.html', 'w') as f:
            f.write(response.body)

        books = selector.xpath('/html/body/div[8]/div[2]/div[3]/div/ul/li')
        for each in books:
            num = each.xpath('div[@class="p-num"]/text()').extract()
            bookName = each.xpath('div[@class="p-detail"]/a/text()').extract()
            author = each.xpath('div[@class="p-detail"]/dl[1]/dd/a[1]/text()').extract()
            press = each.xpath('div[@class="p-detail"]/dl[2]/dd/a/text()').extract()

            temphref = each.xpath('div[@class="p-detail"]/a/@href').extract()
            temphref = str(temphref)
            bookId = str(re.search('com/(.*?)\.html', temphref).group(1))

            json_url = 'http://p.3.cn/prices/mgets?skuIds=J_' + bookId
            r = requests.get(json_url).text
            data = json.loads(r)[0]
            price = data['m']
            disPrice = data['p']

            item['number'] = num
            item['bookName'] = bookName
            item['author'] = author
            item['press'] = press
            item['bookId'] = bookId
            item['price'] = price
            item['disPrice'] = disPrice

            yield item

        nextLink = selector.xpath('/html/body/div[8]/idv[2]/div[4]/div/div/span/a[7]/@href').extract()
        if nextLink:
            nextLink = nextLink[0]
            print(nextLink)
            yield scrapy.Request(nextLink, callback=self.parse)
