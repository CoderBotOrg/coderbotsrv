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
import os
import webapp2
import fixpath
import logging

from google.appengine.api import mail

# Import the helper functions
from identitytoolkit import gitkitclient

from base import BaseHandler

# Import the configuration file you downloaded from Google Developer Console
server_config_json = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'gitkit-server-config.json')
gitkit_instance = gitkitclient.GitkitClient.FromConfigFile(server_config_json)

class LoginHandler(BaseHandler):
  def get(self):
    if self.get_current_gtk_user():
      logging.info("gtk_user: " + str(self.get_current_gtk_user().ToRequest()))
    logging.info("user: " +str(self.get_current_user()))
    template_values = {
      'main': 'signin_widget.html'
    }
    self.get_base(template_values)

class LoginCallbackHandler(BaseHandler):
  def get(self):
    logging.info("logged in.1")
    url_next = self.request.get("url_next") if self.request.get("url_next") else "/"
    # Check for and read the Google Identity Toolkit token if present
    if self.get_current_gtk_user() and self.get_current_user() is None:
      logging.info("logged in.2")
      self.redirect("/signup?url_next=" + url_next)
      return

    self.redirect(url_next)

class LogoutHandler(BaseHandler):
  def get(self):
    del self.session["user"]
    del self.session["gitkit_user"]
    self.redirect("/")

class SendmailHandler(BaseHandler):
  def post(self):
    logging.info("HTTP_CLIENT_IP: " + str(self.request.remote_addr))
    resp = gitkit_instance.GetOobResult(self.request.POST, self.request.remote_addr, self.request.cookies.get('gtoken'))

    sender = "CoderBot [no-reply] <info@coderbot.org>"
    message = mail.EmailMessage()
    message.sender = sender
    logging.info("resp: " + str(resp) + " new_email: " + str(resp.get("new_email")) + " old email: " + str(resp.get("email")))
    message.to = resp.get("new_email") if resp.get("new_email") else resp.get("email")
    action = None
    if resp.get("action") == gitkitclient.GitkitClient.RESET_PASSWORD_ACTION:
      action = "Reset password"
    elif resp.get("action") == gitkitclient.GitkitClient.CHANGE_EMAIL_ACTION:
      action = "Change email"
    
    message.subject = "CoderBot " + action
    message.body = """Message from CoderBot.org.
    You requested a """  + action + """.

    Plese click on the following link: """ + str(resp["oob_link"])
    
    message.send()

    self.response.write(resp.get("response_body"))
 
app = webapp2.WSGIApplication([
    ('/auth/login', LoginHandler),
    ('/auth/callback', LoginCallbackHandler),
    ('/auth/logout', LogoutHandler),
    ('/auth/sendmail', SendmailHandler)
], debug=True)
