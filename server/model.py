#!/usr/bin/env python
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

import logging
import fpformat

from google.appengine.ext.ndb import model, Cursor, Future, tasklet
from google.appengine.ext import blobstore
from google.appengine.api import memcache
from google.appengine.api import users

from common import cached_property, memcached_property, Const, Cache, Sanitizer, CETimeZone
from engineauth import models

class User(model.Model):

  uid = model.StringProperty()
  first_name = model.StringProperty(indexed=False)
  last_name =  model.StringProperty(indexed=False)
  email = model.StringProperty()

  avatar_url = model.StringProperty(indexed=False)
  avatar_data = model.BlobProperty()

  c_d = model.DateTimeProperty(auto_now_add=True)
  m_d = model.DateTimeProperty(auto_now=True)

  status = model.IntegerProperty()

  def is_active(self):
    return self.status != self.DISABLED

  def as_dict(self):
    return {"uid": self.uid,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "avatar_url": self.avatar_url,
            "status": self.status};

  @classmethod
  def get_by_uid(cls, uid):
    logging.info(uid)
    return cls.query().filter(cls.uid==str(uid)).get()

  @classmethod
  def get_by_email(cls, email):
    return cls.query().filter(cls.email==email).get()

  PRE_ACTIVE = 0
  ACTIVE = 1
  DISABLED = 99

class Bot(model.Model):

  uid = model.StringProperty()
  name = model.StringProperty()
  image = model.BlobProperty()
  version = model.StringProperty()
  capabilities = model.StringProperty(repeated=True)
  local_ip = model.StringProperty(indexed=False)
  owner = model.KeyProperty()

  c_d = model.DateTimeProperty(auto_now_add=True)
  c_u = model.KeyProperty(kind=models.User)
  m_d = model.DateTimeProperty(auto_now=True)
  m_u = model.KeyProperty(kind=models.User)

  status = model.IntegerProperty()

  def as_dict(self):
    return { "uid": self.uid,
             "name": self.name,
             "image_url": self.image,
             "version": self.version,
             "local_url": "http://" + self.local_ip + ":8080/" }

  @classmethod
  def get_by_uid(cls, uid):
    return cls.query().filter(cls.uid==uid).get()

  @classmethod
  def get_by_owner(cls, user):
    return cls.query().filter(cls.owner==user.key)

class Project(model.Model):

  name = model.StringProperty()
  desc = model.TextProperty()

  author = model.KeyProperty()

  c_d = model.DateTimeProperty(auto_now_add=True)
  c_u = model.KeyProperty(kind=models.User)
  m_d = model.DateTimeProperty(auto_now=True)
  m_u = model.KeyProperty(kind=models.User)

  status = model.IntegerProperty()


class Program(model.Model):

  name = model.StringProperty()
  code = model.TextProperty()

  author = model.KeyProperty()

  c_d = model.DateTimeProperty(auto_now_add=True)
  c_u = model.KeyProperty(kind=models.User)
  m_d = model.DateTimeProperty(auto_now=True)
  m_u = model.KeyProperty(kind=models.User)

  status = model.IntegerProperty()

  def as_dict(self):
    return { "uid": str(self.key.id),
             "name": self.name,
             "image_url": "/static/img/coderbot_logo_128.png"}
  @classmethod
  def get_by_author(cls, user):
    return cls.query().filter(cls.author==user.key)
