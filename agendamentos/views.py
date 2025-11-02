# agendamentos/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Agendamento
from .forms import AgendamentoForm
from django.utils import timezone
from django.shortcuts import render
from barbeiros.models import Barbeiro
from django.db.models import Sum, F, Value, DecimalField
from clientes.models import Cliente
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models.functions import Coalesce

# Mixin de autenticação
class AgendamentoLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')

# 1. Listagem de Agendamentos
class AgendamentoListView(AgendamentoLoginRequiredMixin, ListView):
    model = Agendamento
    template_name = 'agendamentos/agendamento_list.html'
    context_object_name = 'agendamentos' 
    
# 2. Criação de Agendamento
# 2. Criação de Agendamento
class AgendamentoCreateView(AgendamentoLoginRequiredMixin, CreateView):
    model = Agendamento
    form_class = AgendamentoForm
    template_name = 'agendamentos/agendamento_form.html'
    success_url = reverse_lazy('agendamentos:lista_agendamentos')
    
    def form_valid(self, form):
        # 1. COMBINAÇÃO DA DATA E HORA
        data = form.cleaned_data.get('data')
        hora = form.cleaned_data.get('hora')
        
        if data and hora:
            # Combina os objetos date e time em um datetime
            data_hora_combinada = timezone.datetime.combine(data, hora)
            # Torna o datetime timezone-aware (ajustado ao fuso horário configurado)
            form.instance.data_hora_inicio = timezone.make_aware(data_hora_combinada)

        # 2. Lógica de Preço e Duração (MANTIDA)
        servico_selecionado = form.cleaned_data.get('servico')
        if servico_selecionado:
            form.instance.preco_final = servico_selecionado.preco
            form.instance.duracao_minutos = servico_selecionado.duracao_minutos
            
        return super().form_valid(form)


# 3. Edição de Agendamento
class AgendamentoUpdateView(AgendamentoLoginRequiredMixin, UpdateView):
    model = Agendamento
    form_class = AgendamentoForm
    template_name = 'agendamentos/agendamento_form.html' 
    success_url = reverse_lazy('agendamentos:lista_agendamentos')
    
    def form_valid(self, form):
        # 1. COMBINAÇÃO DA DATA E HORA (IGUAL AO CREATE)
        data = form.cleaned_data.get('data')
        hora = form.cleaned_data.get('hora')
        
        if data and hora:
            data_hora_combinada = timezone.datetime.combine(data, hora)
            form.instance.data_hora_inicio = timezone.make_aware(data_hora_combinada)
            
        # 2. Lógica de Preço e Duração (MANTIDA)
        servico_selecionado = form.cleaned_data.get('servico')
        if servico_selecionado:
            form.instance.preco_final = servico_selecionado.preco
            form.instance.duracao_minutos = servico_selecionado.duracao_minutos
            
        return super().form_valid(form)

# 4. Exclusão de Agendamento
class AgendamentoDeleteView(AgendamentoLoginRequiredMixin, DeleteView):
    model = Agendamento
    template_name = 'agendamentos/agendamento_confirm_delete.html'
    success_url = reverse_lazy('agendamentos:lista_agendamentos')

@login_required(login_url=reverse_lazy('login')) # Confirma a proteção de login
def dashboard_view(request):
    hoje = timezone.localdate()
    
    # 1. Agendamentos de Hoje
    agendamentos_hoje_queryset = Agendamento.objects.filter(
        data_hora_inicio__date=hoje
    ).select_related('cliente', 'servico', 'barbeiro')
    
    # 2. Faturamento de Hoje
    faturamento_hoje = agendamentos_hoje_queryset.filter(
        status='E' # 'E' = Concluído
    ).aggregate(
        total=Sum('preco_final')
    )['total'] or 0.00

    # 3. Total de Clientes
    total_clientes = Cliente.objects.count()

    # 4. Barbeiros Ativos
    barbeiros_ativos = Barbeiro.objects.filter(ativo=True).count()
    
    # 5. Próximos Agendamentos
    proximos_agendamentos_list = agendamentos_hoje_queryset.order_by('data_hora_inicio')


    # 6. LÓGICA DO RANKING DE BARBEIROS (NOVA IMPLEMENTAÇÃO)
    # Calcula o ganho total (Comissão) de cada Barbeiro a partir de agendamentos CONCLUÍDOS.
    ranking_data = Agendamento.objects.filter(
        status='E'
    ).values('barbeiro__usuario__first_name', 'barbeiro__comissao_percentual') \
    .annotate(
        # 1. Soma o faturamento total dos agendamentos
        total_faturado=Sum('preco_final')
    ) \
    .annotate(
        # 2. Calcula o Ganho Total (Comissão) = Total * (Comissão % / 100)
        ganho_total=Coalesce(F('total_faturado') * F('barbeiro__comissao_percentual') / 100.0, 
        Value(0.00), output_field=DecimalField()
        )
    ) \
    .order_by('-ganho_total')[:5] # Ordena e limita aos 5 primeiros

    
    context = {
        'agendamentos_hoje_count': proximos_agendamentos_list.count(),
        'faturamento_hoje': faturamento_hoje,
        'total_clientes': total_clientes,
        'barbeiros_ativos': barbeiros_ativos,
        'agendamentos_hoje_list': proximos_agendamentos_list,
        'lista_barbeiros_com_ganhos': ranking_data, # Passa os dados do ranking para o template
    }
    
    return render(request, 'dashboard.html', context)