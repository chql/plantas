from django.db import models
from django.contrib import admin


class Planta(models.Model):
    """
    Uma planta a partir da qual uma receita pode ser preparada.
    """
    TIPO_CASCA = 'casca'
    TIPO_CERA = 'cera'
    TIPO_FLOR = 'flor'
    TIPO_FOLHA = 'folha'
    TIPO_FRUTA = 'fruta'
    TIPO_RAIZ = 'raiz'
    TIPO_SEIVA = 'seiva'

    TIPOS_CHOICES = (
        (TIPO_CASCA, 'casca'),
        (TIPO_CERA, 'cera'),
        (TIPO_FLOR, 'flor'),
        (TIPO_FOLHA, 'folha'),
        (TIPO_FRUTA, 'fruta'),
        (TIPO_RAIZ, 'raiz'),
        (TIPO_SEIVA, 'seiva')
    )

    nome = models.CharField(max_length=128)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='static/uploads/')

    tipo = models.CharField(choices=TIPOS_CHOICES, max_length=16)

    def __str__(self):
        return self.nome


class Categoria(models.Model):
    """
    Categoria de enfermidade.
    """
    descricao = models.CharField(max_length=64)

    def __str__(self):
        return self.descricao


class Sintoma(models.Model):
    """
    Um sintoma para qual uma receita oferece tratamento.
    """
    descricao = models.CharField(max_length=32)
    chave = models.CharField(max_length=32)
    categoria = models.ForeignKey(Categoria,
                                  on_delete=models.SET_DEFAULT,
                                  default=1,
                                  related_name='sintomas')

    def __str__(self):
        return self.descricao


class Receita(models.Model):
    """
    Uma receita preparada a partir de uma planta no tratamento de sintomas.
    """
    titulo = models.TextField()
    conteudo = models.TextField()
    plantas_base = models.ManyToManyField(Planta)

    sintomas = models.ManyToManyField(Sintoma, related_name='receitas')

    def __str__(self):
        return self.titulo


admin.site.register(Planta)
admin.site.register(Receita)
admin.site.register(Categoria)
admin.site.register(Sintoma)
