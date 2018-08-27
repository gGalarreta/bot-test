from typing import Dict, List
from django.conf import settings
import requests
import sys

class FacebookHelper(object):

    @staticmethod
    def send_message(recipient_id: str, message: str) -> bool:
        params = {
            'access_token': settings.BOT_APP_TOKEN
        }

        data = {
            'recipient': {
                'id': recipient_id
            },
            'message': {'text': message},
        }

        r = requests.post(settings.FACEBOOK_GRAPH_URL + '/messages', params=params, json=data)
        return r.status_code == 200

    @staticmethod
    def post_back_button(title, payload) -> Dict[str,str]:
        return {
            'type': 'postback',
            'title': title,
            'payload': payload
        }

    @staticmethod
    def call_button(title, phone_number) -> Dict[str,str]:
        return {
            'type': 'phone_number',
            'title': title,
            'payload': phone_number
        }

    @staticmethod
    def send_buttons(recipient_id: str, message: str, buttons: List[Dict[str,str]]) -> bool:
        params = {
            'access_token': settings.BOT_APP_TOKEN
        }

        data = {
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'button',
                        'text': message,
                        'buttons': buttons,
                    }
                }
            }
        }
        r = requests.post(settings.FACEBOOK_GRAPH_URL + '/messages', params=params, json=data)
        return r.status_code == 200

    @staticmethod
    def send_list(recipient_id: str, elements: List[Dict[str, str]]) -> bool:
        params ={
            'access_token': settings.BOT_APP_TOKEN
        }
        data = {
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'list',
                        'top_element_style': 'compact',
                        'elements': elements,
                    }
                }
            }            
        }
        r = requests.post(settings.FACEBOOK_GRAPH_URL + '/messages', params=params, json=data)
        return r.status_code == 200

    @staticmethod
    def send_carrousel(recipient_id: str, elements: List[Dict[str, str]]) -> bool:
        params ={
            'access_token': settings.BOT_APP_TOKEN
        }
        data = {
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'generic',
                        'elements': elements,
                    }
                }
            }            
        }
        r = requests.post(settings.FACEBOOK_GRAPH_URL + '/messages', params=params, json=data)
        return r.status_code == 200

    @staticmethod
    def send_video(recipient_id: str, elements: List[Dict[str,str]]) -> bool:
        params = {
            'access_token': settings.BOT_APP_TOKEN
        }
        data = {
            'recipient':{
                'id': recipient_id
            },
            'message': {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'media',
                        'elements': elements,
                    }
                }
            }
        }
        r = requests.post(settings.FACEBOOK_GRAPH_URL + '/messages', params=params, json=data)
        return r.status_code == 200
        
    @staticmethod
    def send_is_typing(recipient_id: str) -> bool:
        params = {
            'access_token': settings.BOT_APP_TOKEN
        }

        data = {
            'recipient': {
                'id': recipient_id
            },
            'sender_action': 'typing_on',
        }
        r = requests.post(settings.FACEBOOK_GRAPH_URL + '/messages', params=params, json=data)
        return r.status_code == 200
