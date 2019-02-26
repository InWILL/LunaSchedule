# LunaSchedule

## License
本项目使用**MIT许可证**
允许**任何人**使用本项目进行二次开发、销售

*LunaSchedule*是一款专为大学生设计的日历订阅网站

## Special Thanks：
InWILL
Mellow
Oriville

## Requirements
- Python      3.7.2
- Django      2.1.7
- PostgreSQL  11
- Nginx       1.14.2
- Uwsgi       2.0
- libpq-dev   9.3.24

### Python plugins
- psycopg2
- uwsgi
- requests
- PyExecJS
- pandas
- pytz
- icalendar

## Installation
Add `location` your nginx setting
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

Initialize Django
    python manage.py makemigrations
    python manage.py migrate

## Run
   uwsgi --ini uwsgi.ini & nginx
