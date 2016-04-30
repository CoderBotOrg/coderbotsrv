#!/usr/bin/env /tethon
#
# Copyright 2015 CoderBot org
# Authors: R.Previtera
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

import cgi
import os, logging, json
from datetime import date, datetime, time, timedelta
import wsgiref.handlers
import fixpath

from google.appengine.ext.ndb import model, toplevel
from google.appengine.api import users


import webapp2 as webapp
import traceback
#from webapp2_extras import jinja2
import jinja2
from webapp2_extras import sessions
from google.appengine.api import memcache
from webapp2_extras import sessions_memcache
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import images
from google.appengine.api import mail
from google.appengine.api.app_identity import *

import model

# Import the helper functions
from identitytoolkit import gitkitclient

import httpagentparser

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+"/templates"))

unsupported_browsers = {"Microsoft Internet Explorer": ["5.0", "6.0"]}

# Import the configuration file you downloaded from Google Developer Console
server_config_json = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'gitkit-server-config.json')
gitkit_instance = gitkitclient.GitkitClient.FromConfigFile(server_config_json)

class BaseHandler(webapp.RequestHandler):
  @toplevel
  def dispatch(self):
    # Get a session store for this request.
    sessions.default_config['secret_key'] = "wIDjEesObzp5nonpRHDzSp40aba7STuqC6ZRY"
    self.session_store = sessions.get_store(request=self.request)

    try:
        # Dispatch the request.
        webapp.RequestHandler.dispatch(self)
    finally:
        # Save all sessions.
        #logging.info(self.get_context())
        #self.set_context()
        self.session_store.save_sessions(self.response)

  @webapp.cached_property
  def session(self):
      # Returns a session using the default cookie key.
    return self.session_store.get_session(backend="memcache")

  channels_store = {}
  
  @classmethod
  def channels(cls):
    return cls.channels_store

  def get_current_user(self):
    user = self.session.get("user")
    if user is None:
      gitkit_user = self.get_current_gtk_user()
      if gitkit_user:
        user = model.User.get_by_uid(gitkit_user.user_id)
        self.session["user"] = user
    return user

  def get_current_gtk_user(self):
    gitkit_user = self.session.get("gitkit_user")
    if gitkit_user is None:
      if 'gtoken' in self.request.cookies:
        gitkit_user = gitkit_instance.VerifyGitkitToken(self.request.cookies['gtoken'])
        logging.info(str(gitkit_user.ToRequest()))
        #gitkit_user = gitkit_instance.GetUserById(gitkit_user.user_id)
        #logging.info(str(gitkit_user.ToRequest()))
        self.session["gitkit_user"] = gitkit_user


    return gitkit_user

  def get_base(self, template_values):

    #if self.request.url.find("appspot.com") != -1 and self.request.url.find("test") == -1 and self.request.url.find("-hr") == -1:
    #  self.redirect("http://.coderbot.org")

    uri = self.request.url[self.request.url.find('//')+2:]

    url, url_linktext = self.get_login_url_text()

    if "main" not in template_values:
      template_values["main"] = 'main.html'
    #template_values["user"] = user
    template_values["url"] = url
    template_values["url_linktext"] = url_linktext
    template_values["locale"] = self.get_locale()
    template_values["host"] = self.get_host()
    template_values["version"] = "0.0.0.1 - 2015.06.01"

    template = jinja_environment.get_template(template_values["main"])
    self.response.write(template.render(template_values))

  def render_template(template_path, template_values):
    template = jinja_environment.get_template(template_path)
    return template.render(template_values)

  #response object dump as json string
  def output_as_json(self, obj):
    self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
    json.dump(obj, self.response.out)

  def get_host(self):
    host = self.request.url[len("http://"):]
    host = host[:host.find("/")]
    return host

  def get_login_url_text(self):
    url = None
    url_linktext = None
    if self.get_current_user():
      url = "/eauth/logout"
      url_linktext = 'Esci'
    else:
      url = "/eauth/login?next=" + self.request.uri
      url_linktext = 'Entra'
    return url, url_linktext

  def get_locale(self):
    # otherwise try to guess the language from the user accept
    # header the browser transmits.
    loc = self.request.accept_language.best_match(['it', 'en', 'fr', 'es'])
    if loc is None:
      loc = 'en'
    return loc



def handle_404(request, response, exception):
  c = {'exception': exception.status}
  jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)[0:len(os.path.dirname(__file__))-3]+"/templates"))
  template = jinja_environment.get_template('404.html')
  t = template.render(c)
  response.write(t)
  response.set_status(exception.status_int)

def handle_500(request, response, exception):
  c = {'exception': traceback.format_exc(20)}
  logging.info(c["exception"])
  sender = "CoderBot <info@coderbot.org>"
  message = mail.EmailMessage()
  message.sender = sender
  message.to = sender
  message.subject = "CoderBot - Exception"
  message.body = """Exception in CoderBot.
  Request: """ + str(request.url) + """
  Exception: """ + str(exception) + """

  <Stacktrace>:
  """ + traceback.format_exc(20) + """

  <Stacktrace/>
  """

  message.send()

  jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)[0:len(os.path.dirname(__file__))-3]+"/templates"))
  template = jinja_environment.get_template('500.html')
  t = template.render(c)
  response.write(t)
  response.set_status(500)

def admin_required(func):
  def callf(base_page, *args, **kwargs):
    user = base_page.request.user if base_page.request.user else None
    if user == None or not user.is_admin():
      base_page.redirect("/auth/login?mode=select&next" + base_page.request.url)
    else:
      return func(basePage, *args, **kwargs)
  return callf

def user_gtk_required(func):
  def callf(base_page, *args, **kwargs):
    gtk_user = base_page.get_current_gtk_user()
    if gitkit_user:
      base_page.redirect("/auth/login?mode=select&next" + base_page.request.url)
    else:
      return func(base_page, *args, **kwargs)
  return callf

def api_user_gtk_required(func):
  def callf(base_page, *args, **kwargs):
    gtk_user = base_page.get_current_gtk_user()
    if gitkit_user:
      retval = {"status": "ko", "message": "auth missing" }
      base_page.response.write(json.dumps(retval))
    else:
      return func(base_page, *args, **kwargs)
  return callf

def user_required(func):
  def callf(base_page, *args, **kwargs):
    user = base_page.get_current_user()
    if user == None:
      base_page.redirect("/auth/login?mode=select&next" + base_page.request.url)
    else:
      return func(base_page, *args, **kwargs)
  return callf

def api_user_required(func):
  def callf(base_page, *args, **kwargs):
    user = base_page.get_current_user()
    if user == None:
      retval = {"status": "ko", "message": "auth missing" }
      base_page.response.write(json.dumps(retval))
    else:
      return func(base_page, *args, **kwargs)
  return callf

def api_bot_required(func):
  def callf(base_page, *args, **kwargs):
    auth = base_page.request.headers.get("Authorization")
    if auth != "CoderBot 123456":
      retval = {"status": "ko", "message": "auth missing" }
      base_page.response.write(json.dumps(retval))
    else:
      return func(base_page, *args, **kwargs)
  return callf

def reguser_required(func):
  def callf(base_page, *args, **kwargs):
    user = base_page.request.user if base_page.request.user else None
    if user == None:
      base_page.redirect("/auth/login?mode=select&next" + base_page.request.url)
    else:
      return func(base_page, *args, **kwargs)
  return callf

def cors_enabled(func):
  def callf(base_page, *args, **kwargs):
    if isinstance(base_page, webapp.RequestHandler):
      base_page.response.headers.add_header("Access-Control-Allow-Origin", "*")
      return func(base_page, *args, **kwargs)
  return callf
