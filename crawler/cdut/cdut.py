def GetCalendar(username,password):
	import requests
	import execjs
	import time
	import pandas
	import pytz
	import re
	from icalendar import Calendar, Event
	import datetime,time

	Default="http://202.115.133.173:805/Default.aspx"
	url="http://202.115.133.173:805/Classroom/ProductionSchedule/StuProductionSchedule.aspx"
	posturl = "http://202.115.133.173:805/Common/Handler/UserLogin.ashx"
	def get_js():
		f = open("./crawler/cdut/md5.js", 'r', encoding='UTF-8')  
		line = f.readline()  
		htmlstr = ''  
		while line:  
			htmlstr = htmlstr + line  
			line = f.readline()  
		return htmlstr
	   
	jsstr = get_js()  
	js = execjs.compile(jsstr)

	sign=str(int(time.time() * 1000));
	pwd=js.call('hex_md5',username+sign+js.call('hex_md5',password))

	#post需要的表单数据，类型为字典
	postdata = {
		'Action': 'Login',
		'userName': username,
		'pwd': pwd,
		'sign': sign,
	}

	#使用seesion登录，这样的好处是可以在接下来的访问中可以保留登录信息
	session = requests.session()

	#requests 的session登录，以post方式，参数分别为url、headers、data
	session.post(posturl, postdata)

	html=session.get(Default).text
	ID=re.findall('Classroom/ProductionSchedule/StuProductionSchedule.aspx([\S]+)"', html)
	if not ID:
		return None
	url+=ID[0]

	html=session.get(url).text

	schedule=pandas.read_html(html)

	FIRST=schedule[1][0][2]
	COLUMNS=1
	INDEX=2
	YEAR=int(re.findall('期:(.*?)-', schedule[0][0][1])[0])
	MONTH=int(FIRST[3:5])
	DAY=int(FIRST[6:8])
	TIME=datetime.datetime(YEAR,MONTH,DAY)

	SHOUR=[8,9,10,11,0,14,15,16,17,19,20,20]
	SMINU=[10,45,15,5,0,30,20,25,15,10,00,50]
	EHOUR=[8,9,11,11,0,15,16,17,18,19,20,21]
	EMINU=[50,45,00,50,0,15,5,10,00,55,45,35]

	cal = Calendar()
	cal.add('prodid', '-//Luna Schedule//LunaSchedule.cn//')
	cal.add('version', '2.0')

	Course=[]
	for index,row in schedule[2].iterrows():
		pandas.set_option('max_colwidth',50)
		mininame=re.findall('\((.*?)\)', str(row))
		maxname=re.findall('\)(.*?)\(', str(row))
		pandas.set_option('max_colwidth',200)
		location=re.findall('\室\[.*?\]', str(row))
		for i,j,k in zip(mininame,maxname,location):
			Course.append([i,j,k])

	def SearchCourse(ceil):
		for i in Course:
			if re.search(i[0],str(ceil)):
				return i

	stime=datetime.time()
	for i in range(20):
		for j in range(7):
			for k in range(12):
				x=COLUMNS+12*j+k
				y=INDEX+i
				if schedule[1][x][y]==schedule[1][x-1][y]:
					continue
				else:
					course=SearchCourse(schedule[1][x-1][y])
					if course:
						etime=datetime.time(hour=EHOUR[k-1],minute=EMINU[k-1])
						event=Event()
						event.add('summary', course[1])
						event.add('dtstart', datetime.datetime.combine(TIME,stime))
						event.add('dtend', datetime.datetime.combine(TIME,etime))
						event.add('location', re.findall('[A-Z][\d]([\S]+)', schedule[1][x-1][y])[0])
						cal.add_component(event)
					stime=datetime.time(hour=SHOUR[k],minute=SMINU[k])
			course=SearchCourse(schedule[1][x][y])
			if course:
				etime=datetime.time(hour=EHOUR[k],minute=EMINU[k])
				event=Event()
				event.add('summary', course[1])
				event.add('dtstart', datetime.datetime.combine(TIME,stime))
				event.add('dtend', datetime.datetime.combine(TIME,etime))
				event.add('location', re.findall('[A-Z][\d]([\S]+)', schedule[1][x][y])[0])
				cal.add_component(event)
			TIME+=datetime.timedelta(days=1)
	return cal.to_ical()
