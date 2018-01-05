import scrapy
import re

#download all articles (text only but with '\n \t " ,  -  .  \'s \ u [ ] ')
class PagesSpider(scrapy.Spider):
    name = "pages"

    def start_requests(self):
        # urls = [
        #     'http://quotes.toscrape.com/page/1/',
        #     'http://quotes.toscrape.com/page/2/',
        # ]
        #urls = ['http://money.cnn.com/2015/03/12/media/univision-fires-rodner-figueroa-michelle-obama/']
        urls = []
        with open("links3.txt") as f:
            for line in f:
                #print line
                urls.append(line.strip())

        for url in urls:
            print (url)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        page = response.url.split("/")[-2]
        filename = 'article-%s.txt' % page

        with open("Articles2/"+filename, 'w') as f:
            contents = response.selector.xpath('//p/text()').extract()
            contents2 = response.selector.xpath('//span//text()').extract()
            contents3 = response.selector.xpath('//h//text()').extract()

            contentsStr = " ".join(re.findall("[a-zA-Z]{3,}", str(contents)))
            contentsStr2 = " ".join(re.findall("[a-zA-Z]{3,}", str(contents2)))
            contentsStr3 = " ".join(re.findall("[a-zA-Z]{3,}", str(contents3)))
            #punctuationless = s.replace("/[.,\/#!$%\^&\*;:{}=\-_`~()]/g"," ");
            #finalString = punctuationless.replace("/\s{2,}/g"," ");
            #self.log(contentsStr)
            f.write('%s' %contentsStr)
            f.write("\n")
            f.write('%s' % contentsStr3)
            #f.write("\n" + str(len(contentsStr)) + "\n")
            #f.write("\n" + str(len(contentsStr3)) + "\n")

            if len(contentsStr) + len(contentsStr3) < 1000:
                f.write(' %s' % contentsStr2[0:2000])
                f.write("\n")

          