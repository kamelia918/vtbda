from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name



class TaskStatus(models.TextChoices):
    TODO = 'To Do', 'To Do'
    IN_PROGRESS = 'In Progress', 'In Progress'
    COMPLETED = 'Completed', 'Completed'

class TaskPriority(models.TextChoices):
    LOW = 'Low', 'Low Priority'
    MEDIUM = 'Medium', 'Medium Priority'
    HIGH = 'High', 'High Priority'
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    priority = models.CharField(
        max_length=50,
        choices=TaskPriority.choices,
        default=TaskPriority.MEDIUM,
    )
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.TODO,
    )

    def __str__(self):
        return self.title
    
class Source(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(unique=True)
    category = models.ForeignKey(Category, related_name="sources", on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name="sources", on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Content(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(unique=True)
    summary = models.TextField(blank=True, null=True)
    source = models.ForeignKey(Source, related_name="contents", on_delete=models.CASCADE)
    date_fetched = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="contents", on_delete=models.SET_NULL, null=True, blank=True)
    task = models.ForeignKey(Task, related_name="contents", on_delete=models.CASCADE, null=True, blank=True)  # Ajout de la clé étrangère vers Task

    def __str__(self):
        return self.title



# class SavedArticle(models.Model):
#     title = models.CharField(max_length=500)
#     link = models.URLField(unique=True)
#     content = models.TextField(default="No content available.")
#     summary = models.TextField(default="No content available.")
#     author = models.TextField(default="No author available.")  # Updated default

   

#     def __str__(self):
#         return self.title



class SavedArticle(models.Model):
    title = models.CharField(max_length=500)
    link = models.URLField(unique=True)
    content = models.TextField(default="No content available.")
    summary = models.TextField(default="No content available.")
    author = models.TextField(default="No author available.")  # Updated default
    task = models.ForeignKey(Task, related_name='saved_articles', on_delete=models.CASCADE,null=True)

   

    def __str__(self):
        return self.title



class DeletedArticle(models.Model):
    title = models.CharField(max_length=500)
    link = models.URLField(unique=True)

    def __str__(self):
        return self.title






class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, related_name="assignments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="assignments", on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} assigned to {self.task}"

class Report(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="reports", on_delete=models.CASCADE)
    related_task = models.ForeignKey(Task, related_name="reports", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title



class Rapport(models.Model):
    titre = models.CharField(max_length=200)
    date_creation = models.DateTimeField(auto_now_add=True)
    top_keywords = models.JSONField(default=list)  # Pour stocker les mots-clés
    articles = models.JSONField(default=list)  # Pour stocker les articles
    global_summary = models.TextField(blank=True)  # Pour stocker le résumé global
    remarks = models.JSONField(default=list)  # Pour stocker les remarques
    wordcloud_image = models.TextField(blank=True)  # Pour stocker l'image du nuage de mots
    bar_chart_image = models.TextField(blank=True)  # Pour stocker l'image du graphique en barres

    def __str__(self):
        return self.titre
    

class Article(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    content = models.TextField(blank=True)
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Note(models.Model):
    article = models.ForeignKey(
        'SavedArticle', 
        on_delete=models.CASCADE, 
        related_name='notes'
    )
    remarks = models.TextField(
        null=True, 
        blank=True, 
        help_text="Remarques ou observations supplémentaires"
    )
    analysis = models.TextField(
        null=True, 
        blank=True, 
        help_text="Résumé de l'analyse générale"
    )
    table_data = models.TextField(
        null=True, 
        blank=True, 
        help_text="Données du tableau remplies par l'utilisateur"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def str(self):
        return f"Note for {self.article.title} - {self.created_at}"


class GeneratedReport(models.Model):
    title = models.CharField(max_length=255, default="Rapport Global")
    generated_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='generated_reports/', null=True, blank=True)

    def str(self):
        return f"{self.title} - {self.generated_at}"