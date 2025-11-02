# barbearia_manager/barbeiros/urls.py

from django.urls import path
from .views import BarbeiroCreateView, BarbeiroListView, BarbeiroUpdateView, BarbeiroDeleteView, AlterarSenhaView

app_name = 'barbeiros'

urlpatterns = [
    path('', BarbeiroListView.as_view(), name='lista_barbeiros'), 
    path('novo/', BarbeiroCreateView.as_view(), name='cria_barbeiro'), 
    path('<int:pk>/editar/', BarbeiroUpdateView.as_view(), name='edita_barbeiro'),
    path('<int:pk>/excluir/', BarbeiroDeleteView.as_view(), name='exclui_barbeiro'),
    path('alterar-senha/', AlterarSenhaView.as_view(), name='alterar_senha'),
]