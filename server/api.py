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
import datetime
import time
import logging
import copy

from google.appengine.api import memcache
import model

# Import the helper functions
from identitytoolkit import gitkitclient

from base import BaseHandler, api_user_required, api_bot_required, api_user_gtk_required, cors_enabled

class BotHandler(BaseHandler):

  @cors_enabled
  @api_bot_required
  def get(self, bot_id):
    try:
      bot = model.Bot.get_by_uid(bot_id)
      retval = {"status": "ok", "bot": bot.as_dict()}
    except Exception as e:
      logging.error("Exception: " + str(e))
      retval = {"status": "ko"}
    self.response.write( json.dumps(retval) )

  @cors_enabled
  @api_bot_required
  def post(self, bot_id):
    logging.info("BotNew: " + bot_id)
    data = {}
    try:
      data = json.loads(self.request.body)

      #search for existing Bot
      bot = model.Bot.get_by_uid(bot_id)
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
      bot.uid = bot_id
      bot.name = data.get("bot_name")
      bot.local_ip = data.get("bot_ip")
      bot.image = data.get("bot_image")
      bot.owner = user_owner.key
      bot.version = data.get("bot_version")
      bot.put()

      retval = {"status": "ok", "retcode": "registration_complete"}
    except Exception as e:
      logging.error("Exception: " + str(e))
      retval = {"status": "ko"}
    self.response.write( json.dumps(retval) )

  @cors_enabled
  @api_bot_required
  def put(self, bot_uid):
    data = {}
    try:
      data = json.loads(self.request.body)

      #search for existing Bot
      bot = model.Bot.get_by_uid(bot_uid)
      if bot == None:
        logging.error("bot not present ")
        raise ValueError()

      if data.get("local_ip"):
        bot.local_ip = data.get("local_ip")
      if data.get("name"):
        bot.name = data.get("name")
      if data.get("version"):
        bot.version = data.get("version")
      bot.put()

      retval = {"status": "ok", "retcode": "update_complete"}
    except Exception as e:
      logging.error("invalid input: " + str(e))
      retval = {"status": "ko", "retcode": "invalid_input"}

    self.response.write( json.dumps(retval) )

class BotUserNewHandler(BaseHandler):

  @cors_enabled
  @api_bot_required
  def post(self):
    data = {}
    try:
      data = json.loads(self.request.body)

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
    except Exception as e:
      logging.error("Exception: " + str(e))
      retval = {"status": "ko"}
    self.response.write( json.dumps(retval) )

class BotProgramListHandler(BaseHandler):
  @cors_enabled
  @api_bot_required
  def get(self, bot_id):
    logging.info("BotProgramListHandler: " + bot_id)
    try:
      bot = model.Bot.get_by_uid(bot_id)
      programs = model.Program.find_by_author(bot.owner.get())
      program_list = []
      for program in programs:
        program_list.append(program.as_dict())

      retval = {"status": "ok", "program_list": program_list}
    except Exception as e:
      logging.error("Exception: " + str(e))
      retval = {"status": "ko"}
    self.response.write( json.dumps(retval) )

class BotProgramHandler(BaseHandler):

  @cors_enabled
  @api_bot_required
  def post(self, bot_id, prog_id):
    try:
      data = json.loads(self.request.body)
      #logging.info("program_data: " + str(data))

      bot = model.Bot.get_by_uid(bot_id)

      program = None
      try:
        program = model.Program.get_by_id(int(prog_id))
      except ValueError:
        logging.info("uid=None")

      if program is None:
        #create new
        program = model.Program()
        program.c_u = bot.owner

      prog_data = data.update(data.get("data"))
      program.from_dict(data)
      program.m_u = bot.owner
      program.put()

      for channel in self.channels().values():
        if channel.get("user_id") == bot.owner.id:
          events = channel.get("events")
          if len(events) > 9:
            events = events[0:9]
          events.insert(0, {"ts": str(int(round(time.time() * 1000)))[:-1], "type": "program"})
          channel["events"] = events

      retval = {"status": "ok", "retcode": "program_saved", "program": program.as_dict()}
    except Exception as e:
      logging.error("Exception: " + str(e))
      retval = {"status": "ko"}
      raise
    self.response.write( json.dumps(retval) )

  @cors_enabled
  @api_bot_required
  def get(self, prog_id):
    retval = {}
    try:
      program = model.Program.get_by_id(int(prog_id))
      retval = {"status": "ok", "program_data": program.as_dict()}
    except Exception as e:
      logging.error("Exception: " + str(e))
      retval = {"status": "ko"}
    self.response.write( json.dumps(retval) )

class UserBotListHandler(BaseHandler):

  @cors_enabled
  @api_user_required
  def get(self):
    logging.info("ListBotHandler")
    try:
      user = self.get_current_user()
      bots = model.Bot.get_by_owner(user)
      bot_list = []
      for bot in bots:
        bot_list.append(bot.as_dict())
      #logging.info(str(bot_list))

      retval = {"status": "ok", "bot_list": bot_list}
    except Exception as e:
      logging.error("Exception: " + str(e))
      retval = {"status": "ko"}
    self.response.write( json.dumps(retval) )

class UserHandler(BaseHandler):

  @cors_enabled
  @api_user_required
  def get(self):
    user = self.get_current_user()
    try:
      if user:
        retval = {"status": "ok", "user_data": user.as_dict() }
      else:
        retval = {"status": "ko", "ret_code": "user_not_logged" }
    except Exception as e:
      logging.error("Exception: " + str(e))
      retval = {"status": "ko"}
    self.response.write( json.dumps(retval) )

  @cors_enabled
  @api_user_required
  def post(self):
    user = self.get_current_user()
    data = {}
    try:
      data = json.loads(self.request.body)

      user.email = data.get("email")
      user.first_name = data.get("first_name")
      user.last_name = data.get("last_name")
      user.avatar_url = data.get("avatar_url")
      user.put()

      retval = {"status": "ok", "retcode": "user_updated" }
    except Exception as e:
      logging.error("Exception: " + str(e))
      retval = {"status": "ko"}
    self.response.write( json.dumps(retval) )

class UserEventHandler(BaseHandler):

  @cors_enabled
  @api_user_required
  def get(self):
    user = self.get_current_user()
    now = datetime.datetime.now()

    channel = self.channels().get(id(self.session))
    if channel is None:
        self.channels()[id(self.session)] = channel = {"user_id": user.key.id, "ts" : now, "events":[]}

    events = []
    while datetime.datetime.now() < now + datetime.timedelta(seconds=20):
      events = copy.copy(channel["events"])
      if len(events):
        channel["events"] = []
        break
      else:
        time.sleep(1)
    retval = {"status": "ok", "events": events}
    self.response.write( json.dumps(retval) )

class UserBotHandler(BaseHandler):

  @cors_enabled
  @api_user_required
  def get(self, bot_uid):
    try:
      bot = model.Bot.get_by_uid(bot_uid)
      retval = {"status": "ok", "bot_data": bot.as_dict() }
    except Exception as e:
      logging.error("Exception: " + str(e))
      retval = {"status": "ko"}
    self.response.write( json.dumps(retval) )

  @cors_enabled
  @api_user_required
  def put(self, bot_uid):
    data = {}
    try:
      data = json.loads(self.request.body)

      #search for existing Bot
      bot = model.Bot.get_by_uid(bot_uid)
      if bot == None:
        logging.info("bot not present ")
        self.response.write( json.dumps({"status": "ko", "retcode": "bot_not_present"}) )
      else:
        if data.get("name"):
          bot.name = data.get("name")
        if data.get("version"):
          bot.version = data.get("version")
        bot.put()

      retval = {"status": "ok", "retcode": "update_complete"}
    except Exception as e:
      logging.error("Exception: " + str(e))
      retval = {"status": "ko"}
    self.response.write( json.dumps(retval) )

class UserProgramListHandler(BaseHandler):

  @cors_enabled
  @api_user_required
  def get(self):
    try:
      programs = model.Program.find_by_author(self.get_current_user())
      program_list = []
      for program in programs:
        program_list.append(program.as_dict())

      retval = {"status": "ok", "program_list": program_list}
    except Exception as e:
      logging.error("Exception: " + str(e))
      retval = {"status": "ko"}
    self.response.write( json.dumps(retval) )

  @cors_enabled
  @api_user_required
  def post(self):
    try:
      data = json.loads(self.request.body)
      tags = data.get("tags", [])
      status = data.get("status", model.Program.STATUS_PRIVATE)
      logging.info("status: " + str(status) + " tags: " + str(tags))
      programs = model.Program.find_by_status_tags(status, tags)
      program_list = []
      for program in programs:
        program_list.append(program.as_dict())

      retval = {"status": "ok", "program_list": program_list}
    except Exception as e:
      logging.error("Exception: " + str(e))
      retval = {"status": "ko"}
    self.response.write( json.dumps(retval) )

class UserProgramHandler(BaseHandler):

  @cors_enabled
  @api_user_required
  def post(self, prog_id):
    data = json.loads(self.request.body)
    program = model.Program.get_by_id(prog_id)
    if program is None:
      #create new
      program = model.Program()

    program.from_dict(data)
    program.put()

    retval = {"status": "ok", "retcode": "program_saved", "program": program.as_dict()}
    self.response.write( json.dumps(retval) )

  @cors_enabled
  @api_user_required
  def get(self, prog_id):
    retval = {}
    try:
      program = model.Program.get_by_id(int(prog_id))
      retval = {"status": "ok", "program_data": program.as_dict()}
    except:
      retval = {"status": "ko", "retcode": "program_not_found"}
    self.response.write( json.dumps(retval) )


app = webapp2.WSGIApplication([
    ('/api/coderbot/1.0/bot/(.*)/programs/(.*)', BotProgramHandler),
    ('/api/coderbot/1.0/bot/(.*)/programs', BotProgramListHandler),
    ('/api/coderbot/1.0/bot/(.*)/user', BotUserNewHandler),
    ('/api/coderbot/1.0/bot/(.*)', BotHandler),
    ('/api/coderbot/1.0/user/events', UserEventHandler),
    ('/api/coderbot/1.0/user/programs', UserProgramListHandler),
    ('/api/coderbot/1.0/user/programs/(.*)', UserProgramHandler),
    ('/api/coderbot/1.0/user/bots', UserBotListHandler),
    ('/api/coderbot/1.0/user/bots/(.*)', UserBotHandler),
    ('/api/coderbot/1.0/user', UserHandler)
], debug=True)
