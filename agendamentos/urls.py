# agendamentos/urls.py
from django.urls import path
from .views import (
    AgendamentoListView, 
    AgendamentoCreateView, 
    AgendamentoUpdateView, 
    AgendamentoDeleteView
)

app_name = 'agendamentos'

urlpatterns = [
    # Rotas de Listagem e Criação
    path('', AgendamentoListView.as_view(), name='lista_agendamentos'),
    path('novo/', AgendamentoCreateView.as_view(), name='cria_agendamento'),
    
    # Rotas de Edição e Exclusão (requerem a chave primária: pk)
    path('<int:pk>/editar/', AgendamentoUpdateView.as_view(), name='edita_agendamento'),
    path('<int:pk>/excluir/', AgendamentoDeleteView.as_view(), name='exclui_agendamento'),
]