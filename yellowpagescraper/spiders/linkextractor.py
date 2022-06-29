
import scrapy
import re
from operator import add


#Enter keywords to Scrape
keywords = ["Towing"]


#Enter the location
lists= ["California"]

# ]

class UrlssSpider(scrapy.Spider):
    name = 'urlss'
    allowed_domains = ['yellowpages.com']
    start_urls = ['http://google.com/']


   

    def start_requests(self):

       
        for value in keywords:
            for j in lists:
                urls = [ 'https://www.yellowpages.com/search?search_terms={}&geo_location_terms={}&s=default&page={}'.format(value,j,i) for i in range(1,102) ]
                # urls = [ 'https://www.yellowpages.com/search?search_terms=print%20shop&geo_location_terms=Colombus&page={}'.format(i) for i in range(1,102) ]
                for url in urls:
                    yield scrapy.Request(url=url, callback=self.parse)

        #Response
    def parse(self, response):
        

        hello=[]
        new_link=response.xpath("//a[@class='business-name']//@href").extract()
       # pagenumber = str(response.url)
        for i in range(len(new_link)):
            hello.append('www.yellowpages.com')

        new=list( map(add, hello, new_link) )
        #page = re.findall('pageNumber=(.*?)&pageSize',pagenumber)[0]

        new = list(dict.fromkeys(new))

        #_file = "{0}.html".format(page)
        new=filter(None,new)

        url = response.url
        #with open(_file, "wb") as f:
         # f.write(response.body)
        filename = re.search('(?<=search_terms=).*?(?=&)',url).group(0)
        

    


        
        with open('{}.txt'.format(filename.strip().replace('%20',' ')), mode='a+') as myfile:
            myfile.write("\n".join(new))
            myfile.write('\n')

