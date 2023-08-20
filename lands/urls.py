from django.urls import path

from lands.views import index, result_page, about_us, privacy_policy

# Define URL patterns for the Django project.
urlpatterns = [
    # Pattern for the root URL (Homepage)
    path('', index, name='index'),
    # Pattern for the 'result_page' page URL
    path('result-page/', result_page, name='result_page'),
    # Pattern for the 'about' page URL
    path('about-us/', about_us, name='about_us'),
    # Pattern for the 'privacy' page URL
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
]
