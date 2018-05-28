import requests
import json

url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=4334f956493941c491f82dcf2823580d&orderno=MF2018552216ZLph3G&returnType=2&count=1'
response = requests.get(url)
result = json.loads(response.text)
if result['ERRORCODE'] == '0':
	print(result['RESULT'][0]['ip'], int(result['RESULT'][0]['port']))
else:
	print(result['ERRORCODE'])
	exit()
