# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Case, When, Value, BooleanField

from src.apps.settings.models import Topic
from src.apps.settings.serializers import TopicSerializer


class SettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = Topic.objects.annotate(
            checked=Case(
                When(users=request.user, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        ).order_by('name')
        serializer = TopicSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        for data in request.data:
            topic = Topic.objects.get(pk=data['id'])
            if data['checked']:
                topic.users.add(request.user)
            else:
                topic.users.remove(request.user)
        return Response()
