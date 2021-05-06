# -*- coding: utf-8 -*-
from django.urls import path
from src.apps.settings.views import SettingsView


urlpatterns = [
    path('api/settings', SettingsView.as_view()),
]
