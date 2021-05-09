# -*- coding: utf-8 -*-
from datetime import datetime

import numpy as np
from scipy import spatial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from src.apps.articles.models import Article
from src.apps.settings.models import Topic
from src.apps.articles.serializers import ArticleSerializer


class ArticlesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        day_articles = Article.objects.filter(
            timestamp__date=datetime.utcnow().date()
        ).order_by('timestamp')
        topics_embs = Topic.objects.filter(users=request.user).values_list('embedding', flat=True)
        relevant_articles = list()
        for article in day_articles:
            sim = max(1 - spatial.distance.cosine(article.embedding, topics_emb) for topics_emb in topics_embs)
            if sim > 0.6:
                relevant_articles.append(article)
        serializer = ArticleSerializer(relevant_articles, many=True)
        print(len(serializer.data))
        return Response(serializer.data)
