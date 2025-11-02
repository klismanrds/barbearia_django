# barbearia_manager/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # O admin precisa ser incluído no public schema, mas funcionará no tenant
    path('admin/', admin.site.urls), 

    # Rotas da Aplicação (Dashboard será a página inicial do tenant)
    path('', include('agendamentos.urls')), 

    # Adicione rotas de login/logout aqui futuramente
]