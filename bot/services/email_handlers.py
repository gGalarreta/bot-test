# -*- coding: utf-8 -*-
from boto3 import client
from django.shortcuts import render

class SESMailer(object):
    aws_region = None
    aws_access_key_id = None
    aws_secret_access_key = None
    app = None
    _connection = None

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    @property
    def connection(self):
        if not self._connection:
            self._connection = self._connect()
        return self._connection

    def init_app(self, app):
        self.app = app
        self.aws_region = self.app.config.get('AWS_REGION') or 'us-east-1'
        self.aws_access_key_id = self.app.config.get('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = self.app.config.get(
            'AWS_SECRET_ACCESS_KEY',
        )

    def _connect(self):
        return client(
            service_name='ses',
            region_name=self.aws_region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )

    def send(self, to, subject, sender=None, cc=[], bcc=[], text='', html=''):
        try:
            response = self.connection.send_email(
                Source=sender,
                Destination={
                    'ToAddresses': to,
                    'CcAddresses': cc,
                    'BccAddresses': bcc,
                },
                Message={
                    'Subject': {
                        'Data': subject,
                        'Charset': 'UTF-8',
                    },
                    'Body': {
                        'Text': {
                            'Data': text,
                            'Charset': 'UTF-8',
                        },
                        'Html': {
                            'Data': html,
                        },
                    },
                },
            )
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return True
        except:
            return False

    def send_email(self, data, email, template, subject):
      args = {
          'to': email.replace(' ', '').split(','),
          'subject': subject,
          'html': render(template, data=data),
      }

      return self.send(**args)


