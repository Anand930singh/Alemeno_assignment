from django.contrib import admin
from django.urls import include, path
from .views import urineStripAnalyzer

urlpatterns = [
    path('urineStrip/', urineStripAnalyzer, name='urineStrip'),
]

