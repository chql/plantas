from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.http.response import JsonResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.views.generic import View, CreateView, ListView, UpdateView, DeleteView, DetailView
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .forms import PlantaForm, ReceitaForm
from .models import Planta, Receita, Sintoma


def index_view(request):
    """
    Exibe a pagina inicial para o usuario.
    :param request:
    :return:
    """
    return render(request, 'index.html', {
        'sintomas': Sintoma.objects.all()[:5]
    })


def receitas_card(request):
    """
    Exibe cartoes de receitas filtradas por sintoma ou planta.
    :param request:
    :return:
    """
    sintoma = request.GET.get('sintoma')
    categoria = request.GET.get('categoria')

    if sintoma is not None:
        receitas = Receita.objects.filter(sintomas__in=[int(sintoma)]).all()
    elif categoria is not None:
        receitas = Receita.objects.filter(plantas_base__tipo=categoria).all()
    else:
        receitas = Receita.objects.all()[:5]

    return render(request, 'receitas/card.html', {
        'receitas': receitas or Receita.objects.all()[:5]
    })


@login_required
def dashboard_view(request):
    """
    Exibe o menu de administracao.
    :param request:
    :return:
    """
    return render(request, 'dashboard.html')


@require_http_methods(['PUT'])
@csrf_exempt
@login_required
def sintomas_put(request):
    """
    Adiciona/seleciona um sintoma.
    Esse endpoint busca um sintoma e retorna sua identificacao
    se um sintoma correspondente nao existir ele sera criado.
    :param request:
    :return:
    """
    descricao = request.GET['q']
    chave = slugify(descricao)
    try:
        sintoma = Sintoma.objects.get(chave=chave)
    except Sintoma.DoesNotExist:
        sintoma = Sintoma.objects.create(descricao=descricao,
                                         chave=chave)
    return JsonResponse({
        'id': sintoma.id,
        'descricao': sintoma.descricao,
        'chave': sintoma.chave
    })


class SintomasFilter(View):
    """
    Permite filtrar plantas e receitas por um conjunto de sintomas.
    """
    list_template_name = 'sintomas/list.html'
    filter_template_name = 'sintomas/filter.html'

    def get(self, request):
        """
        Exibe a pagina para selecao de sintomas.
        :param request:
        :return:
        """
        return render(request,
                      self.list_template_name,
                      {'sintomas': Sintoma.objects.all()})

    def post(self, request):
        """
        Filtra as plantas e receitas atraves dos sintomas selecionados.
        :param request:
        :return:
        """
        pks = map(int, request.POST.getlist('sintomas'))
        sintomas = Sintoma.objects.filter(id__in=pks)
        receitas = Receita.objects.prefetch_related('plantas_base')

        for sintoma in sintomas:
            receitas = receitas.intersection(sintoma.receitas.all())

        resultados = {}
        for receita in receitas.all():
            for planta in receita.plantas_base.all():
                resultado = resultados.get(planta.id)

                if resultado is None:
                    resultado = {'planta': planta, 'receitas': []}
                    resultados[planta.id] = resultado

                resultado['receitas'].append(receita)

        return render(request,
                      self.filter_template_name,
                      {'resultados':  resultados})


class ReceitaCreate(LoginRequiredMixin, CreateView):
    """
    Permite cadastrar uma receita.
    """
    model = Receita
    form_class = ReceitaForm
    template_name = 'receitas/edit.html'
    success_url = reverse_lazy('receitas-list')


class ReceitaDetail(DetailView):
    """
    Visualizacao completa de uma receita.
    """
    model = Receita
    template_name = 'receitas/detail.html'
    context_object_name = 'receita'


class ReceitaList(LoginRequiredMixin, ListView):
    """
    Exibe as receitas cadastradas.
    """
    model = Receita
    template_name = 'receitas/list.html'
    context_object_name = 'receitas'


class ReceitaUpdate(LoginRequiredMixin, UpdateView):
    """
    Permite alterar uma receita.
    """
    model = Receita
    form_class = ReceitaForm
    template_name = 'receitas/edit.html'
    success_url = reverse_lazy('receitas-list')
    context_object_name = 'receita'


class ReceitaDelete(LoginRequiredMixin, DeleteView):
    """
    Permite remover uma receita do banco de dados.
    """
    model = Receita
    template_name = 'receitas/delete.html'
    success_url = reverse_lazy('receitas-list')
    context_object_name = 'receita'


class PlantaCreate(LoginRequiredMixin, CreateView):
    """
    Permite adicionar uma planta.
    """
    model = Planta
    form_class = PlantaForm
    template_name = 'plantas/edit.html'
    success_url = reverse_lazy('plantas-list')


class PlantaList(LoginRequiredMixin, ListView):
    """
    Exibe as plantas cadastradas.
    """
    model = Planta
    template_name = 'plantas/list.html'
    context_object_name = 'plantas'


class PlantaUpdate(LoginRequiredMixin, UpdateView):
    """
    Permite alterar uma planta.
    """
    model = Planta
    form_class = PlantaForm
    template_name = 'plantas/edit.html'
    success_url = reverse_lazy('plantas-list')
    context_object_name = 'planta'


class PlantaDelete(LoginRequiredMixin, DeleteView):
    """
    Permite remover uma planta do banco de dados.
    """
    model = Planta
    template_name = 'plantas/delete.html'
    success_url = reverse_lazy('plantas-list')
    context_object_name = 'planta'

