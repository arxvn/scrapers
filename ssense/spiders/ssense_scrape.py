import scrapy
from ssense.items import SsenseItem
from datetime import datetime
import re


class Ssense(scrapy.Spider):
	name = "my_scraper"

	# First Start Url
	start_urls = ["https://www.ssense.com/en-gb/men/designers/raf-simons", "https://www.ssense.com/en-gb/men/designers/undercover", "https://www.ssense.com/en-gb/men/designers/ambush", "https://www.ssense.com/en-gb/men/designers/balenciaga"]

	def next_page(self,response):
		for href in response.xpath("//a[cotains(@class, 'router-link-active')//@href"):
			url = "https://ssense.com" + href.extract()
			yield scrapy.Request(url, callback=self.parse)

	
	def parse(self, response):
		for href in response.xpath("//figure[contains(@class, 'browsing-product-item')]/a//@href"):
			# add the scheme, eg http://
			url  = "https://ssense.com" + href.extract() 
			yield scrapy.Request(url, callback=self.parse_dir_contents)	
					
	def parse_dir_contents(self, response):
		item = SsenseItem()

		# Getting Brand
		item['brand'] = response.xpath("//meta[contains(@property, 'product:brand')]/@content").extract_first()

		# Getting product name
		item['title']= response.xpath("//h2[contains(@class, 'product-name')]/text()").extract_first()

		# Getting product description
		item['description'] = response.xpath("//meta[contains(@property, 'og:description')]/@content").extract_first()

		
		# image
		item['image'] = response.xpath("//meta[contains(@property, 'og:image')]/@content").extract_first()

		# Number of site name
		item['author'] = response.xpath("//meta[contains(@name, 'author')]/@content").extract_first()

		# Get product price
		item['price']  = response.xpath("//h1[contains(@class, 'product-price')]/span/text()").extract_first()

		# Url (The link to the page)
		item['url'] = response.xpath("//meta[contains(@property, 'og:url')]/@content").extract_first()

		yield item