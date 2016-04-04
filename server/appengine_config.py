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
import os
import sys
import logging
from google.appengine.api.app_identity import *
ON_DEV = False
ON_TEST = False
try:
  ON_DEV = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
  ON_TEST = "test" in get_application_id()
except:
  pass
import fixpath

#########################################
# Remote_API Authentication configuration.
#
# See google/appengine/ext/remote_api/handler.py for more information.
# For datastore_admin datastore copy, you should set the source appid
# value.  'HTTP_X_APPENGINE_INBOUND_APPID', ['trusted source appid here']
#
remoteapi_CUSTOM_ENVIRONMENT_AUTHENTICATION = (
    'HTTP_X_APPENGINE_INBOUND_APPID', ['coderbot.org'])

#def webapp_add_wsgi_middleware(app):
    #from google.appengine.ext.appstats import recording
    #app = recording.appstats_wsgi_middleware(app)
    #return app

logging.info("Dev: " + str(ON_DEV))
logging.info("Test: " + str(ON_TEST))
