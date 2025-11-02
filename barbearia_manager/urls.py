# barbearia_manager/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from agendamentos.views import dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),    
    path('', dashboard_view, name='dashboard'),
    path('servicos/', include('servicos.urls')),
    path('barbeiros/', include('barbeiros.urls')),
    path('clientes/', include('clientes.urls')),
    path('agendamentos/', include('agendamentos.urls')),
]