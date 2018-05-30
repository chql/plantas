from plyntas.models import Planta, Receita
from django import forms


class ReceitaForm(forms.ModelForm):
    """
    Formulario de validacao de receitas.
    """
    def __init__(self, *args, **kwargs):
        super(ReceitaForm, self).__init__(*args, **kwargs)
        self.fields['plantas_base'].widget.attrs.update({'class': 'form-control form-control-lg'})

    class Meta:
        model = Receita
        fields = ['titulo', 'conteudo', 'plantas_base', 'sintomas']


class PlantaForm(forms.ModelForm):
    """
    Formulario de validacao de plantas.
    """
    def __init__(self, *args, **kwargs):
        super(PlantaForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].widget.attrs.update({'class': 'form-control form-control-lg'})

    class Meta:
        model = Planta
        fields = ['nome', 'tipo', 'descricao', 'imagem']
