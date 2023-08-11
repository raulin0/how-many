from django.urls import path

from lands.views import about, index, privacy

# Define URL patterns for the Django project.
urlpatterns = [
    # Pattern for the root URL (Homepage)
    path('', index, name='index'),
    # Pattern for the 'about' page URL
    path('about/', about, name='about'),
    # Pattern for the 'privacy' page URL
    path('privacy/', privacy, name='privacy'),
]
