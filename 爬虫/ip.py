from lxml import etree
import requests
import json

url = 'http://www.xicidaili.com/nn/{}'

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive'
    }

ip_port = []

for i in range(1, 100):
    response = requests.get(url.format(i), headers=headers)
    html = etree.HTML(response.text)
    result = html.xpath('//table[@id="ip_list"]/tr')
    for j in result[1:]:
    	lines = j.xpath('.//td')
    	if int(lines[6].xpath('.//div/div')[0].get('style')[6:8]) >= 90:
    		ip_port.append((lines[1].text, lines[2].text))
    		print((lines[1].text, lines[2].text))


print(len(ip_port))

with open('proxy.json', 'w') as f:
    json.dump(ip_port, f)