import scrapy


class CnnSpider(scrapy.Spider):
    name = "cnn"
    start_urls = ['http://www.cnn.com/US/archive/']

    def parse(self, response):
        # follow links to author pages
        for href in response.css('a::attr(href)').extract():
            #self.log('Href Here :%s' % href)
            with open("links3.txt", 'a') as f:
                if 'cnn.com/2010/' in href:
                #if 'www.cnn.com/2016' in href or 'www.cnn.com/2015' in href or 'www.cnn.com/2014' in href or 'www.cnn.com/2013' in href or 'www.cnn.com/2012' in href or 'www.cnn.com/2012' in href or 'www.cnn.com/2011' in href or 'www.cnn.com/2010' in href:
                    f.write(href)
                    f.write("\n")
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse)
