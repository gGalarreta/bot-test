import facebook
import os
import sys

class FacebookGraph():

  def __init__(self):
    self.graph = facebook.GraphAPI(access_token=os.getenv('BOT_APP_TOKEN'), version=os.getenv('GRAPH_VERSION'))

  def get_user_name(self, sender_id, field):
    user = self.graph.get_object(id=sender_id, fields=field)
    return user[field]
