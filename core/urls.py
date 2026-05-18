from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cadastro/', views.cadastro_cliente, name='cadastro_cliente'),
    path('publicacao/<int:id>/', views.detalhe_publicacao, name='detalhe_publicacao'),
    path('minha-conta/', views.minha_conta, name='minha_conta'),

    path(
        'login/',
        LoginView.as_view(template_name='core/login.html'),
        name='login'
    ),

    path(
        'logout/',
        LogoutView.as_view(next_page='home'),
        name='logout'
    ),
]