# clientes/urls.py
from django.urls import path
from .views import ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView

app_name = 'clientes'

urlpatterns = [
    # Rotas de Listagem e Criação
    path('', ClienteListView.as_view(), name='lista_clientes'),
    path('novo/', ClienteCreateView.as_view(), name='cria_cliente'),
    
    # Rotas de Edição e Exclusão (requerem a chave primária: pk)
    path('editar/<int:pk>/', ClienteUpdateView.as_view(), name='edita_cliente'),
    path('excluir/<int:pk>/', ClienteDeleteView.as_view(), name='exclui_cliente'),
]