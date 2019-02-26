from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('Login/', views.Login, name='login'),
	path('Logout/', views.Logout, name='logout'),
	path('Join/', views.Join, name='join'),
	path('Home/', views.Home, name='home'),
	path('Import/', views.Import, name='import'),
	path('Info/', views.Info, name='info'),
	path('Donate/', views.Donate, name='donate'),
]