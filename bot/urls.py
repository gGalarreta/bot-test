# -*- coding: utf-8 -*-
from bot.views import MessageViewSet
from bot.views import WebViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'messages', MessageViewSet)
router.register(r'webview', WebViewSet)
urlpatterns = router.urls
