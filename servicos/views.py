from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Servico
from .forms import ServicoForm

class ServicoCreateView(LoginRequiredMixin, CreateView):
    model = Servico
    form_class = ServicoForm
    template_name = 'servicos/servico_form.html'
    success_url = reverse_lazy('servicos:lista_servicos') # Redireciona para a lista
    
    # Opcional: Se precisar passar dados adicionais ao formulário (ex: barbearia_id)
    def form_valid(self, form):
        return super().form_valid(form)
    

class ServicoListView(LoginRequiredMixin, ListView):
    model = Servico
    context_object_name = 'servicos'
    template_name = 'servicos/servico_list.html'

    def get_queryset(self):
        mostrar_todos = self.request.GET.get('todos') == '1'
        qs = Servico.objects.all().order_by('-ativo', 'nome')
        if not mostrar_todos:
            qs = qs.filter(ativo=True)
        return qs

class ServicoUpdateView(LoginRequiredMixin, UpdateView):
    model = Servico
    form_class = ServicoForm
    template_name = 'servicos/servico_form.html' # Reutiliza o template de cadastro
    success_url = reverse_lazy('servicos:lista_servicos')

class ServicoDeleteView(LoginRequiredMixin, DeleteView):
    model = Servico
    template_name = 'servicos/servico_confirm_delete.html' # Você precisará criar este template
    success_url = reverse_lazy('servicos:lista_servicos')