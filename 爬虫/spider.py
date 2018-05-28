from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import etree
import random
import xlrd
import time
import csv
import json

import requests

with open('proxy.json', 'r') as f:
	ip_port = json.load(f)

google = ['https://quick.likeso.ml/',
#	'https://g.codery.ga/',
	'https://coderschool.2345.ga/']

scholar = ['https://scholar.90h6.cn:1668',
	'https://zz.glgooo.top/extdomains/scholar.google.com/']

table = xlrd.open_workbook('exportAwards-2016.xls')
sheet = table.sheet_by_index(0)
begin_index = 5055
column2 = sheet.col_values(2)[begin_index:10002]

f = open('result.csv', 'w', newline='', encoding='utf8')
file = open('author.csv', 'w', newline='', encoding='utf8')
table_header = ['Researcher', 'ID', 'Title', 'Authors', 'Publication date', 'Journal', 'Volume', 'Issue', 'Pages', 'Publisher', 'Description']
file_header = ['Researcher', 'ID', 'Citations', 'h-index', 'i10-index']
index = ['Title', 'Authors', 'Publication date', 'Journal', 'Volume', 'Issue', 'Pages', 'Publisher', 'Description']
writer = csv.DictWriter(f, table_header)
writer.writeheader()

writer_ = csv.DictWriter(file, file_header)
writer_.writeheader()


# proxy = Proxy(
#     {
#         'proxyType': ProxyType.MANUAL,
#         'httpProxy': 'https://127.0.0.1:8000'
#     }
# )
# desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
# proxy.add_to_capabilities(desired_capabilities)
# browser.start_session(desired_capabilities)
# browser = webdriver.PhantomJS()
# browser.start_session(webdriver.DesiredCapabilities.PHANTOMJS)

# proxy=webdriver.Proxy()
# proxy.proxy_type=ProxyType.MANUAL
# proxy.http_proxy='111.170.82.96:61234'
# proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)

# profile = webdriver.FirefoxProfile()
# profile.set_preference('network.proxy.type', 1)
# profile.set_preference('network.proxy.http', '49.79.196.175')
# profile.set_preference('network.proxy.http_port', 61234)
# profile.update_preferences()
# browser = webdriver.Firefox(firefox_profile=profile)


# browser.set_page_load_timeout(10)
# browser.set_script_timeout(10)

# browser = webdriver.Firefox()
# print(dir(browser))

for ID, researcher in enumerate(column2):
	profile = webdriver.FirefoxProfile()

# this part is for xundaili API
	# url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=4334f956493941c491f82dcf2823580d&orderno=MF2018552216ZLph3G&returnType=2&count=1'
	# # this url is free
	# response = requests.get(url)
	# result = json.loads(response.text)
	# if result['ERRORCODE'] == '0':
	# 	profile.set_preference('network.proxy.type', 1)
	# 	profile.set_preference('network.proxy.http', result['RESULT'][0]['ip'])
	# 	profile.set_preference('network.proxy.http_port', int(result['RESULT'][0]['port']))
	# else:
	# 	print(result['ERRORCODE'])
	# 	exit()
# end xundaili API

# this part is for free ip proxy
	proxy = random.choice(ip_port)
	profile.set_preference('network.proxy.type', 1)
	profile.set_preference('network.proxy.http', proxy[0])
	profile.set_preference('network.proxy.http_port', int(proxy[1]))
	
# end free ip proxy

	profile.update_preferences()
	browser = webdriver.Firefox(firefox_profile=profile)
	browser.set_page_load_timeout(10)
	browser.set_script_timeout(10)

	try:
		browser.get(random.choice(google))
		# browser.get(google[2])
		# browser.get('https://www.baidu.com')
	except:
		pass
	# print(browser.page_source)
	# break
	search = browser.find_element_by_name('q')
	button = browser.find_element_by_name('btnK')
	search.send_keys('google scholar citations {}'.format(researcher))
	try:
		button.click()
	except:
		pass
	# print(browser.page_source)
	html = etree.HTML(browser.page_source)
	result = html.xpath('//h3[@class="r"]/a')
	try:
		code = result[0].get('href').split('%')[2][2:]
	except IndexError:
		try:
			code = result[0].get('href').split('=')[1].split('&')[0]
		except IndexError:
			print('!------------------------------------!')
			print('error caused by name or crash: missing researcher--%d-%s' % (ID + begin_index, researcher))
			print('!------------------------------------!')
			browser.close()
			continue

	print(code)
	browser.set_page_load_timeout(30)
	browser.set_script_timeout(30)

	# http://xueshu.endni.com
	# https://sci-hub.org.cn
	# https://scholar.90h6.cn:1668

	try:
		browser.get('https://scholar.90h6.cn:1668/citations?user='\
		 + code \
		 + '&hl=en&view_op=list_works&sortby=pubdate')
	except:
		pass
	html = etree.HTML(browser.page_source)
	# print(browser.page_source)

	# table = html.xpath('//table[@id="gsc_rsb_st"]/tbody/tr')
	try:
		table = html.xpath('//table[@id="gsc_rsb_st"]/tbody/tr')
		author_data = {
			'Researcher': researcher,
			'ID': str(ID + begin_index),
			'Citations': table[0].xpath('.//td')[1].text,
			'h-index': table[1].xpath('.//td')[1].text,
			'i10-index': table[2].xpath('.//td')[1].text
		}
		# print(table[0].xpath('.//td')[1].text)
		# print(table[1].xpath('.//td')[1].text)
		# print(table[2].xpath('.//td')[1].text)
		writer_.writerow(author_data)
	except IndexError:
		print('!------------------------------------!')
		print('error caused by network delay: missing researcher--%d-%s' % (ID + begin_index, researcher))
		print('!------------------------------------!')
		browser.close()
		continue

	result = html.xpath('//a[@class="gsc_a_at"]')
	year = html.xpath('//span[@class="gs_oph"]')
	# time.sleep(5)
	for i, j in zip(result, year):
		if int(j.text[2:]) > 2015:
			data = {'Researcher': researcher, 'ID': str(ID + begin_index)}
			target = 'https://scholar.90h6.cn:1668' + i.get('data-href')
			try:
				browser.get(target)
			except:
				pass
			html = etree.HTML(browser.page_source.replace('<br>', ''))
			try:
				title = html.xpath('//div[@id="gsc_vcd_title"]/a')[0].text
				print(title)
			except:
				continue
			data['Title'] = title
			filed = html.xpath('//div[@class="gsc_vcd_field"]')
			value = html.xpath('//div[@class="gsc_vcd_value"]')
			if (not filed) or (not value):
				continue
			for (f_, v_) in zip(filed, value):
				if f_.text in index:
					data[f_.text] = v_.text
			writer.writerow(data)
			time.sleep(random.randint(8, 12))
		else:
			break
	browser.close()
# browser.close()
# miss 5001 5017 5029 5030 5031