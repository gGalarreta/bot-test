from typing import Any, List, Optional
import bot.utils.messages as messages
from bot.utils.patterns import Handler, Singleton
from bot.helpers.facebook import FacebookHelper
from bot.models import EventMessage, FacebookTextMessage, FacebookTextMessageType, Message, Conversation
import datetime
import sys
import os

class FacebookGetStartedHandler(Handler):

    def is_valid(self, request: Any) -> bool:
        return isinstance(request, FacebookTextMessage) \
            and request.type is FacebookTextMessageType.QUICK_REPLY \
            and request.text == 'START'

    def perform(self, request: Any) -> None:
        conversation, created = Conversation.objects.get_or_create(
            sender_id=request.recipient_id,
            recipient_id=request.sender_id,
        )
        if FacebookHelper.send_message(request.sender_id, messages.GREETINGS_MESSAGE):
            buttons = self.build_buttons()
            FacebookHelper.send_buttons(request.sender_id, messages.QUESTION_TITLE, buttons)
            Message.objects.create(
                text=request.text,
                recipient_id=request.sender_id,
                sender_id=request.recipient_id
            )

    def build_buttons(self) -> List[Any]:
        post_backs = [
            {
                'payload': messages.OPTION1_PAYLOAD,
                'title': messages.OPTION1_TITLE,
            },
            {
                'payload': messages.OPTION2_PAYLOAD,
                'title': messages.OPTION2_TITLE,
            },
        ]
        buttons = []
        for post_back in post_backs:
            buttons.append(FacebookHelper.post_back_button(
                    post_back.get('title'),
                    post_back.get('payload')
                ))
        return buttons

class FacebookTextHandler(Handler):

    def is_valid(self, request: Any) -> bool:
        return isinstance(request, FacebookTextMessage) and request.type is FacebookTextMessageType.PLAIN_TEXT

    def perform(self, request: Any) -> None:
        if FacebookHelper.send_message(request.sender_id, messages.DEFAULT_MESSAGE):
            Message.objects.create(
                text=request.text,
                recipient_id=request.sender_id,
                sender_id=request.recipient_id
            )

class FacebookOption1Handler(Handler):

    def is_valid(self, request: Any) -> bool:
        return isinstance(request, FacebookTextMessage) \
            and request.type is FacebookTextMessageType.QUICK_REPLY \
            and request.text == messages.OPTION1_PAYLOAD

    def perform(self, request: Any) -> bool:
        if FacebookHelper.send_message(request.sender_id, messages.OPTION1_MESSAGE):
            buttons = self.build_buttons()
            FacebookHelper.send_buttons(request.sender_id, messages.QUESTION_TITLE, buttons)
            Message.objects.create(
                text=request.text,
                recipient_id=request.sender_id,
                sender_id=request.recipient_id
            )

    def build_buttons(self) -> List[Any]:
        post_backs = [
            {
                'payload': messages.LIST_PAYLOAD,
                'title': messages.LIST_TITLE,
            },
            {
                'payload': messages.CARROUSEL_PAYLOAD,
                'title': messages.CARROUSEL_TITLE,
            },
        ]
        buttons = []
        for post_back in post_backs:
            buttons.append(FacebookHelper.post_back_button(
                    post_back.get('title'),
                    post_back.get('payload')
                ))
        return buttons

class FacebookOption2Handler(Handler):

    def is_valid(self, request: Any) -> bool:
        return isinstance(request, FacebookTextMessage) \
            and request.type is FacebookTextMessageType.QUICK_REPLY \
            and request.text == messages.OPTION2_PAYLOAD

    def perform(self, request: Any) -> bool:
        if FacebookHelper.send_message(request.sender_id, messages.OPTION2_MESSAGE):
            buttons = self.build_buttons()
            FacebookHelper.send_buttons(request.sender_id, messages.QUESTION_TITLE, buttons)
            Message.objects.create(
                text=request.text,
                recipient_id=request.sender_id,
                sender_id=request.recipient_id
            )

    def build_buttons(self) -> List[Any]:
        buttons = [
            {
                'type': 'postback',
                'payload': messages.VIDEO_PAYLOAD,
                'title': messages.VIDEO_TITLE,
            },
            {
                'type': 'web_url',
                'url': os.getenv('SERVER_URL') + '/api/v1/webview/options/',
                'webview_height_ratio': 'full',
                'title': messages.MEDIA_TITLE,
            },
        ]
        return buttons

class FacebookListHandler(Handler):
    def is_valid(self, request: Any) -> bool:
        return isinstance(request, FacebookTextMessage) \
            and request.type is FacebookTextMessageType.QUICK_REPLY \
            and request.text == messages.LIST_PAYLOAD

    def perform(self, request: Any) -> bool:
        if FacebookHelper.send_message(request.sender_id, messages.LIST_MESSAGE):
            data = [{'title': 'Titulo 1', 'subtitle': 'Subtitulo 1'},{'title': 'Titulo 1', 'subtitle': 'Subtitulo 1'}]
            elements = self.build_elements(data)
            FacebookHelper.send_list(request.sender_id, elements)
            Message.objects.create(
                text=request.text,
                recipient_id=request.sender_id,
                sender_id=request.recipient_id
            )            

    def build_elements(self, data) -> List[Any]:
        elements = []
        for element in data :
            content = {
                'title': element['title'],
                'subtitle': element['subtitle'],
            }
            elements.append(content)
        return elements

class FacebookCarrouselHandler(Handler):
    def is_valid(self, request: Any) -> bool:
        return isinstance(request, FacebookTextMessage) \
            and request.type is FacebookTextMessageType.QUICK_REPLY \
            and request.text == messages.CARROUSEL_PAYLOAD

    def perform(self, request: Any) -> bool:
        if FacebookHelper.send_message(request.sender_id, messages.CARROUSEL_MESSAGE):
            data = [{'title': 'Titulo 1', 'subtitle': 'Subtitulo 1'},{'title': 'Titulo 1', 'subtitle': 'Subtitulo 1'}]
            elements = self.build_elements(data)
            FacebookHelper.send_carrousel(request.sender_id, elements)
            Message.objects.create(
                text=request.text,
                recipient_id=request.sender_id,
                sender_id=request.recipient_id
            )

    def build_elements(self, data) -> List[Any]:
        elements = []
        for element in data :
            content = {
                'title': element['title'],
                'subtitle': element['subtitle'],
            }
            elements.append(content)
        return elements          

class FacebookVideoHanlder(Handler):
    def is_valid(self, request: Any) -> bool:
        return isinstance(request, FacebookTextMessage) \
            and request.type is FacebookTextMessageType.QUICK_REPLY \
            and request.text == messages.VIDEO_PAYLOAD

    def perform(self, request: Any) -> bool:
        if FacebookHelper.send_message(request.sender_id, messages.VIDEO_MESSAGE):
            elements = [{'media_type': 'video', 'url': 'https://www.facebook.com/Blasfemiiaz/videos/226357831471925/'}]
            FacebookHelper.send_video(request.sender_id, elements)
            Message.objects.create(
                text=request.text,
                recipient_id=request.sender_id,
                sender_id=request.recipient_id
            )

class MessageHandlerManager(metaclass=Singleton):

    def __init__(self):
        default_handler = FacebookTextHandler()
        option1_handler = FacebookOption1Handler(default_handler)
        option2_handler = FacebookOption2Handler(option1_handler)
        list_handler = FacebookListHandler(option2_handler)
        carrousel_handler = FacebookCarrouselHandler(list_handler)
        video_handler = FacebookVideoHanlder(carrousel_handler)
        self.base_handler = FacebookGetStartedHandler(video_handler)

