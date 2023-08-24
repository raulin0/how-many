from django.urls import path

from decklist_analyzer.views import index

# Define URL patterns for the Django project.
urlpatterns = [
    # Pattern for the root URL (Homepage)
    path('', index, name='index'),
]
