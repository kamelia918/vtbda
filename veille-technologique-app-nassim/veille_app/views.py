
# <<<<<<< HEAD
# # from django.shortcuts import render
# # from django.contrib.auth.decorators import login_required
# # from django.contrib.auth.views import LoginView
# # from django.urls import reverse_lazy

# # # Create your views here.
# # @login_required
# # def index(request):
# #     # Fetch stats
# #     context = {
# #         # You can add stats to the context here
# #     }
# #     return render(request, 'index.html', context)

# # class Login(LoginView):
# #     template_name = 'auth-login-basic.html'

# #     def form_valid(self, form):
# #         # After login, redirect to the admin page
# #         return super().form_valid(form)

# #     def get_success_url(self):
# #         # You can customize the success URL here
# #         return reverse_lazy('admin:index')  # Redirect to Django Admin


# # from .models import Task

# # def kanban_board(request):
# #     tasks = Task.objects.all()  # Get all tasks
# #     context = {
# #         'tasks': tasks,
# #     }
# #     return render(request, 'kanban_board.html', context)


# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.views import LoginView
# from .models import Task

# # Create your views here.
# @login_required
# def index(request):
#     tasks_todo = Task.objects.filter(is_completed=False, is_in_progress=False)
#     tasks_in_progress = Task.objects.filter(is_in_progress=True)
#     tasks_completed = Task.objects.filter(is_completed=True)
    
#     context = {
#         'tasks_todo': tasks_todo,
#         'tasks_in_progress': tasks_in_progress,
#         'tasks_completed': tasks_completed,
#     }
#     return render(request, 'index.html', context)

# class Login(LoginView):
#     template_name = 'auth-login-basic.html'

#     def form_valid(self, form):
#         # Add any extra logic here if needed
#         return super().form_valid(form)
    

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .models import Task
# import json

# @csrf_exempt
# def update_task_status(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         task_id = data.get('task_id')
#         status = data.get('status')

#         # Update the task status
#         task = Task.objects.get(id=task_id)
#         task.status = status
#         task.save()

#         return JsonResponse({'success': True})
# =======




# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.views import LoginView
# from django.urls import reverse_lazy

# # Create your views here.
# @login_required
# def index(request):
#     # Fetch stats
#     context = {
#         # You can add stats to the context here
#     }
#     return render(request, 'index.html', context)

# class Login(LoginView):
#     template_name = 'auth-login-basic.html'

#     def form_valid(self, form):
#         # After login, redirect to the admin page
#         return super().form_valid(form)

#     def get_success_url(self):
#         # You can customize the success URL here
#         return reverse_lazy('admin:index')  # Redirect to Django Admin


# from .models import Task

# def kanban_board(request):
#     tasks = Task.objects.all()  # Get all tasks
#     context = {
#         'tasks': tasks,
#     }
#     return render(request, 'kanban_board.html', context)


import base64
from io import BytesIO
import io
from sqlite3 import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
import nltk
from .models import Content, Task
import json
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.data import find
from wordcloud import WordCloud
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import io
import base64
from matplotlib import pyplot as plt
from collections import Counter

# Create your views here.
def index(request):
     # Check if the logged-in user is in the 'decideur' group
    if request.user.groups.filter(name='Décideur').exists():
        # If user is in 'decideur' group, fetch all tasks
        tasks = Task.objects.all()
        tasks_todo = tasks.filter(status='To Do')
        tasks_in_progress = tasks.filter(status='In Progress')
        tasks_completed = tasks.filter(status='Completed')

    else:
        # If user is not in 'decideur' group, fetch tasks assigned to the logged-in user
        if request.user.groups.filter(name='Veilleur').exists():
        # If user is in 'decideur' group, fetch all tasks
        
            return redirect(veilleur_view)
        else:
        # If user is not in 'decideur' group, fetch tasks assigned to the logged-in user
            if request.user.groups.filter(name='Analyste').exists():
            # If user is in 'decideur' group, fetch all tasks
            
                return redirect(analyste_view)
        

    return render(request, 'kanban.html', {'tasks': tasks,'tasks_todo':tasks_todo,'tasks_in_progress':tasks_in_progress,'tasks_completed':tasks_completed})

class Login(LoginView):
    template_name = 'auth-login-basic.html'

    def form_valid(self, form):
        # Add any extra logic here if needed
        return super().form_valid(form)
    
from django.shortcuts import render
from .models import Task


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import Group
from .models import Task

@login_required
def kanban_view(request):

    # Check if the logged-in user is in the 'decideur' group
    if request.user.is_superuser or request.user.groups.filter(name='Décideur').exists():
    # If user is a superuser or in 'Décideur' group, fetch all tasks
        tasks = Task.objects.all()

        
    else:
        if request.user.groups.filter(name='Veilleur').exists():
        # If user is in 'decideur' group, fetch all tasks
        
            return redirect(veilleur_view)
        else:
        # If user is not in 'decideur' group, fetch tasks assigned to the logged-in user
            if request.user.groups.filter(name='Veilleur').exists():
            # If user is in 'decideur' group, fetch all tasks
            
                return redirect(analyste_view)

    return render(request, 'kanban.html', {'tasks': tasks})

# @login_required
# def kanban_view(request):
#     # Get tasks assigned to the logged-in user
#     tasks = Task.objects.filter(assignments__user=request.user).prefetch_related('assignments__user')

#     return render(request, 'kanban.html', {'tasks': tasks})



import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Task, TaskStatus


@csrf_exempt  # You might need to remove this in production and use proper CSRF token handling
def update_task_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task_id = data.get('task_id')
        new_status = data.get('status')
        if new_status== "in-progress-column":
            new_status = "In Progress"
        elif new_status== "to-do-column":
            new_status = "To Do"
        else :
            new_status = "Completed"
        print(new_status)
        try:
            task = Task.objects.get(id=task_id)
            task.status = new_status
            task.save()
            return JsonResponse({'success': True, 'message': 'Task status updated.'})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Task not found.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@login_required
def veilleur_view(request):
    # Get tasks assigned to the logged-in user
    tasks = Task.objects.filter(assignments__user=request.user).prefetch_related('assignments__user')
    
    tasks_todo = tasks.filter(status='To Do')
    tasks_in_progress = tasks.filter(status='In Progress')
    tasks_completed = tasks.filter(status='Completed')

    return render(request, 'veilleur.html', {'tasks': tasks,'tasks_todo':tasks_todo,'tasks_in_progress':tasks_in_progress,'tasks_completed':tasks_completed})

from collections import defaultdict
from datetime import datetime, timedelta

# @login_required
# def analyste_view(request):
#     # Télécharger les ressources NLTK nécessaires
#     nltk.download('stopwords')
#     nltk.download('punkt')  # Assurez-vous que 'punkt' est téléchargé

#     # Définir des mots supplémentaires à exclure
#     extra_stopwords = {"etc", "could", "would", "also"}
#     all_stopwords = set(stopwords.words('english')).union(extra_stopwords)

#     # Charger les articles depuis la base de données
#     articles = SavedArticle.objects.all()

#     # Initialiser les structures pour analyser le contenu
#     cleaned_text = []
#     word_occurrences = {}
#     article_word_count = {}

#     for article_id, article in enumerate(articles):
#         text = article.content
#         # Nettoyage du texte : suppression des nombres et caractères spéciaux
#         text = re.sub(r'[^\w\s]', '', text)  # Supprimer la ponctuation
#         text = re.sub(r'\b\d+\b', '', text)  # Supprimer les nombres
#         tokens = word_tokenize(text.lower())  # Tokenisation en minuscules

#         # Filtrage des stopwords et des mots incomplets
#         filtered_tokens = [
#             word for word in tokens
#             if word not in all_stopwords and len(word) > 2 and word.isalpha()
#         ]

#         # Ajouter les mots au texte nettoyé global
#         cleaned_text.extend(filtered_tokens)

#         # Suivi des occurrences par article
#         for word in filtered_tokens:
#             if word not in word_occurrences:
#                 word_occurrences[word] = {}
#             if article_id not in word_occurrences[word]:
#                 word_occurrences[word][article_id] = 0
#             word_occurrences[word][article_id] += 1

#         # Compter les mots pour cet article
#         article_word_count[article_id] = filtered_tokens

#     # Génération du nuage de mots
#     final_text = " ".join(cleaned_text)
#     wordcloud = WordCloud(
#         width=800,
#         height=400,
#         background_color='white',
#         colormap='viridis',
#         max_words=100,
#     ).generate(final_text)

#     # Sauvegarder le nuage de mots comme image
#     wordcloud_file = "static/img/wordcloud.png"
#     wordcloud.to_file(wordcloud_file)

#     # Génération du graphique en barres pour les mots les plus fréquents
#     word_counts = Counter(cleaned_text)
#     most_common_words = word_counts.most_common(20)
#     words, counts = zip(*most_common_words)

#     # Sauvegarder le graphique en barres comme image
#     plt.figure(figsize=(12, 6))
#     plt.bar(words, counts, color='skyblue')
#     plt.xticks(rotation=45, ha='right', fontsize=12)
#     plt.title("Top 20 Most Frequent Words", fontsize=16)
#     plt.xlabel("Words", fontsize=14)
#     plt.ylabel("Frequency", fontsize=14)
#     plt.grid(axis='y', linestyle='--', alpha=0.7)
#     plt.tight_layout()
#     bar_chart_file = "static/img/bar_chart.png"
#     plt.savefig(bar_chart_file)
#     plt.close()

#     # Préparer les articles pour les mots les plus fréquents
#     frequent_words_data = []
#     for word, _ in most_common_words:
#         articles_for_word = sorted(word_occurrences[word].items(), key=lambda x: x[1], reverse=True)
#         word_articles = []
#         for article_id, count in articles_for_word:
#             article = articles[article_id]  # Get the entire article object
#             word_articles.append({'article': article, 'count': count})  # Store the full article object
#         frequent_words_data.append({'word': word, 'articles': word_articles})

#     # Passer les données au modèle HTML
#     context = {
#         'wordcloud_file': wordcloud_file,
#         'bar_chart_file': bar_chart_file,
#         'frequent_words_data': frequent_words_data,
#     }
#     return render(request, 'Analystekeywords.html', context)
import plotly.graph_objects as go
from collections import defaultdict

def create_bubble_chart(correlation_data):
    # Extraire tous les mots-clés uniques
    words = set()
    for entry in correlation_data:
        words.add(entry["word1"])
        words.add(entry["word2"])

    # Calculer la fréquence de chaque mot-clé
    word_freq = defaultdict(int)
    for entry in correlation_data:
        word_freq[entry["word1"]] += entry["count"]
        word_freq[entry["word2"]] += entry["count"]

    # Préparer les données pour le graphique en bulles
    bubble_trace = go.Scatter(
        x=[hash(word) % 100 for word in words],  # Position aléatoire sur l'axe X
        y=[hash(word) % 100 for word in words],  # Position aléatoire sur l'axe Y
        mode='markers+text',
        text=list(words),
        marker=dict(
            size=[word_freq[word] * 2 for word in words],  # Taille de la bulle basée sur la fréquence
            color='lightblue',  # Couleur des bulles
            sizemode='diameter'  # La taille est un diamètre
        ),
        hoverinfo='text'
    )

    # Créer la figure
    fig = go.Figure(data=[bubble_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        title="Graphique en Bulles des Mots-Clés"
                    ))
    return fig


import plotly.graph_objects as go
from collections import defaultdict

def create_network_graph(correlation_data):
    nodes = set()
    edges = []
    for entry in correlation_data:
        word1, word2, count = entry["word1"], entry["word2"], entry["count"]
        nodes.add(word1)
        nodes.add(word2)
        edges.append((word1, word2, count))

    # Créer les positions des nœuds
    node_positions = {node: (i, i) for i, node in enumerate(nodes)}

    # Créer les arêtes
    edge_trace = []
    for word1, word2, count in edges:
        x0, y0 = node_positions[word1]
        x1, y1 = node_positions[word2]
        edge_trace.append(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            line=dict(width=count / 10, color='#888'),  # Épaisseur basée sur la corrélation
            hoverinfo='none',
            mode='lines'
        ))

    # Créer les nœuds
    node_trace = go.Scatter(
        x=[node_positions[node][0] for node in nodes],
        y=[node_positions[node][1] for node in nodes],
        mode='markers+text',
        text=list(nodes),
        textposition="top center",
        marker=dict(size=20, color='lightblue'),
        hoverinfo='text'
    )

    # Créer la figure
    fig = go.Figure(data=edge_trace + [node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        title="Graphique en Réseau des Mots-Clés"
                    ))
    return fig


def create_arc_diagram(correlation_data):
    nodes = set()
    edges = []
    for entry in correlation_data:
        word1, word2, count = entry["word1"], entry["word2"], entry["count"]
        nodes.add(word1)
        nodes.add(word2)
        edges.append((word1, word2, count))

    # Créer les positions des nœuds
    node_positions = {node: i for i, node in enumerate(nodes)}

    # Créer les arcs
    arc_trace = []
    for word1, word2, count in edges:
        x0, x1 = node_positions[word1], node_positions[word2]
        arc_trace.append(go.Scatter(
            x=[x0, x1], y=[0, 0],
            mode='lines',
            line=dict(width=count / 10, color='#888'),  # Épaisseur basée sur la corrélation
            hoverinfo='none'
        ))

    # Créer les nœuds
    node_trace = go.Scatter(
        x=[node_positions[node] for node in nodes],
        y=[0] * len(nodes),
        mode='markers+text',
        text=list(nodes),
        textposition="top center",
        marker=dict(size=20, color='lightblue'),
        hoverinfo='text'
    )

    # Créer la figure
    fig = go.Figure(data=arc_trace + [node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        title="Graphique en Arc des Mots-Clés"
                    ))
    return fig


def create_correlation_matrix(correlation_data):
    words = sorted(set([entry["word1"] for entry in correlation_data] + [entry["word2"] for entry in correlation_data]))
    matrix = [[0] * len(words) for _ in range(len(words))]

    for entry in correlation_data:
        word1, word2, count = entry["word1"], entry["word2"], entry["count"]
        i, j = words.index(word1), words.index(word2)
        matrix[i][j] = count
        matrix[j][i] = count  # La matrice est symétrique

    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=words,
        y=words,
        colorscale='Viridis',
        hoverongaps=False
    ))
    return fig

from collections import defaultdict, Counter
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from django.shortcuts import render
from .models import SavedArticle  # Remplacez `yourapp` par le nom de votre application

def analyste_view(request):
    # Télécharger les ressources NLTK nécessaires
    nltk.download('stopwords')
    nltk.download('punkt')

    # Définir des mots supplémentaires à exclure
    extra_stopwords = {"etc", "could", "would", "also"}
    all_stopwords = set(stopwords.words('english')).union(extra_stopwords)

    # Charger les articles depuis la base de données
    articles = SavedArticle.objects.all()

    # Initialiser les structures pour analyser le contenu
    cleaned_text = []
    word_occurrences = {}
    co_occurrence = defaultdict(lambda: defaultdict(int))  # Matrice de co-occurrence

    for article_id, article in enumerate(articles):
        text = article.content
        # Nettoyage du texte : suppression des nombres et caractères spéciaux
        text = re.sub(r'[^\w\s]', '', text)  # Supprimer la ponctuation
        text = re.sub(r'\b\d+\b', '', text)  # Supprimer les nombres
        tokens = word_tokenize(text.lower())  # Tokenisation en minuscules

        # Filtrage des stopwords et des mots incomplets
        filtered_tokens = [
            word for word in tokens
            if word not in all_stopwords and len(word) > 2 and word.isalpha()
        ]

        # Ajouter les mots au texte nettoyé global
        cleaned_text.extend(filtered_tokens)

        # Suivi des occurrences par article
        for word in filtered_tokens:
            if word not in word_occurrences:
                word_occurrences[word] = {}
            if article_id not in word_occurrences[word]:
                word_occurrences[word][article_id] = 0
            word_occurrences[word][article_id] += 1

        # Mettre à jour la matrice de co-occurrence
        unique_words_in_article = set(filtered_tokens)  # Éviter les doublons dans le même article
        for word1 in unique_words_in_article:
            for word2 in unique_words_in_article:
                if word1 != word2:
                    co_occurrence[word1][word2] += 1

    # Génération du nuage de mots
    final_text = " ".join(cleaned_text)
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='viridis',
        max_words=100,
    ).generate(final_text)

    # Sauvegarder le nuage de mots comme image
    wordcloud_file = "static/img/wordcloud.png"
    wordcloud.to_file(wordcloud_file)

    # Génération du graphique en barres pour les mots les plus fréquents
    word_counts = Counter(cleaned_text)
    most_common_words = word_counts.most_common(20)
    words, counts = zip(*most_common_words)

    # Sauvegarder le graphique en barres comme image
    plt.figure(figsize=(12, 6))
    plt.bar(words, counts, color='skyblue')
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.title("Top 20 Most Frequent Words", fontsize=16)
    plt.xlabel("Words", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    bar_chart_file = "static/img/bar_chart.png"
    plt.savefig(bar_chart_file)
    plt.close()

    # Préparer les articles pour les mots les plus fréquents
    frequent_words_data = []
    for word, _ in most_common_words:
        articles_for_word = sorted(word_occurrences[word].items(), key=lambda x: x[1], reverse=True)
        word_articles = []
        for article_id, count in articles_for_word:
            article = articles[article_id]  # Get the entire article object
            word_articles.append({'article': article, 'count': count})  # Store the full article object
        frequent_words_data.append({'word': word, 'articles': word_articles})

    # Convertir most_common_words en dictionnaire
    most_common_words_dict = dict(most_common_words)

    # Préparer les données pour la corrélation
    correlation_data = []
    for word1, related_words in co_occurrence.items():
        for word2, count in related_words.items():
            if word1 in most_common_words_dict and word2 in most_common_words_dict:  # Limiter aux mots fréquents
                correlation_data.append({"word1": word1, "word2": word2, "count": count})

    # Créer tous les graphiques
    network_graph = create_network_graph(correlation_data)
    arc_diagram = create_arc_diagram(correlation_data)
    correlation_matrix = create_correlation_matrix(correlation_data)
    bubble_chart = create_bubble_chart(correlation_data)

    # Convertir les graphiques en HTML
    network_graph_html = network_graph.to_html(full_html=False)
    arc_diagram_html = arc_diagram.to_html(full_html=False)
    correlation_matrix_html = correlation_matrix.to_html(full_html=False)
    bubble_chart_html = bubble_chart.to_html(full_html=False)

    # Passer les données au modèle HTML
    context = {
        'wordcloud_file': wordcloud_file,
        'bar_chart_file': bar_chart_file,
        'frequent_words_data': frequent_words_data,
        'network_graph_html': network_graph_html,
        'arc_diagram_html': arc_diagram_html,
        'correlation_matrix_html': correlation_matrix_html,
        'bubble_chart_html': bubble_chart_html,
    }
    return render(request, 'Analystekeywords.html', context)


# >>>>>>> origin/main




# VEILLLEUR ----


import requests 
import xml.etree.ElementTree as ET
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from .forms import ArxivSearchForm,ScholarSearchForm,ScholarsemSearchForm,PLOSOneSearchForm  
from .models import SavedArticle, DeletedArticle
from scholarly import scholarly
import pdfplumber  
from bs4 import BeautifulSoup 

import requests 
import xml.etree.ElementTree as ET
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from .forms import ArxivSearchForm,ScholarSearchForm,ScholarsemSearchForm,PLOSOneSearchForm  
from .models import SavedArticle, DeletedArticle
from scholarly import scholarly
import pdfplumber  
from bs4 import BeautifulSoup 




@login_required
def fetch_arxiv_articles(request,task_id):
    task = get_object_or_404(Task, pk=task_id)
    articles = []
    form = ArxivSearchForm(request.GET or None)

    if form.is_valid():
        mot_cle = form.cleaned_data.get('mot_cle', '') or ''
        date_debut = form.cleaned_data.get('date_debut', None)
        date_fin = form.cleaned_data.get('date_fin', None)

        # 1) Vérifier si tout est vide (mot-cle et dates)
        if not mot_cle and not date_debut and not date_fin:
            # On ne lance pas la requête et on renvoie la page vide
            return render(request, 'articles.html', {'form': form, 'articles': articles})

        # 2) Construire la requête ArXiv
        #    Si mot_cle est vide, on peut mettre "all:" => potentiellement large.
        #    Sinon, on fait all:mot_cle
        if mot_cle:
            query_param = f"all:{mot_cle}"
        else:
            query_param = "all:"  # attention au volume potentiellement énorme

        url = f"http://export.arxiv.org/api/query?search_query={query_param}&start=0&max_results=20"

        # 3) Appeler l'API ArXiv avec un timeout
        try:
            response = requests.get(url, timeout=10)  # Timeout 10s
            response.raise_for_status()              # Lève une exception pour code 4xx/5xx
        except requests.exceptions.RequestException as e:
            return render(request, 'error.html', {
                'error_message': f"Erreur lors de la requête ArXiv : {str(e)}"
            })

        # 4) Si la requête est OK, parser la réponse XML
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.content)
            except ET.ParseError as pe:
                return render(request, 'error.html', {
                    'error_message': f"Impossible de parser la réponse XML : {str(pe)}"
                })

            # 5) Parcourir les entrées
            for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
                title_el = entry.find("{http://www.w3.org/2005/Atom}title")
                summary_el = entry.find("{http://www.w3.org/2005/Atom}summary")
                published_el = entry.find("{http://www.w3.org/2005/Atom}published")

                # Récupérer titre, résumé, date
                title = title_el.text if title_el is not None else "No Title"
                summary = summary_el.text if summary_el is not None else "No Summary"
                published = published_el.text if published_el is not None else ""

                # Convertir date en objet date
                try:
                    pub_date = datetime.strptime(published, "%Y-%m-%dT%H:%M:%S%z").date()
                except ValueError:
                    pub_date = None

                # Récupérer auteurs
                authors = []
                for author_el in entry.findall("{http://www.w3.org/2005/Atom}author"):
                    name_el = author_el.find("{http://www.w3.org/2005/Atom}name")
                    if name_el is not None:
                        authors.append(name_el.text)

                # Récupérer lien (version 'abs')
                link_el = entry.find("{http://www.w3.org/2005/Atom}link[@rel='alternate']")
                if link_el is not None and 'href' in link_el.attrib:
                    link = link_el.attrib['href']
                else:
                    link = "#"

                # PDF link (remplace 'abs' par 'pdf')
                pdf_link = link.replace("abs", "pdf")

                # 6) Vérifier si article est marqué 'Deleted'
                if DeletedArticle.objects.filter(link=link).exists():
                    continue

                # 7) Vérifier date_debut/date_fin si elles existent
                #    Si date_debut / date_fin n'existent pas, on ne filtre pas
                if (date_debut and date_fin and pub_date) and not (date_debut <= pub_date <= date_fin):
                    # Pub date hors intervalle => on ignore
                    continue

                # 8) Vérifier si déjà 'Saved'
                is_saved = SavedArticle.objects.filter(link=link).exists()

                # 9) Extraire le contenu PDF si la date est dans l'intervalle
                article_content = None
                try:
                    pdf_response = requests.get(pdf_link, timeout=10)
                    if pdf_response.status_code == 200:
                        # Sauvegarder temporairement le PDF
                        with open("temp.pdf", "wb") as f:
                            f.write(pdf_response.content)
                        # Extraire le texte
                        with pdfplumber.open("temp.pdf") as pdf:
                            article_content = "\n".join(
                                page.extract_text() or "" for page in pdf.pages
                            )
                except Exception as e:
                    article_content = f"Impossible d'extraire le contenu : {str(e)}"

                # 10) Ajouter l'article à la liste
                articles.append({
                    'title': title,
                    'summary': summary,
                    'authors': authors,
                    'link': link,
                    'published': pub_date,
                    'is_saved': is_saved,
                    'content': article_content,
                })
        else:
            return render(
                request, 
                'error.html', 
                {'error_message': f"Erreur lors de la requête. Statut : {response.status_code}"}
            )
    tasks = Task.objects.all()
    # 11) Renvoyer le template
    return render(request, 'articles.html', {
    'form': form,
    'articles': articles,
    'tasks': tasks,  # Ajout des tâches au contexte
    'task_id': task_id  # Add task_id to the context
     
      })



# views.py
# views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Task, SavedArticle
from django.views.decorators.csrf import csrf_exempt
import logging
# views.py

import logging
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Task, SavedArticle, DeletedArticle
from .forms import PLOSOneSearchForm, ArxivSearchForm
import requests
from bs4 import BeautifulSoup
import nltk
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# Configurez un logger
logger = logging.getLogger(__name__)

# Vue `save_article`
@csrf_exempt  # Pour le débogage seulement. Supprimez ceci en production et gérez correctement le CSRF.
def save_article(request, task_id):
    if request.method == 'POST':
        logger.debug(f"Received POST request to save_article for task_id={task_id}")
        try:
            task = get_object_or_404(Task, pk=task_id)
            logger.debug(f"Task found: {task}")

            title = request.POST.get('title')
            link = request.POST.get('link')
            content = request.POST.get('content')  
            summary = request.POST.get('summary')  
            authors = request.POST.get('authors') 

            logger.debug(f"Received data - Title: {title}, Link: {link}, Authors: {authors}")

            if not all([title, link, content, summary, authors]):
                logger.warning("Incomplete article data received.")
                return JsonResponse({'message': 'Données de l\'article incomplètes.'}, status=400)

            saved_article, created = SavedArticle.objects.get_or_create(
                link=link,
                defaults={
                    'title': title,
                    'content': content,
                    'summary': summary,
                    'author': authors,
                    'task': task
                }
            )

            if not created:
                logger.debug("Article already exists. Updating task.")
                saved_article.task = task
                saved_article.save()
                return JsonResponse({'message': 'Article mis à jour avec succès !'})
            
            logger.debug("Article created successfully.")
            return JsonResponse({'message': 'Article sauvegardé avec succès !'})
        
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de l'article: {e}")
            return JsonResponse({'message': 'Une erreur est survenue lors de la sauvegarde de l\'article.', 'error': str(e)}, status=500)
    
    logger.warning("Non-POST request received for save_article.")
    return JsonResponse({'message': 'Requête invalide'}, status=400)

# Vue `delete_article`
def delete_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        link = request.POST.get('link')

        if not all([title, link]):
            return JsonResponse({'message': 'Données insuffisantes pour supprimer l\'article.'}, status=400)

        # Marquer l'article comme supprimé
        DeletedArticle.objects.get_or_create(title=title, link=link)

        # Optionnel : Supprimer l'article de SavedArticle
        SavedArticle.objects.filter(title=title, link=link).delete()

        return JsonResponse({'message': 'Article deleted successfully!'})
    return JsonResponse({'message': 'Invalid request'}, status=400)

# Vue `fetch_plosone_articles`
@login_required
def fetch_plosone_articles(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    articles = []
    form = PLOSOneSearchForm(request.GET or None)

    if form.is_valid():
        mot_cle = form.cleaned_data['mot_cle'] or ''
        date_debut = form.cleaned_data['date_debut']
        date_fin = form.cleaned_data['date_fin']

        # 1) Si l'utilisateur n'a RIEN saisi (ni mot_cle ni dates), on n'appelle pas l'API
        if not mot_cle and not date_debut and not date_fin:
            # On renvoie juste la page (articles = [])
            return render(request, 'plosone_articles.html', {
                'form': form,
                'articles': articles,
                'tasks': Task.objects.all(),
                'task_id': task_id
            })

        # 2) Construire la requête Lucene pour l'API PLOS
        if date_debut and date_fin:
            # L'utilisateur a mis un intervalle de dates
            start_str = date_debut.strftime('%Y-%m-%dT00:00:00Z')
            end_str = date_fin.strftime('%Y-%m-%dT23:59:59Z')

            if mot_cle:
                # mot_cle + intervalle
                query = f"title:{mot_cle} AND publication_date:[{start_str} TO {end_str}]"
            else:
                # Pas de mot_cle => récupérer *tout* dans l'intervalle
                query = f"title:* AND publication_date:[{start_str} TO {end_str}]"
        else:
            # Pas de dates valides
            if mot_cle:
                # Recherche uniquement par mot_cle
                query = f"title:{mot_cle}"
            else:
                # Pas de mot_cle non plus => autoriser "tout" sans dates :
                query = "title:*"

        url = f"https://api.plos.org/search?q={query}&wt=json&rows=10"

        # 3) Appel API avec timeout et gestion d'erreur
        try:
            response = requests.get(url, timeout=10)  # Timeout de 10 secondes
            response.raise_for_status()               # Lève une exception si HTTP 4xx/5xx
        except requests.exceptions.RequestException as e:
            return render(request, 'error.html', {
                'error_message': f"Erreur lors de la requête à PLOS : {str(e)}"
            })

        # 4) Exploiter la réponse JSON
        data = response.json()
        docs = data.get('response', {}).get('docs', [])

        for doc in docs:
            link = f"https://journals.plos.org/plosone/article?id={doc.get('id')}"

            # Sauter les articles "Deleted"
            if DeletedArticle.objects.filter(link=link).exists():
                continue

            # Vérifier si déjà "Saved"
            is_saved = SavedArticle.objects.filter(link=link).exists()

            # Récupérer un éventuel texte d'intro
            content = ""
            try:
                article_page = requests.get(link, timeout=10)
                article_page.raise_for_status()
                soup = BeautifulSoup(article_page.content, 'html.parser')

                intro_section = soup.find('section', class_='intro')
                if not intro_section:
                    intro_section = soup.find('section', id='article-introduction')

                if intro_section:
                    content = intro_section.get_text(separator="\n", strip=True)
                else:
                    content = soup.get_text(separator="\n", strip=True)

            except requests.exceptions.RequestException as e:
                content = f"Erreur lors de la récupération du contenu : {str(e)}"

            # Ajouter l'article à la liste
            articles.append({
                'id': doc.get('id'),  # Assurez-vous d'avoir un champ 'id'
                'title': doc.get('title_display', 'No Title'),
                'authors': doc.get('author_display', []),
                'journal': doc.get('journal', 'Unknown Journal'),
                'link': link,
                'published': doc.get('publication_date', 'Unknown Date'),
                'summary': doc.get('abstract', 'No Abstract'),
                'content': content,
                'is_saved': is_saved,
            })

    # Récupérer toutes les tâches disponibles
    tasks = Task.objects.all()
    # 5) Renvoyer le template avec le formulaire et les articles trouvés
    return render(request, 'plosone_articles.html', {
        'form': form,
        'articles': articles,
        'task_id': task_id,
        'tasks': tasks
    })


from django.shortcuts import render
from .models import *

def fetch_content(request, task_id):
    if task_id:
        # Retrieve the task object and filter articles for the specific task
        task = Task.objects.get(id=task_id)  # Retrieve the task based on the task_id
        saved_articles = SavedArticle.objects.filter(task_id=task_id)
    else:
        saved_articles = SavedArticle.objects.all()
        task = None  # If no task_id, set task to None

    return render(request, 'fetch_content.html', {'saved_articles': saved_articles, 'task': task})   

def task_content(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Get or create a default category
    default_category, _ = Category.objects.get_or_create(
        name="Default Category",
        defaults={"description": "This is a default category."},
    )

    # Get or create a default source
    default_source, _ = Source.objects.get_or_create(
        name=f"Default Source for Task {task.id}",
        url=f"https://example.com/task/{task.id}",
        category=default_category,
        task=task,
        defaults={"description": f"Default source for task {task.id}"},
    )

    # Retrieve all saved articles associated with the task
    saved_articles = SavedArticle.objects.filter(task=task)

    # Add saved articles as contents
    for article in saved_articles:
        # Check if a Content object with the same URL already exists
        if not Content.objects.filter(url=article.link, task=task).exists():
            try:
                Content.objects.create(
                    title=article.title,
                    url=article.link,
                    summary=article.summary,
                    source=default_source,
                    task=task,
                    created_by=request.user if request.user.is_authenticated else None,
                )
            except IntegrityError:
                print(f"Duplicate content detected for URL: {article.link}")
        else:
            print(f"Content with URL {article.link} already exists.")

    return render(request, 'task_content.html', {'task': task, 'saved_articles': saved_articles})


from collections import Counter
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render
from .models import SavedArticle
from collections import Counter
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render
from .models import SavedArticle

def author_statistics(request):
    # Fetch all articles
    articles = SavedArticle.objects.all()

    # Collect authors and their articles
    author_count = Counter()
    author_articles = {}

    for article in articles:
        # Split authors by commas and strip whitespace
        authors = [author.strip() for author in article.author.split(',')]
        for author in authors:
            author_count[author] += 1
            if author not in author_articles:
                author_articles[author] = []
            author_articles[author].append(article)  # Store the full article object

    # Create a bar chart for the most repeated authors
    top_authors = author_count.most_common(10)  # Top 10 authors
    labels, values = zip(*top_authors) if top_authors else ([], [])

    # Plot the graph
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='skyblue')
    plt.title("Top 10 Most Repeated Authors")
    plt.xlabel("Authors")
    plt.ylabel("Occurrences")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the graph as a base64 string
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Prepare data for the table
    author_data = [
        {"author": author, "articles": articles, "count": author_count[author]}
        for author, articles in author_articles.items()
    ]

    context = {
        "image_base64": image_base64,
        "author_data": author_data,
    }
    return render(request, "analysteAuteur.html", context)


import csv
from django.http import HttpResponse
from collections import Counter
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from django.shortcuts import render
from .models import SavedArticle
from collections import Counter
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render
from .models import SavedArticle

def word_statistics(request):
    query = request.GET.get('query', '').strip()
    word_count = Counter()
    word_articles = {}

    if query:
        words = [word.strip().lower() for word in query.split()]
        articles = SavedArticle.objects.all()

        for article in articles:
            for word in words:
                # Compter les occurrences du mot dans le titre, le contenu et le résumé
                count = (
                    article.title.lower().count(word) +
                    article.content.lower().count(word) +
                    article.summary.lower().count(word)
                )
                if count > 0:
                    word_count[word] += count
                    if word not in word_articles:
                        word_articles[word] = []
                    # Stocker l'article et le nombre d'occurrences pour ce mot
                    word_articles[word].append({"article": article, "count": count})

        # Générer un graphique en barres pour les mots les plus fréquents
        if word_count:
            plt.figure(figsize=(10, 6))
            words, counts = zip(*word_count.most_common())  # Tous les mots ou les plus fréquents
            plt.bar(words, counts, color='skyblue')
            plt.title("Word Occurrences")
            plt.xlabel("Words")
            plt.ylabel("Occurrences")
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Sauvegarder le graphique en base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            plt.close()
        else:
            image_base64 = None
    else:
        image_base64 = None

    # Préparer les données pour le template
    word_data = [
        {"word": word, "articles": articles, "total_count": word_count[word]}
        for word, articles in word_articles.items()
    ]

    context = {
        "query": query,
        "word_data": word_data,
        "image_base64": image_base64,  # Ajouter l'image au contexte
    }
    return render(request, "analyseCustom.html", context)


# ---- GENERATION DE RAPPORT  ------



from django.shortcuts import render, redirect, get_object_or_404
from .models import SavedArticle, Rapport
from .forms import RapportForm
import google.generativeai as genai
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import time

# Configurer la clé API Gemini
genai.configure(api_key="GEMINI_API_KEY")

def summarize_text_with_gemini(content, max_retries=3, delay=2):
    for attempt in range(max_retries):
        try:
            if len(content) > 4000:
                content = content[:4000]
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(
                f"Résumez le contenu suivant en un paragraphe détaillé tout en conservant les détails importants : {content}"
            )
            summary = response.text.strip()
            return summary
        except Exception as e:
            print(f"Tentative {attempt + 1} échouée : {e}")
            time.sleep(delay)
    return "Erreur lors de la génération du résumé après plusieurs tentatives."

def extract_keywords(content):
    if not content.strip():
        return []
    vectorizer = CountVectorizer(max_features=10, stop_words='french')
    try:
        matrix = vectorizer.fit_transform([content])
        keywords = vectorizer.get_feature_names_out()
        counts = matrix.toarray().sum(axis=0)
        return list(zip(keywords, counts))
    except Exception as e:
        print(f"Erreur lors de l'extraction des mots-clés : {e}")
        return []
    
from wordcloud import WordCloud
def generate_wordcloud_image(text):
    
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

def generate_bar_chart_image(top_keywords):
    words, counts = zip(*top_keywords)
    plt.figure(figsize=(10, 5))
    plt.bar(words, counts, color='skyblue')
    plt.xlabel('Mots-Clés')
    plt.ylabel('Fréquence')
    plt.title('Mots-Clés les Plus Fréquents')
    plt.xticks(rotation=45)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

def generate_remarks_with_gemini(top_keywords, articles, global_summary, max_retries=3, delay=2):
    for attempt in range(max_retries):
        try:
            prompt = (
                "En tant qu'expert, donnez 3 à 5 remarques ou insights basés sur les informations suivantes :\n"
                f"Mots-clés fréquents : {', '.join([word for word, _ in top_keywords])}\n"
                f"Articles pertinents : {', '.join([article.title for article in articles])}\n"
                f"Résumé global : {global_summary}"
            )
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            remarks = response.text.strip()
            return remarks
        except Exception as e:
            print(f"Tentative {attempt + 1} échouée : {e}")
            time.sleep(delay)
    return "Erreur lors de la génération des remarques après plusieurs tentatives."

def rapport(request):
    # Récupérer tous les articles
    articles = SavedArticle.objects.all().order_by('-id')[:5]  # Par exemple, les 5 articles les plus récents

    # Extraire les mots-clés les plus fréquents
    all_content = " ".join([article.content for article in articles])
    keywords = extract_keywords(all_content)
    top_keywords = Counter(dict(keywords)).most_common(10) if keywords else []

    # Générer un résumé global pour tous les articles
    combined_content = " ".join([article.content for article in articles])
    global_summary = summarize_text_with_gemini(combined_content)

    # Générer des remarques avec Gemini
    remarks = generate_remarks_with_gemini(top_keywords, articles, global_summary)

    # Générer les graphiques
    wordcloud_image = generate_wordcloud_image(all_content) if all_content.strip() else None
    bar_chart_image = generate_bar_chart_image(top_keywords) if top_keywords else None

    # Préparer les données pour le template
    context = {
        'top_keywords': top_keywords,
        'articles': articles,
        'global_summary': global_summary,
        'remarks': remarks,
        'wordcloud_image': wordcloud_image,
        'bar_chart_image': bar_chart_image,
    }
    return render(request, 'rapport.html', context)




def liste_rapports(request):
    rapports = Rapport.objects.all().order_by('-date_creation')
    return render(request, 'liste_rapports.html', {'rapports': rapports})

def creer_rapport(request):
    if request.method == 'POST':
        form = RapportForm(request.POST)
        if form.is_valid():
            rapport = form.save()
            return redirect('detail_rapport', rapport_id=rapport.id)
    else:
        form = RapportForm()
    return render(request, 'creer_rapport.html', {'form': form})

def detail_rapport(request, rapport_id):
    rapport = get_object_or_404(Rapport, id=rapport_id)
    # Récupérer tous les articles
    articles = SavedArticle.objects.all().order_by('-id')[:5]  # Par exemple, les 5 articles les plus récents

    # Extraire les mots-clés les plus fréquents
    all_content = " ".join([article.content for article in articles])
    keywords = extract_keywords(all_content)
    top_keywords = Counter(dict(keywords)).most_common(10) if keywords else []

    # Générer un résumé global pour tous les articles
    combined_content = " ".join([article.content for article in articles])
    global_summary = summarize_text_with_gemini(combined_content)

    # Générer des remarques avec Gemini
    remarks = generate_remarks_with_gemini(top_keywords, articles, global_summary)

    # Générer les graphiques
    wordcloud_image = generate_wordcloud_image(all_content) if all_content.strip() else None
    bar_chart_image = generate_bar_chart_image(top_keywords) if top_keywords else None

    # Préparer les données pour le template
    context = {
        'rapport':rapport,
        'top_keywords': top_keywords,
        'articles': articles,
        'global_summary': global_summary,
        'remarks': remarks,
        'wordcloud_image': wordcloud_image,
        'bar_chart_image': bar_chart_image,
    }
    
    return render(request, 'rapport.html', context)



# def analyste_kanban_view(request):
#     # tasks = Task.objects.filter(assignmentsuser=request.user).prefetch_related('assignmentsuser')
#     tasks=Task.objects
#     tasks_todo = tasks.filter(status='To Do')
#     tasks_in_progress = tasks.filter(status='In Progress')
#     tasks_completed = tasks.filter(status='Completed')

#     return render(request, 'analyste.html', {'tasks': tasks,'tasks_todo':tasks_todo,'tasks_in_progress':tasks_in_progress,'tasks_completed':tasks_completed})


def analyste_kanban_view(request):
    # Récupérer les tâches assignées à l'utilisateur connecté
    tasks = Task.objects.all()  # Exécute une requête pour récupérer tous les objets Task
    tasks_todo = tasks.filter(status='To Do')
    tasks_in_progress = tasks.filter(status='In Progress')
    tasks_completed = tasks.filter(status='Completed')

    return render(request, 'analyste.html', {
        'tasks': tasks, 
        'tasks_todo': tasks_todo,
        'tasks_in_progress': tasks_in_progress,
        'tasks_completed': tasks_completed
    })



def task_saved_articles(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # Fetch all saved articles related to the task
    # saved_articles = SavedArticle.objects.filter(task=task)
    saved_articles = SavedArticle.objects

    return render(request, 'analysteArticles.html', {'task': task, 'saved_articles': saved_articles})





####  ---------- KAHINAAA



from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Note
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
from django.http import HttpResponse
import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY



def home(request):
    articles = SavedArticle.objects.all().order_by('-id')  # Trier par ID décroissant
    return render(request, 'home.html', {'articles': articles})



def article_detail(request, pk):
    article = get_object_or_404(SavedArticle, pk=pk)  # Assurez-vous d'utiliser le modèle `SavedArticle`
    return render(request, 'article_detail.html', {'article': article})



from django.shortcuts import render, get_object_or_404, redirect
from .models import SavedArticle, Note
from .forms import NoteForm

def select_article_for_note(request):
    articles = SavedArticle.objects.all()
    return render(request, 'select_article_for_note.html', {'articles': articles})


def create_note(request, article_id):
    article = get_object_or_404(SavedArticle, id=article_id)
    notes = Note.objects.filter(article=article)

    # Valeurs par défaut pour les lignes et colonnes
    rows = int(request.GET.get('rows', 3))  # Par défaut, 3 lignes
    columns = int(request.GET.get('columns', 3))  # Par défaut, 3 colonnes

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.article = article
            new_note.save()
            return redirect('create_note', article_id=article_id)
    else:
        form = NoteForm()

    return render(request, 'create_note.html', {
        'article': article,
        'notes': notes,
        'form': form,
        'rows': range(rows),  # Transmettre une plage pour les lignes
        'columns': range(columns),  # Transmettre une plage pour les colonnes
    })


def generate_table(request, article_id):
    article = get_object_or_404(SavedArticle, id=article_id)
    # Vérifier si une note existe, sinon en créer une
    note, created = Note.objects.get_or_create(article=article)

    if request.method == 'POST':
        if 'save_table' in request.POST:
            # Sauvegarde des données du tableau
            table_data = []
            rows = int(request.POST.get('rows', 0))
            columns = int(request.POST.get('columns', 0))
            for row in range(rows):
                row_data = []
                for col in range(columns):
                    cell_value = request.POST.get(f'cell_{row}_{col}', '')
                    row_data.append(cell_value)
                table_data.append(row_data)
            note.table_data = json.dumps(table_data)  # Sauvegarde des données du tableau en JSON
            note.save()
            return redirect('create_note', article_id=article.id)
        else:
            # Génération initiale du tableau
            rows = int(request.POST.get('rows', 0))
            columns = int(request.POST.get('columns', 0))
            table_data = [["" for _ in range(columns)] for _ in range(rows)]
            return render(request, 'generate_table.html', {
                'article': article,
                'rows': rows,
                'columns': columns,
                'table_data': table_data,
            })

    return render(request, 'generate_table.html', {'article': article})



def assistant_redirect(request):
    # Remplacez l'URL par celle de votre assistant virtuel
    return redirect('https://chat.openai.com/')



def article_notes(request, article_id):
    article = get_object_or_404(SavedArticle, id=article_id)
    notes = Note.objects.filter(article=article)

    # Convertir table_data de JSON en liste Python pour chaque note
    for note in notes:
        if note.table_data:
            try:
                note.table_data = json.loads(note.table_data)
            except json.JSONDecodeError:
                note.table_data = []  # Gérer le cas où JSON est invalide

    return render(request, 'article_notes.html', {
        'article': article,
        'notes': notes,
    })



import json
def generate_full_report(request):
    articles = SavedArticle.objects.all()
    notes = Note.objects.all()

    # Décodage des données du tableau
    for note in notes:
        if note.table_data:
            try:
                note.table_data = json.loads(note.table_data)
            except json.JSONDecodeError:
                note.table_data = []

    context = {
        'articles': articles,
        'notes': notes,
    }

    return render(request, 'rapport_global.html', context)

from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.core.files.base import ContentFile
from django.utils.timezone import now
from .models import SavedArticle, Note, GeneratedReport
import json


def generate_pdf(request):
    # Récupérer les articles et les notes
    articles = SavedArticle.objects.all()
    notes = Note.objects.all()

    # Traiter les données des tableaux
    for note in notes:
        if note.table_data:
            try:
                note.table_data = json.loads(note.table_data)
                if not isinstance(note.table_data, list):
                    note.table_data = []
            except json.JSONDecodeError:
                note.table_data = []

    # Créer le contexte pour le rendu HTML
    context = {
        'articles': articles,
        'notes': notes,
    }

    # Rendu du contenu HTML pour le PDF
    html = render_to_string('rapport_global.html', context)

    # Générer le PDF en mémoire
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapport_global.pdf"'

    pdf = pisa.CreatePDF(html, dest=response)
    if pdf.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)

    # Enregistrer le PDF dans la base de données
    pdf_content = ContentFile(response.content)
    report_title = f"Rapport_{now().strftime('%Y%m%d_%H%M%S')}"
    report = GeneratedReport(title=report_title)
    report.pdf_file.save(f"{report_title}.pdf", pdf_content)
    report.save()

    # Retourner le PDF comme réponse
    return response