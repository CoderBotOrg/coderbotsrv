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
import datetime
import os
import base64

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
  def get_by_id(cls, user_id):
    return model.Key("User", user_id).get()

  @classmethod
  def get_by_uid(cls, uid):
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
  owner = model.KeyProperty(kind=User)

  c_d = model.DateTimeProperty(auto_now_add=True)
  c_u = model.KeyProperty(kind=User)
  m_d = model.DateTimeProperty(auto_now=True)
  m_u = model.KeyProperty(kind=User)

  status = model.IntegerProperty()

  def as_dict(self):
    return { "uid": self.uid,
             "name": self.name,
             "image": "data:image/jpeg;base64," + base64.b64encode(self.image) if self.image else '/static/img/coderbot_default_image.jpg',
             "version": self.version,
             "local_url": "http://" + self.local_ip + ":8080/" }

  def from_dict(self, data):
    self.uid = data.get("uid")
    self.name = data.get("name")
    if data.get("image"):
      self.image = base64.b64decode(data.get("image")[len("data:image/jpeg;base64,"):])
    self.version = data.get("version")

  @classmethod
  def get_by_uid(cls, uid):
    return cls.query().filter(cls.uid==uid).get()

  @classmethod
  def get_by_owner(cls, user):
    return cls.query().filter(cls.owner==user.key)

class Project(model.Model):

  name = model.StringProperty()
  desc = model.TextProperty()

  c_d = model.DateTimeProperty(auto_now_add=True)
  c_u = model.KeyProperty(kind=models.User)
  m_d = model.DateTimeProperty(auto_now=True)
  m_u = model.KeyProperty(kind=models.User)

  status = model.IntegerProperty()


class Program(model.Model):

  name = model.StringProperty()
  code = model.TextProperty()
  dom_code = model.TextProperty()

  parent = model.KeyProperty()

  c_d = model.DateTimeProperty(auto_now_add=True)
  c_u = model.KeyProperty(kind=models.User)
  m_d = model.DateTimeProperty(auto_now=True)
  m_u = model.KeyProperty(kind=models.User)

  tags = model.StringProperty(repeated=True)

  STATUS_PRIVATE=1
  STATUS_PUBLIC=10
  STATUS_DELETED=99

  status = model.IntegerProperty()

  version = model.IntegerProperty(indexed=False)

  def as_dict(self):
    return { "uid": str(self.key.id()),
             "name": self.name,
             "code": self.code,
             "dom_code": self.dom_code,
             "tags": self.tags,
             "c_u": self.c_u.get().as_dict(),
             "c_d": datetime.datetime.strftime(self.c_d, "%Y%m%d%H%M%S"),
             "m_u": self.m_u.get().as_dict(),
             "m_d": datetime.datetime.strftime(self.m_d, "%Y%m%d%H%M%S"),
             "status": self.status,
             "version": self.version }

  def from_dict(self, data):
    self.name = data["name"]
    self.code = data["code"]
    self.dom_code = data["dom_code"]
    self.tags = data["tags"]
    #for t in data["tags"]:
    #  self.tags = t
    self.status = data.get("status", 1)
    if self.c_u is None and data.get("c_u"):
      self.c_u = User.get_by_id(int(data["c_u"]["uid"])).key
    if data.get("c_d"):
      self.c_d = datetime.datetime.strptime(data["c_d"], "%Y%m%d%H%M%S")
    if self.m_u is None and data.get("m_u"):
      self.m_u = User.get_by_id(int(data["m_u"]["uid"])).key
    if data.get("m_d"):
      self.m_d = datetime.datetime.strptime(data["m_d"], "%Y%m%d%H%M%S")
    self.version = data["version"]

  @classmethod
  def get_by_id(cls, id):
    return model.Key("Program", id).get()

  @classmethod
  def find_by_author(cls, user, status=STATUS_PRIVATE):
    return cls.query().filter(cls.c_u==user.key).filter(cls.status==status)

  @classmethod
  def find_by_status_tags(cls, status, tags):
    query = cls.query().filter(cls.status==status)
    if tags and len(tags):
        query = query.filter(cls.tags.IN(tags))
    return query
