import requests
import time
import json
from datetime import datetime
from bs4 import BeautifulSoup
from environs import Env
import pymysql.cursors


env = Env()
env.read_env()
db_host = env.str('DB_HOST')
db_port = env.int('DB_PORT')
db_user = env.str('DB_USER')
db_pawd = env.str('DB_PASSWORD')
db_name = env.str('DB_NAME')

print(db_name)

connection = pymysql.connect(host=db_host, port=db_port, database=db_name, user=db_user,
          password=db_pawd, charset='utf8')


url = "https://www.cjhdj.com.cn/hdfw/sw/"

cursor = connection.cursor()

# with connection:
#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO `shuiwei` (`time`, `hankou`) VALUES (%s, %s)"
#         cursor.execute(sql, ('2023-10-23', 4.4))

#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()

# dt = datetime.strptime("2023-10-23 8", "%Y-%m-%d %H")
# print(dt)

# ts = datetime.timestamp(dt)
# print(ts)

# 执行sql语句
sql = "insert into shuiwei(time, yibing, jiangan, luzhou, zhutuo, jiangjin, chongqing, changshou, fuling, wanzhou, zhigui, yichang, cheyanghe, zhijiang, shashi, haoxue, shishou, jianli, chenglinji, jiayu, hankou, huangshi, jiujiang, anqing, tonglin, wuhu, nanjing, zhengjiang, shanxia_in, shanxia_out, gezhouba_out) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
# cursor.execute(sql, ('2023-10-23 8', 4.5))
# connection.commit()
# exit()

# print(url)


#API链接    后台获取链接地址
proxyAPI = "http://15623057227.user.xiecaiyun.com/api/proxies?action=getJSON&key=NPE57CDC42&count=1&word=&rand=true&norepeat=false&detail=true&ltime=&idshow=true"
proxyusernm = "15623057227"        #代理帐号
proxypasswd = "15623057227"        #代理密码
# url='https://2023.ip138.com/'


proxyurl = "http://192.168.33.1:8990"

#获取IP
r = requests.get(proxyAPI)
if(r.status_code == 200):
    # print(r.text)
    j = json.loads(r.text)
    if(j["success"] and len(j["result"]) > 0):
        p=j["result"][0]
        #name = input();

        proxyurl="http://"+proxyusernm+":"+proxypasswd+"@"+p["ip"]+":"+"%d"%p["port"]
        # print(r.text)
    else:
        print('获取0个代理IP')
else:
    print('获取代理失败')

print(proxyurl)


t1 = time.time()
r = requests.get('https://2023.ip138.com/', proxies={'http':proxyurl,'https':proxyurl}, headers={
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Cache-Control":"max-age=0",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"})
r.encoding='utf-8'

t2 = time.time()

print(r.text)
print("时间差:" , (t2 - t1));


headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Cache-Control":"max-age=0",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

web_data = requests.get(url, headers=headers, proxies={'http':proxyurl,'https':proxyurl})
web_data.encoding = 'utf-8'
print(web_data.status_code)
# print(web_data.text)

soup = BeautifulSoup(web_data.text, 'lxml')
# print(soup.select('.gl_list1'))

ls = soup.select('.gl_list1 ul li')
print(len(ls))
print(type(ls))
# exit()

# for ul in ls:
for i in range(len(ls)-1, -1, -1):
	ul = ls[i]
	#日期
	ri = ul.select('h3 span')[0].string
	print(ri)

	#时间
	title = ul.select('h3 a')[0]['title']
	index_ri = title.find('日')
	index_shi= title.find('时')
	shi = title[index_ri+1 : index_shi]
	# print(shi)

	page_date = ri + " " + shi
	dt = datetime.strptime(page_date, "%Y-%m-%d %H")
	print(dt)

	sql2 = "select time from shuiwei where time = %s"
	res = cursor.execute(sql2, dt.strftime("%Y-%m-%d %H:%M:%S"))
	# print(res)

	#该日期不存在
	if res == 0:
		#当前时间的链接
		href = ul.select('h3 a')[0]['href']
		print(href)

		sub_url = url + href
		print(sub_url)

		#请求该日期的子页面数据
		sub_data = requests.get(sub_url, proxies={'http':proxyurl,'https':proxyurl})
		sub_data.encoding = 'utf-8'


		sub_soup = BeautifulSoup(sub_data.text, 'lxml')
		print(sub_soup.title)

		sw_yibing = 0
		sw_jiangan = 0
		sw_luzhou = 0
		sw_zhutuo = 0
		sw_jiangjin = 0
		sw_chongqing = 0
		sw_changshou = 0
		sw_fuling = 0
		sw_wanzhou = 0
		sw_zhigui = 0
		sw_yichang = 0
		sw_cheyanghe = 0
		sw_zhijiang = 0
		sw_shashi = 0
		sw_haoxue = 0
		sw_shishou = 0
		sw_jianli = 0
		sw_chenglinji = 0
		sw_jiayu = 0
		sw_hankou = 0
		sw_huangshi = 0
		sw_jiujiang = 0
		sw_anqing = 0
		sw_tonglin = 0
		sw_wuhu = 0
		sw_nanjing = 0
		sw_zhengjiang = 0
		shanxia_in = 0
		shanxia_out = 0
		gezhouba_out = 0

		tb = sub_soup.select('div.xl_con1 table tr')
		# print(tb)
		# exit()


		for t in tb:
			city = t.select('td')[0].string
			height = t.select('td')[1].string
			change = t.select('td')[2].string
			print(city, height, change)

			if -1 < city.find("宜宾"):
				sw_yibing = height

			if -1 < city.find("江安"):
				sw_jiangan = height

			if -1 < city.find("泸州"):
				sw_luzhou = height

			if -1 < city.find("朱沱"):
				sw_zhutuo = height

			if -1 < city.find("江津"):
				sw_jiangjin = height

			if -1 < city.find("重庆"):
				sw_chongqing = height

			if -1 < city.find("长寿"):
				sw_changshou = height

			if -1 < city.find("涪陵"):
				sw_fuling = height

			if -1 < city.find("万州"):
				sw_wanzhou = height

			if -1 < city.find("秭归"):
				sw_zhigui = height

			if -1 < city.find("中水门"):
				sw_yichang = height

			if -1 < city.find("车阳河"):
				sw_cheyanghe = height

			if -1 < city.find("枝江"):
				sw_zhijiang = height

			if -1 < city.find("沙市"):
				sw_shashi = height

			if -1 < city.find("郝穴"):
				sw_haoxue = height

			if -1 < city.find("石首"):
				sw_shishou = height

			if -1 < city.find("监利"):
				sw_jianli = height

			if -1 < city.find("城陵矶"):
				sw_chenglinji = height

			if -1 < city.find("莫家河"):
				sw_jiayu = height

			if -1 < city.find("汉口"):
				sw_hankou = height

			if -1 < city.find("黄石"):
				sw_huangshi = height

			if -1 < city.find("九江"):
				sw_jiujiang = height

			if -1 < city.find("安庆"):
				sw_anqing = height

			if -1 < city.find("铜陵"):
				sw_tonglin = height

			if -1 < city.find("芜湖"):
				sw_wuhu = height

			if -1 < city.find("南京"):
				sw_nanjing = height

			if -1 < city.find("镇江"):
				sw_zhengjiang = height

			if -1 < city.find("三峡入库"):
				shanxia_in = height

			if -1 < city.find("三峡出库"):
				shanxia_out = height

			if -1 < city.find("葛洲坝出库"):
				gezhouba_out = height

		print(sw_jiayu)

		cursor.execute(sql, (dt, sw_yibing, sw_jiangan, sw_luzhou, sw_zhutuo, sw_jiangjin, sw_chongqing, sw_changshou, sw_fuling, sw_wanzhou, sw_zhigui, sw_yichang, sw_cheyanghe, sw_zhijiang, sw_shashi, sw_haoxue, sw_shishou, sw_jianli, sw_chenglinji, sw_jiayu, sw_hankou, sw_huangshi, sw_jiujiang, sw_anqing, sw_tonglin, sw_wuhu, sw_nanjing, sw_zhengjiang, shanxia_in, shanxia_out, gezhouba_out))
		connection.commit()
		time.sleep(10)
	else:
		print("已采集")

	

	# print(ul.select('h3 a')[0]['title'])
	print('-------------------------------------------')


print('============================================================================================')
# print(uls)

# body > div.xl_con > div.xl_con1 > div > table > tbody