# File Name			: word_spider.py
# Description		: Gets the meaning of a word from Vocabulary.com
# Author			: Ajay
# Date				: 2016-11-22
#==================================================


from scrapy import Spider

class WordSpider(Spider):
    name = "word"
    start_urls = [
        'https://www.vocabulary.com/dictionary/unalienable',
    ]

    def parse(self, response):
        yield {
                'word': response.xpath('//span[@class="word"]//text()').extract(),
                'short': response.xpath('//p[@class="short"]//text()').extract(),
                'long': response.xpath('//p[@class="long"]//text()').extract(),
                }
        

# OR
# import scrapy

# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     start_urls = [
#         'http://quotes.toscrape.com/page/1/',
#         'http://quotes.toscrape.com/page/2/',
#     ]

#     def parse(self, response):
#         page = response.url.split("/")[-2]
#         filename = 'quotes-%s.html' % page
#         with open(filename, 'wb') as f:
#             f.write(response.body)

        # for it in response.css('div.quote'):
        #     yield {
        #             'text': q.css('span.text::text').extract_first(),
        #             'author': q.css('span small::text').extract_first(),
        #             }

'''
m = response.css('div.main')
short = m.css('p.short').extract()
long = m.css('p.long').extract()
[u'<p class="long">To find the origins of the word <i>unalienable</i>, we can look at the root, <i>alien</i>, which comes from the Latin <i>alienus</i>, meaning "of or belonging to another." This provides the basis for our word, with the prefix <i>un-</i> providing the turnaround "not," and the suffix <i>-able</i> providing the idea of capability. Therefore, we get \u201cnot able to be denied.\u201d Oh, and if you are wondering about the common argument as to whether it is "<i>un</i>alienable" or "<i>in</i>alienable," either is correct.</p>']
word = m.css('span.word::text').extract_first()   u'unalienable'

SHORT
response.xpath('//p[@class="short"]').extract()
or
response.xpath('//p[@class="short"]//text()').extract()

LONG
response.xpath('//p[@class="long"]//text()').extract()

WORD
response.xpath('//span[@class="word"]//text()').extract()

import json
j = json.loads(response.body_as_unicode())
l = j['result']['sentences']
type(l)
l[0]['sentence']
len(l)

'''