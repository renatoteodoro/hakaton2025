from django.urls import path
from . import views

urlpatterns = [
    # --- Rota Principal ---
    path('', views.dashboard, name='dashboard'),

    # --- Funcionalidade 1: Escriba Inteligente (Reuniões) ---
    path('upload/', views.upload_reuniao, name='upload_reuniao'),
    path('reuniao/<int:pk>/', views.detalhe_reuniao, name='detalhe_reuniao'),

    # --- Funcionalidade 2: Mentoria de Feedback (Líderes) ---
    path('mentoria/', views.mentoria_feedback, name='mentoria_feedback'),
    
    # Rota HTMX (Mágica Oculta): Chamada automaticamente enquanto digita
    path('checar-feedback/', views.checar_feedback_htmx, name='checar_feedback'),

    # --- Funcionalidade 3: Tradutor Cultural (RAG) ---
    path('glossario/', views.glossario_cultural, name='glossario'),

    # --- Funcionalidade 4: Gestão de Colaboradores (RH) ---
    path('colaboradores/', views.lista_colaboradores, name='lista_colaboradores'),
]