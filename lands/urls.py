from django.urls import path

from lands.views import about_us, index, privacy_policy

# Define URL patterns for the Django project.
urlpatterns = [
    # Pattern for the root URL (Homepage)
    path('', index, name='index'),
    # Pattern for the 'about' page URL
    path('about-us/', about_us, name='about_us'),
    # Pattern for the 'privacy' page URL
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
]
