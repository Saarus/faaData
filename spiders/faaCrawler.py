from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from faaData.items import FaadataItem

class faaCrawler(CrawlSpider):
    name = "faaCrawler"
    allowed_domains = ["www.faa.gov"]
    start_urls = ["http://www.faa.gov/regulations_policies/orders_notices/"]
    rules = (
        Rule(SgmlLinkExtractor(allow='document.information*'),callback='parse_links',follow=True),
        )
 
    def parse_start_url(self, response):
        list(self.parse_links(response))
        
    def parse_page(self, response):
		hxs = HtmlXPathSelector(response)
		item=FaadataItem()
		print response.url		
		contents = []
		tup = ()
		for nodes in hxs.select('//dl'):
		    for i in nodes.select('.//dt'):
				tagName = i.select('./text()').extract()[0]
				
				if tagName=='Content':
					tagVal = i.select('following-sibling::dd[1]/ul/li/a/@href').extract()
				else:
					tagVal = i.select('following-sibling::dd[1]/text()').extract()
					 					
				tup = (tagName,tagVal)
				contents.append(tup)
				
		content = dict(contents)
		content['link'] = response.url
		#content['title']= response.meta['title']		
		item['content'] = content		
		return item
		
    def parse_links(self, response):
        hxs = HtmlXPathSelector(response)
        links = hxs.select('//a')
        for link in links:
            title = ''.join(link.select('./text()').extract())
            url = ''.join(link.select('./@href').extract())
            meta={'title':title,'link':url}
            #print url
            if url.startswith('/regulations_policies/orders_notices/index.cfm'):
               #cleaned_url = "%s/?1" % url if not '/' in url.partition('//')[2] else "%s?1" % url
               cleaned_url = "http://www.faa.gov" + url
               #print cleaned_url
               yield Request(cleaned_url, callback = self.parse_page, meta=meta,)
            else:
				pass   	       

	


