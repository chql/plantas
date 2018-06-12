"""plyntas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from plyntas.views import index_view, dashboard_view, sintomas_put, receitas_card,\
                            PlantaCreate, PlantaList, PlantaUpdate, PlantaDelete,\
                            ReceitaCreate, ReceitaList, ReceitaUpdate, ReceitaDelete, ReceitaDetail,\
                            SintomasFilter

urlpatterns = [
    path('', index_view, name='index'),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),

    path('plantas/create', PlantaCreate.as_view(), name='plantas-create'),
    path('plantas/list', PlantaList.as_view(), name='plantas-list'),
    path('plantas/<slug:pk>/update', PlantaUpdate.as_view(), name='plantas-update'),
    path('plantas/<slug:pk>/delete', PlantaDelete.as_view(), name='plantas-delete'),

    path('receitas/create', ReceitaCreate.as_view(), name='receitas-create'),
    path('receitas/list', ReceitaList.as_view(), name='receitas-list'),
    path('receitas/<slug:pk>/update', ReceitaUpdate.as_view(), name='receitas-update'),
    path('receitas/<slug:pk>/delete', ReceitaDelete.as_view(), name='receitas-delete'),
    path('receitas/<slug:pk>/detail', ReceitaDetail.as_view(), name='receitas-detail'),
    path('receitas/cards', receitas_card, name='receitas-card'),

    path('receitas/search', SintomasFilter.as_view(), name='sintomas-filter'),
    path('sintomas', sintomas_put, name='sintomas'),

    path('dashboard', dashboard_view, name='dashboard')
]
