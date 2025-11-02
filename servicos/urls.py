# barbearia_manager/servicos/urls.py

from django.urls import path
from .views import ServicoCreateView, ServicoListView, ServicoUpdateView, ServicoDeleteView

app_name = 'servicos'

urlpatterns = [
    path('', ServicoListView.as_view(), name='lista_servicos'), 
    path('novo/', ServicoCreateView.as_view(), name='cria_servico'), 
    path('<int:pk>/editar/', ServicoUpdateView.as_view(), name='edita_servico'),
    path('<int:pk>/excluir/', ServicoDeleteView.as_view(), name='exclui_servico'),
]