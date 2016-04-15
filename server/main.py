#!/usr/bin/env python
#
# Copyright CoderBot.org
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from os import path

import webapp2
import fixpath
import json
import logging

import model

# Import the helper functions
from identitytoolkit import gitkitclient

from base import BaseHandler, user_required, user_gtk_required

class SignupHandler(BaseHandler):

  def get(self):
    url_next = self.request.get("url_next") if self.request.get("url_next") else "/"
    user = None
    gtk_user = self.get_current_gtk_user()

    if model.User.get_by_email(gtk_user.email) == None:
      user = model.User()

    user.uid = gtk_user.user_id
    user.email = gtk_user.email
    user.avatar_url = gtk_user.photo_url
    user.put()
    self.redirect(url_next)

class MainHandler(BaseHandler):
  def get(self):
    template_values = {
      'main': 'index.html',
      'content': "user: " + self.get_current_user().email if self.get_current_user() else "not logged"
    }
    self.get_base(template_values)

app = webapp2.WSGIApplication([
    ('/signup', SignupHandler),
    ('/.*', MainHandler)
], debug=True)
