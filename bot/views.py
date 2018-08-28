# -*- coding: utf-8 -*-
from bot.models import Message, Conversation
from bot.serializers import MessageSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
from django.http import HttpResponse
from rest_framework import status
from django.conf import settings
from django.db.models import Count
from .factories.facebook_factories import MessageFactory
from .helpers.facebook import FacebookHelper
from .services.message_handlers import MessageHandlerManager
import json
import requests
import asyncio
import time
import sys
from django.template.loader import get_template
from django.shortcuts import render


loop = asyncio.get_event_loop_policy().new_event_loop()

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @list_route(methods=['post', 'get'])
    def webhook(self, request):
        try:
            if request.method == 'POST':
                for entry in request.data.get('entry'):
                    for message_event in entry.get('messaging', []):
                      message = MessageFactory().make(message_event)
                      if message:
                        FacebookHelper.send_is_typing(message.sender_id)
                        loop.run_in_executor(None, MessageHandlerManager().base_handler.handle_request, message)
                return Response(status=status.HTTP_200_OK)
            return HttpResponse(request.GET['hub.challenge'], content_type='text/plain')
        except Exception as e:
            raise e


class WebViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @list_route(methods=['get'])
    def options(self, request):
        data_list = []
        t = get_template('option.html')
        options_to_display = ['opcion 1', 'opcion 2']
        html = t.render({'dropdown_data': options_to_display, 'data_list': data_list})
        return HttpResponse(html)

    @list_route(methods=['get'])
    def generate(self, request):
        data_list = []
        if request.GET.get('data') == 'opcion 2':
            data_list = ['opcion 2']
        else :
            data_list = ['opcion 1']
        template = 'section.html'
        context = {'data_list': data_list}
        return render(request, template, context)



