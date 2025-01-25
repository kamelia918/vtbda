from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Category, Source, Content, Task, TaskAssignment, Report,SavedArticle , GeneratedReport

# Custom Restricted Admin Site
class RestrictedAdminSite(admin.AdminSite):
    def has_permission(self, request):
        # Limit access to superusers only
        return request.user.is_superuser

restricted_admin_site = RestrictedAdminSite(name="restricted_admin")

# Admin Configurations
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'category', 'description')
    list_filter = ('category',)
    search_fields = ('name', 'url')
    ordering = ('name',)

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'source', 'date_fetched', 'created_by')
    list_filter = ('source', 'date_fetched')
    search_fields = ('title', 'url')
    ordering = ('-date_fetched',)

class TaskAssignmentInline(admin.TabularInline):
    model = TaskAssignment
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'status')
    list_filter = ('status', 'due_date')
    search_fields = ('title',)
    ordering = ('due_date',)
    inlines = [TaskAssignmentInline]

# @admin.register(TaskAssignment)
class TaskAssignmentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'assigned_at')
    list_filter = ('assigned_at',)
    search_fields = ('task__title', 'user__username')
    ordering = ('-assigned_at',)



@admin.register(SavedArticle)
class SavedArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'content', 'summary')
    

class NoteAdmin(admin.ModelAdmin):
    list_display = ('article', 'remarks', 'analysis', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('article__title', 'remarks', 'analysis')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('article', 'remarks', 'analysis', 'table_data')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(GeneratedReport)
class GeneratedReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'generated_at', 'pdf_file')
    readonly_fields = ('generated_at',)


# Register models to Restricted Admin Site
restricted_admin_site.register(Content, ContentAdmin)
restricted_admin_site.register(Source, SourceAdmin)
restricted_admin_site.register(Task, TaskAdmin)

restricted_admin_site.register(Category, CategoryAdmin)
restricted_admin_site.register(SavedArticle, SavedArticleAdmin)
