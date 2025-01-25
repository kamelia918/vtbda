# <<<<<<< HEAD
# from django.urls import path

# from django.contrib.auth import views as auth_views

# from veille_app.views import *

# urlpatterns = [
#     path('', index, name='index'),
#     path('accounts/login/', Login.as_view(), name='login'),
#     path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
# ]
# =======
from django.urls import path

from django.contrib.auth import views as auth_views

from veille_app.views import *
from django.conf.urls.static import static  

urlpatterns = [
    path('', index, name='index'),
    path('veilleur', veilleur_view, name='veilleur'),
     path('analystekanban', analyste_kanban_view, name='analysteK'),
    path('analyste', analyste_view, name='analyste'),
    path('accounts/login/', Login.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('kanban/', kanban_view, name='kanban'),
    path('update_task_status/', update_task_status, name='update_task_status'),
    
    path('content/<int:task_id>/', task_content, name='task_content'),

    path('articles/', fetch_arxiv_articles, name='fetch_arxiv_articles'),
    path('save_article/', save_article, name='save_article'),
    path('delete_article/', delete_article, name='delete_article'),
    path('plosarticle/', fetch_plosone_articles, name='plos_article'),
    path('author-statistics/', author_statistics, name='author_statistics'),
    path('word-statistics/', word_statistics, name='word_statistics'),
    # path('generate_report/', rapport, name='generate_report'),
     path('rapports/', liste_rapports, name='liste_rapports'),
    path('rapports/<int:rapport_id>/', detail_rapport, name='detail_rapport'),
    path('creer-rapport/', creer_rapport, name='creer_rapport'),
    path('rapport/', rapport, name='rapport'),
    path('task_saved_articles/<int:task_id>/', task_saved_articles, name='task_saved_articles'),

# KAHINA
   path('homeAnalyste', home, name='home'),
    path('add_note/', create_note, name='add_note'),
    path('article/<int:pk>/', article_detail, name='article_detail'),  # Page de détail d'article
    path('select_article_for_note/', select_article_for_note, name='select_article_for_note'),
    path('article/<int:article_id>/add_note/', create_note, name='create_note'),
    path('generate_table/<int:article_id>/', generate_table, name='generate_table'),  # Vérifiez cette ligne
    path('assistant/', assistant_redirect, name='assistant_redirect'),
    path('article/<int:article_id>/notes/', article_notes, name='article_notes'),
    path('generate-full-report/', generate_full_report, name='generate_full_report'),
    path('generate-pdf/', generate_pdf, name='generate_pdf'),



    #--------------BEKARI

    path('content/<int:task_id>/', task_content, name='task_content'),
    path('articles/<int:task_id>/', fetch_arxiv_articles, name='fetch_arxiv_articles'),
    path('save_article/<int:task_id>/', save_article, name='save_article'),
    path('delete_article/', delete_article, name='delete_article'),
    path('plosarticle/<int:task_id>/', fetch_plosone_articles, name='plos_article'),
    path('fetch-content/<int:task_id>/', fetch_content, name='fetch_content'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# >>>>>>> origin/main