# LunaSchedule
**LunaSchedule**是一款专为大学生设计的日历订阅网站  
LunaSchedule开发交流群：881520051

用了一学期超级课程表，被50+M的内存、巨慢的加载速度劝退了，于是自己设计一款课程表  
支持Android、IOS  
添加日历订阅，自动导入到系统日历，无需安装任何app  

如果您喜欢此网站，请为我们进行捐赠，网站成本极低，基本上每捐赠1￥，运营时间则可多延长1天

![Donate](http://images.cnblogs.com/cnblogs_com/InWILL/898968/o_pai.jpg)

## License
本项目使用**MIT许可证**
允许**任何人**使用本项目进行二次开发、销售

## Special Thanks：
InWILL  
Mellow  
Oriville  

## Standard  
请尽量使用requests模拟登陆，而不是复杂的urllib  
统一函数名、参数名、返回值（返回icalendar日历结构）  
```
def GetCalendar(username, password):
    return cal.to_ical()
```

## Requirements
- Python      3.7.2
- Django      2.1.7
- PostgreSQL  11
- Nginx       1.14.2
- Uwsgi       2.0
- libpq-dev   9.3.24

### Python plugins
- psycopg2    2.7.6
- uwsgi       2.0.18
- requests    1.0.2
- PyExecJS    1.5.1
- pandas      0.24.1
- pytz        2018.9
- icalendar   4.0.3

## Installation
Add location your nginx setting
```
location / {
    include  uwsgi_params;
    uwsgi_pass  127.0.0.1:8000;
    uwsgi_param UWSGI_SCRIPT LunaSchedule.wsgi;
    uwsgi_param UWSGI_CHDIR /Luna;
    index  index.html index.htm;
    client_max_body_size 35m;
}
location /static {
    alias /LunaSchedule/static;
}
location /s {
    alias /LunaSchedule/s;
}
```

Initialize Django
```
python manage.py makemigrations
python manage.py migrate
```

## Run
- `uwsgi --ini uwsgi.ini & nginx`
