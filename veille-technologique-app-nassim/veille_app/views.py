
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


def task_content(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # Fetch all content related to the task's source
    contents = Content.objects.filter(source__task=task)
    return render(request, 'task_content.html', {'task': task, 'contents': contents})
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




def fetch_arxiv_articles(request):
    articles = []  
    form = ArxivSearchForm(request.GET or None)  

    if form.is_valid():
        mot_cle = form.cleaned_data['mot_cle']
        date_debut = form.cleaned_data['date_debut']
        date_fin = form.cleaned_data['date_fin']

        
        url = f"http://export.arxiv.org/api/query?search_query=all:{mot_cle}&start=0&max_results=10"
        response = requests.get(url)

        if response.status_code == 200:
            root = ET.fromstring(response.content)

            for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
                title = entry.find("{http://www.w3.org/2005/Atom}title").text
                summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
                authors = [author.find("{http://www.w3.org/2005/Atom}name").text for author in entry.findall("{http://www.w3.org/2005/Atom}author")]
                link = entry.find("{http://www.w3.org/2005/Atom}link[@rel='alternate']").attrib['href']
                pdf_link = f"{link.replace('abs', 'pdf')}"

                published = entry.find("{http://www.w3.org/2005/Atom}published").text
                pub_date = datetime.strptime(published, "%Y-%m-%dT%H:%M:%S%z").date()

                if not DeletedArticle.objects.filter(link=link).exists():
                    is_saved = SavedArticle.objects.filter(link=link).exists()
                    if date_debut <= pub_date <= date_fin:
                        article_content = None
                        try:
                            # Télécharger et extraire le contenu du PDF
                            pdf_response = requests.get(pdf_link)
                            if pdf_response.status_code == 200:
                                with open("temp.pdf", "wb") as f:
                                    f.write(pdf_response.content)
                                with pdfplumber.open("temp.pdf") as pdf:
                                    article_content = "\n".join(page.extract_text() for page in pdf.pages)
                        except Exception as e:
                            article_content = f"Impossible d'extraire le contenu : {e}"

                        articles.append({
                            'title': title,
                            'summary': summary,
                            'authors': authors,
                            'link': link,
                            'published': pub_date,
                            'is_saved': is_saved,
                            'content': article_content
                        })
        else:
            return render(request, 'error.html', {'error_message': f"Erreur lors de la requête. Statut : {response.status_code}"})

    return render(request, 'articles.html', {'form': form, 'articles': articles})


def save_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        link = request.POST.get('link')
        content = request.POST.get('content')  
        summary = request.POST.get('summary')  
        authors = request.POST.get('authors') 

       
        SavedArticle.objects.get_or_create(
            title=title,
            link=link,
            content=content, 
            summary=summary,
            author=authors,
          
        )

        return JsonResponse({'message': 'Article saved successfully!'})
    return JsonResponse({'message': 'Invalid request'}, status=400)



def delete_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        link = request.POST.get('link')

       
        DeletedArticle.objects.get_or_create(title=title, link=link)

        return JsonResponse({'message': 'Article deleted successfully!'})
    return JsonResponse({'message': 'Invalid request'}, status=400)



def fetch_plosone_articles(request):
    articles = [] 
    form = PLOSOneSearchForm(request.GET or None)  # Initialiser le formulaire

    if form.is_valid():
        mot_cle = form.cleaned_data['mot_cle']
        url = f"https://api.plos.org/search?q=title:{mot_cle}&wt=json&rows=10"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            docs = data.get('response', {}).get('docs', [])

            for doc in docs:
                link = f"https://journals.plos.org/plosone/article?id={doc.get('id')}"

                
                if DeletedArticle.objects.filter(link=link).exists():
                    continue

                
                is_saved = SavedArticle.objects.filter(link=link).exists()

                
                content = ''
                try:
                    article_page = requests.get(link)
                    if article_page.status_code == 200:
                        soup = BeautifulSoup(article_page.content, 'html.parser')

                        
                        introduction_section = soup.find('section', {'class': 'intro'})
                        
                        if not introduction_section:
                            
                            introduction_section = soup.find('section', {'id': 'article-introduction'})
                            
                        if introduction_section:
                            
                            content = introduction_section.get_text(separator="\n", strip=True)
                        else:
                           
                            content = soup.get_text(separator="\n", strip=True)
                            
                except requests.exceptions.RequestException as e:
                    content = f"Erreur lors de la récupération du contenu : {str(e)}"

                
                articles.append({
                    'title': doc.get('title_display', 'No Title'),
                    'authors': doc.get('author_display', []),
                    'journal': doc.get('journal', 'Unknown Journal'),
                    'link': link,
                    'published': doc.get('publication_date', 'Unknown Date'),
                    'summary': doc.get('abstract', 'No Abstract'),
                    'content': content, 
                    'is_saved': is_saved, 
                })
        else:
            return render(request, 'error.html', {'error_message': f"Erreur lors de la requête. Statut : {response.status_code}"})

    return render(request, 'plosone_articles.html', {'form': form, 'articles': articles})




from collections import Counter
from django.db.models import F
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



def analyste_kanban_view(request):
    # tasks = Task.objects.filter(assignmentsuser=request.user).prefetch_related('assignmentsuser')
    tasks=Task.objects
    tasks_todo = tasks.filter(status='To Do')
    tasks_in_progress = tasks.filter(status='In Progress')
    tasks_completed = tasks.filter(status='Completed')

    return render(request, 'analyste.html', {'tasks': tasks,'tasks_todo':tasks_todo,'tasks_in_progress':tasks_in_progress,'tasks_completed':tasks_completed})