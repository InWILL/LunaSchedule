from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from . import models
import hashlib
import time
from icalendar import Calendar

def index(request):
	template = loader.get_template('Index.html')
	context = {}
	return HttpResponse(template.render(context, request))
	
def Login(request):
	if request.session.get('Status',None):#禁止重复登陆
		return HttpResponseRedirect('/Home/')
	if request.method == "POST":
		email = request.POST.get('email')#关键字 默认值
		password = request.POST.get('password')
		message = "请检查填写的内容！"
		password = hashlib.md5(bytes(str(password),encoding='utf-8')).hexdigest()
		if email and password:
			email = email.strip()
			try:
				user = models.User.objects.get(email=email)
				if user.password == password:
					request.session['Status'] = True
					request.session['User_ID'] = user.id
					request.session['User_Name'] = user.username
					request.session['User_Email'] = user.email
					request.session['User_Url'] = user.url
					return HttpResponseRedirect('/Home/')
				else:
					message = "密码不正确！"
			except:
				message = "用户不存在！"
	return render(request,'Login.html',locals())

def Join(request):
	if request.method == "POST":
		username = request.POST.get('username')
		email = request.POST.get('email')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		message = "请检查填写的内容！"
		if password1 != password2:
			message = "两次输入的密码不同！"
			return render(request,'Join.html',locals())
		if len(password1) < 4:
			message = "密码不得小于4位！"
			return render(request,'Join.html',locals())
		if username and email and password1 and password2:
			username = username.strip()
			email = email.strip()
			try:
				user = models.User.objects.get(email=email)
				if user:
					message = "邮箱已注册！"
					return render(request,'Join.html',locals())
			except:
				password1 = hashlib.md5(bytes(str(password1),encoding='utf-8')).hexdigest()
				new_user = models.User.objects.create()
				new_user.username = username
				new_user.email = email
				new_user.password = password1
				new_user.calendar = bytes(0)
				new_user.save()
				message = "注册成功！"
	return render(request,'Join.html',locals())

def Logout(request):
	request.session.flush()
	return HttpResponseRedirect('/')

def Home(request):
	if not request.session.get('Status',None):
		return HttpResponseRedirect('/')
	Url='webcal://'+request.get_host()+'/s/'+request.session['User_Url']
	return render(request,'Home.html',locals())

def Import(request):
	if request.method == "POST":
		school = request.POST.get('school')
		username = request.POST.get('username')
		password = request.POST.get('password')
		if school == "成都理工大学":
			from crawler.cdut import cdut
			cal = cdut.GetCalendar(username,password)
		else:
			message = "请选择学校！"
			return render(request,'Import.html',locals())
		if not cal:
			message = "请检查填写的内容！"
			return render(request,'Import.html',locals())
		email = request.session['User_Email']
		url = hashlib.md5(bytes(email,encoding='utf-8')).hexdigest()[8:-8]+'.ics'
		calfile = open('./s/'+url, 'wb')
		calfile.write(cal)
		calfile.close()
		models.User.objects.filter(email=email).update(url=url)
		request.session['User_Url'] = url
		message = "导入成功！"
	return render(request,'Import.html',locals())

def Info(request):
	if request.method == "POST":
		email = request.session['User_Email']
		password = request.POST.get('password')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		user = models.User.objects.get(email=email)
		password = hashlib.md5(bytes(str(password),encoding='utf-8')).hexdigest()
		if user.password != password:
			message = "原密码错误！"
			return render(request,'Info.html',locals())
		if len(password1) < 4:
			message = "密码不得小于4位！"
			return render(request,'Info.html',locals())
		if password1 == password2:
			password1 = hashlib.md5(bytes(str(password1),encoding='utf-8')).hexdigest()
			models.User.objects.filter(email=email).update(password=password1)
			message = "密码修改成功！"
		else:
			message = "两次输入的密码不同！"
	return render(request,'Info.html',locals())

def Donate(request):
	return render(request,'Donate.html')
