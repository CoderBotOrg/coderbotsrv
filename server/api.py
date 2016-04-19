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
import json
import logging

import model

# Import the helper functions
from identitytoolkit import gitkitclient

from base import BaseHandler, api_user_required, api_bot_required, api_user_gtk_required, cors_enabled

class NewBotHandler(BaseHandler):

  @cors_enabled
  def post(self):
    data = {}
    try:
      data = json.loads(self.request.body)
    except ValueError as e:
      logging.error("invalid input: " + str(e))
      return

    #search for existing Bot
    bot = model.Bot.get_by_uid(data.get("bot_uid"))
    if bot:
      logging.info("bot already registered")
      self.response.write( json.dumps({"status": "ko", "retcode": "bot_already_registered"}) )
      return

    user_owner = model.User.get_by_email(data.get("user_email"))
    logging.info("user_email: " + data.get("user_email") + " user: " + str(user_owner))
    if user_owner == None:
      user_owner = model.User()
      user_owner.email = data.get("user_email")
      user_owner.status = model.User.PRE_ACTIVE # 0 = pre-registered
      user_owner.put()

    bot = model.Bot()
    bot.uid = data.get("bot_uid")
    bot.name = data.get("bot_name")
    bot.local_ip = data.get("bot_ip")
    bot.image = data.get("bot_image")
    bot.owner = user_owner.key
    bot.version = data.get("bot_version")
    bot.put()

    retval = {"status": "ok", "retcode": "registration_complete"}
    self.response.write( json.dumps(retval) )

class ListBotHandler(BaseHandler):

  @cors_enabled
  @api_user_required
  def get(self):
    logging.info("ListBotHandler")
    user = self.get_current_user()
    bots = model.Bot.get_by_owner(user)
    bot_list = []
    for bot in bots:
      bot_list.append(bot.as_dict())
    logging.info(str(bot_list))

    retval = {"status": "ok", "bot_list": bot_list}
    self.response.write( json.dumps(retval) )


class BotHandler(BaseHandler):
  def get(self, bot_uid):
    bot = model.Bot.get_by_uid(bot_uid)
    if bot == None:
      return

    retval = {"status": "ok", "bot_data": bot.as_dict() }
    self.response.write( json.dumps(retval) )


  def put(self, bot_uid):
    data = {}
    try:
      data = json.loads(self.request.body)
    except ValueError as e:
      logging.error("invalid input: " + str(e))

    #search for existing Bot
    bot = model.Bot.get_by_uid(bot_uid)
    if bot == None:
      logging.info("bot not present ")
      self.response.write( json.dumps({"status": "ko", "retcode": "bot_not_present"}) )
      return

    user_owner = User.get_by_email(data.get("user_email"))

    if data.get("local_ip"):
      bot.local_ip = data.get("local_ip")
    if data.get("name"):
      bot.name = data.get("name")
    if data.get("version"):
      bot.version = data.get("version")
    bot.put()

    retval = {"status": "ok", "retcode": "update_complete"}
    self.response.write( json.dumps(retval) )

class NewUserHandler(BaseHandler):
  def post(self):
    data = {}
    try:
      data = json.loads(self.request.body)
    except ValueError as e:
      logging.error("invalid input: " + str(e))
      return

    user = User.get_by_email(data.get("email"))
    if user and user.status != model.User.PRE_ACTIVE:
      logging.info("user already registered")
      self.response.write( json.dumps({"status": "ko", "retcode": "user_already_registered"}) )
      return
    if user == None:
      user = model.User()

    user.email = data.get("email")
    user.first_name = data.get("first_name")
    user.last_name = data.get("last_name")
    user.avatar_url = data.get("avatar_url")
    user.status = model.User.ACTIVE # 1 = registered
    user.put()

    retval = {"status": "ok", "retcode": "registration_complete"}
    self.response.write( json.dumps(retval) )

class GTKUserHandler(BaseHandler):

  @api_user_gtk_required
  def get(self):
    user = self.get_current_gtk_user()
    retval = {"status": "ok", "user_data": user }
    self.response.write( json.dumps(retval) )

class UserHandler(BaseHandler):

  def get(self):
    user = self.get_current_user()
    if user:
      retval = {"status": "ok", "user_data": user.as_dict() }
    else:
      retval = {"status": "ko", "ret_code": "user_not_logged" }
    self.response.write( json.dumps(retval) )

  @api_user_required
  def post(self):
    user = self.get_current_user()

    data = {}
    try:
      data = json.loads(self.request.body)
    except ValueError as e:
      logging.error("invalid input: " + str(e))
      return

    user.email = data.get("email")
    user.first_name = data.get("first_name")
    user.last_name = data.get("last_name")
    user.avatar_url = data.get("avatar_url")
    user.put()

    retval = {"status": "ok", "retcode": "user_updated" }
    self.response.write( json.dumps(retval) )

class NewProgramHandler(BaseHandler):
  def post(self):
    data = {}
    retval = {"status": "ok", "retcode": "program_created", "prog_id": 1}
    self.response.write( json.dumps(retval) )

class ListProgramHandler(BaseHandler):

  @cors_enabled
  @api_user_required
  def get(self):
    programs = model.Program.find_by_author(self.get_current_user())
    program_list = []
    for program in programs:
      program_list.append(program.as_dict())

    retval = {"status": "ok", "program_list": program_list}
    logging.info(str(retval))
    self.response.write( json.dumps(retval) )

  @cors_enabled
  @api_user_required
  def post(self):
    data = json.loads(self.request.body)
    tags = data.get("tags", [])
    status = data.get("status", model.Program.STATUS_PRIVATE)
    programs = model.Program.find_by_tag_status(tags, status)
    program_list = []
    for program in programs:
      program_list.append(program.as_dict())

    retval = {"status": "ok", "program_list": program_list}
    self.response.write( json.dumps(retval) )

class ProgramHandler(BaseHandler):

  @cors_enabled
  @api_bot_required
  def post(self, prog_id):
    data = json.loads(self.request.body)
    if data.get("prog_id"):
      #update existing
      program = model.Program.get_by_id(data.get("prog_id"))
    else:
      #create new
      program = model.Program()

    program.from_dict(data)
    program.put()

    retval = {"status": "ok", "retcode": "program_created"}
    self.response.write( json.dumps(retval) )

  def get(self, prog_id):
    retval = {}
    try:
      program = model.Program.get_by_id(int(prog_id))
      retval = {"status": "ok", "program_data": program.as_dict()}
    except:
      retval = {"status": "ko", "retcode": "program_not_found"}
    self.response.write( json.dumps(retval) )


app = webapp2.WSGIApplication([
    ('/api/coderbot/1.0/bot', NewBotHandler),
    ('/api/coderbot/1.0/bot/list', ListBotHandler),
    ('/api/coderbot/1.0/bot/(.*)', BotHandler),
    ('/api/coderbot/1.0/user/new', NewUserHandler),
    ('/api/coderbot/1.0/user/current', UserHandler),
    ('/api/coderbot/1.0/program', NewProgramHandler),
    ('/api/coderbot/1.0/program/list', ListProgramHandler),
    ('/api/coderbot/1.0/program/(.*)', ProgramHandler)
], debug=True)
