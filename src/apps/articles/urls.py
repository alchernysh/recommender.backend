# -*- coding: utf-8 -*-
from django.urls import path
from src.apps.articles.views import ArticlesView


urlpatterns = [
    path('api/articles', ArticlesView.as_view()),
]
