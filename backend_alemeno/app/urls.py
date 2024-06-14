
from django.contrib import admin
from django.urls import include, path
from .views import home, urineStripAnalyzer

urlpatterns = [
    path('urineStrip/', urineStripAnalyzer, name='urineStrip'),
    path('', home, name='home')
]

