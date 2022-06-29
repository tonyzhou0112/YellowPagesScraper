
import scrapy
import re
import csv
import random
import time
from operator import add
import json
from pprint import pprint
import os.path
from os import path
def days_extract(string):
    days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    days_list = [i.strip() for i in string.split('-')]
    indices = [days.index(day) for day in days_list]
    return days[indices[0]:indices[1]+1]


def to_full_name(string):
    return string.replace('Mon','Monday').replace('Tue','Tuesday').replace('Wed','Wednesday').replace('Thu','Thursday').replace('Fri','Friday')\
    .replace('Sat','Saturday').replace('Sun','Sunday')

def change_format(dataline):
    try:
        oneline_split = dataline.split(':',1)
        days = oneline_split[0]
        days_list = days_extract(days)
        time_split = oneline_split[1].replace('-',',').strip().replace(' ','')
        x = '|'.join(list(map(lambda x: x+','+ time_split,days_list)))
        return to_full_name(x)
    except:
        return to_full_name(dataline.replace(':',',',1).replace('-',',').replace(' ',''))

def days_closed(hours):
	days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	y = [element.split(',')[0] for element in hours.split('|')]
	missing = list(set(days).difference(set(y)))
	closed_string = '|'.join(list(map(lambda x: x+','+ 'Closed',missing)))
	return hours+'|'+closed_string


filenames = ["Towing.txt"]

class donutSpider(scrapy.Spider):

	name="donut"

	def start_requests(self):

		for filename in filenames:


			hello=[]

			with open(filename) as f:
				comp = list(f.readlines())
			urls = [i.strip('\n') for i in comp]

			for i in range(len(urls)):
				hello.append('https://')

			urlss=list( map(add, hello,urls ) )

			for url in urlss:
				yield scrapy.Request(url=url, callback=self.parse,meta={'filename':filename,'url':url})

	def parse(self, response):
		# item=NewmoneyItem()
		filename = response.meta['filename']
		url = response.meta['url']

		try:
			name=response.xpath("//div[@class='sales-info']/h1/text()").get()

		except:
			name=response.xpath("//div[@class='sales-info']/h1/text()").get()


		# try:
		# 	phone=response.xpath("//p[@class='phone']/text()").get()



		# except:
		# 	phone='none'

		try:
			emails =response.xpath("//a[@class='email-business']//@href").get()
			email = emails.replace('mailto:','').strip()

		except:
			email=''

		try:
			# address=response.xpath("//h2[@class='address']/text()").get()
			# address2= response.xpath("//h2[@class='address']/span/text()").get()
			address3= response.xpath("//p//span[contains(text(),'Address: ')]/ancestor::p/text()").get()

		except:
			# address="none"
			address3=""

		try:
			website=response.xpath('//a[@class="website-link dockable"]//@href').get()

		except:
			website='none'


		try:
			latitude = response.xpath('//div[@id="bpp-static-map"]/@data-lat').get()

		except:
			latitude = 'none'

		try:
			longitude = response.xpath('//div[@id="bpp-static-map"]/@data-lng').get()

		except:
			longitude = 'none'


		try:
			general_info = response.xpath('//dd[@class="general-info"]/text()').get()

		except:
			general_info = 'none'


		try:
			tags = ' '.join(response.xpath('//dd[@class="categories"]//a//text()').getall())
			length = len(response.xpath('//dd[@class="categories"]//a'))
			info_list = []
			for i in range(1,length+1):
				info = ''.join(response.xpath('//dd[@class="categories"]//a[{}]/text()'.format(i)).extract())
				if info:
					info_list.append(info.replace('\xa0',''))

			tags = ','.join(info_list)		
		except:
			tags = 'none'

		try:
			length = len(response.xpath('//*[@class="other-information"][2]//p'))
			info_list = []
			for i in range(1,length+1):
				info = ''.join(response.xpath('//*[@class="other-information"][2]//p[{}]//text()'.format(i)).extract())
				if info:
					info_list.append(info.replace('\xa0',''))

			other_information = ','.join(info_list)

		except:
			other_information = 'none'


		try:
			hours_list = len(response.xpath('//div[@class="open-details"]//table//tr'))
			array = []
			for i in range(hours_list):

				x = ' '.join(response.xpath('//div[@class="open-details"]//table//tr[{}]//text()'.format(i)).extract())
				if x:
					array.append(change_format(x))
			hour = '|'.join(array)
			if hour:
				hours = days_closed(hour)
			else:
				hours = ''


		except:
			hours = 'none'
			print('None passed.......................................None Alert'*9)

		try:
			images = response.xpath('//div[@class="collage"]//a/@href').get()

		except:
			images = ''


		try:
			state =address.strip().split(',')[1].strip().split(' ')[0]
		except:
			state= ''

		try:
			zip_code = address.strip()[-5:]
		except:
			zip_code = ''

		try:
			location = address.strip().split(',')[0].strip()

		except:
			location = ''

		try:
			street = response.xpath("//h2[@class='address']/span/text()").get()

		except:
			street = ''

		try:
			fax = response.xpath('//dd[@class="extra-phones"]//span[contains(text(),"Fax")]/following-sibling::span/text()').get()

		except:
			fax = ''		


		# try:
		# 	time.sleep(5)
		# 	tarating = response.xpath("(//div[contains(@class,'ta-rating')])/@class").get()

		# except:

		# 	tarating  = ''
		# try:
		# 	tacount = response.xpath('(//span[@class="ta-count"])/text()').get()

		# except:
		# 	tacount  = ''

		address_info = json.loads(response.xpath('/html/head/script[@type="application/ld+json"][1]/text()').get(''))
		address_dict = address_info.get('address',{})
		postalCode = address_dict.get('postalCode','')
		streetAddress = address_dict.get('streetAddress','')
		addressLocality = address_dict.get('addressLocality','')
		addressRegion = address_dict.get('addressRegion','')
		full_address = streetAddress + "," + addressLocality + "," + " "+ addressRegion + " " + postalCode


		geo_dict = address_info.get('geo',{})
		latitude = geo_dict.get('latitude','')
		longitude = geo_dict.get('longitude','')
		phone = address_info.get('telephone','')

		# full_address = json.loads(response.xpath('/html/head/script[14]/text()').get(''))
		# full1_address = full_address.get('YPU',{})
		# full2_address = full1_address.get('address','')


		item = {
			'Name':name,
			'General Info':general_info,
			'Address':address3,
			# 'Latitude':latitude,
			# 'Longitude':longitude,
			'Phone':phone,
			'Email':email,
			'Website':website,
			'Twitter':'#',
			'Facebook':'#',
			'Linkedin':'#',
			'Google_plus':'#',
			'Youtube':'#',
			'Instagram':'#',
			'Youtube Video URL':'#',
			'Price From':'$$',
			'Price To':'',
			'Category':'{}'.format(filename.replace('.txt','').replace('.Txt','').strip().title()),
			'Features':other_information,
			'Tags (Keywords)':tags,
			'Street':streetAddress,
			'Location':addressLocality,
			'State':addressRegion,
			'Zip Code':postalCode,
			'Longitude' : longitude,
			'Latitude' : latitude,
			'Business Hours (Day,OpenTime,CloseTime)':hours,
			'MainAddress':full_address,
			'Url':url,
			'fax':fax
			# 'tarating':tarating,
			# 'tacount':tacount

		}
		# import ipdb; ipdb.set_trace()
		file_exists = os.path.isfile('{}.csv'.format(filename).replace('.txt',''))


		# if images == None:
		# 	item['Gallery'] =images


		with open('{}.csv'.format(filename).replace('.txt',''), mode='a+') as f:
			# Just use 'w' mode in 3.x
			w = csv.DictWriter(f, item.keys(),lineterminator = '\n')
			if not file_exists:
				w.writeheader()
			w.writerow(item)
		# with open('Minni5.csv', mode='a+') as f:
		# 		# Just use 'w' mode in 3.x
		# 	w = csv.DictWriter(f, item.keys(),lineterminator = '\n')

		# 	w.writerow(item)

		# else:
		# 	# import ipdb; ipdb.set_trace()
		# 	yield scrapy.Request(url=response.urljoin(images), callback=self.parse_imgs,meta={'item':item,'filename':filename})







	# def parse_urls(self,response):
	# 	import ipdb; ipdb.set_trace()

	# def parse_imgs(self,response):
	# 	filename = response.meta['filename']
	# 	file_exists = os.path.isfile('{}.csv'.format(filename).replace('.txt',''))
	# 	item = response.meta['item']
	# 	x = response.xpath('//img/@src').getall()
	# 	image_links = ','.join([i for i in x if '.jpg' in i])

	# 	item['Gallery'] = image_links

	# 	with open('{}.csv'.format(filename).replace('.txt',''), mode='a+') as f:
	# 			# Just use 'w' mode in 3.x
	# 		w = csv.DictWriter(f, item.keys(),lineterminator = '\n')
	# 		if not file_exists:
	# 			w.writeheader()
	# 		w.writerow(item)



		# with open('Category15.csv', mode='a+') as f:
		# 		# Just use 'w' mode in 3.x
		# 	w = csv.DictWriter(f, item.keys(),lineterminator = '\n')

		# 	w.writerow(item)








