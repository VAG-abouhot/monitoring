# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Valind&GO
http://www.validandgo.com/
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import hmac
import hashlib
import base64
import random
import sys
import time
import copy
from platform import python_version

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from .version import VERSION
from .application import Application
from .session import Session
from .transport import Transport
from .helpers import deprecated
from .helpers import safe
from .helpers import urlify
from .helpers import endpoint
from .configs import MonitoringConfig

from monitoring.http.transporter import Transporter
from monitoring.http.requester import Requester
from monitoring.http.verb import Verb



class Client(object):
    """
    Entry point in the Python Client API.
    You should instantiate a Client object with your ApplicationID, ApiKey to
    start using Monitoring Service.
    """
    
    
    @property
    def app_id(self):
        # type: () -> str

        return self._config.app_id
        
        
    @property
    def api_key(self):
        # type: () -> str
    
        return self._config.api_key
   
        
    def __init__(self, transporter, monitoring_config):
        """
        Monitoring Client initialization
        @param transporter connection parameters
        @param monitoring_config user configuration system
        """
         # type: (Transporter, MonitoringConfig) -> None

        self._transporter = transporter
        self._config = monitoring_config



    @staticmethod
    def connect(app_id=None, api_key=None):
        # type: (Optional[str], Optional[str]) -> Client

        config = MonitoringConfig(app_id, api_key)

        return Client.connect_with_config(config)
        

    @staticmethod
    def connect_with_config(config):
        # type: (MonitoringConfig) -> Client

        requester = Requester()
        transporter = Transporter(requester, config)
        client = Client(transporter, config)

        return client
        
    def init_application(self, application_name): 
        # type: (str) -> Application

        return Application(self._transporter, self._config, application_name)
    
    
    def create_application(self, application_name, application_label, description, prediction_type, data_input, data_output, metadata, params):
        """
        Create an application object
        @param application_name application system name
        @param application_label application understandable name        
        @param description description of application (text)
        @prediction_type type of prediction (ex: regression, binary classification, multi-class)
        @data_input explicative features
        @data_output target
        @metadata illustrative features
            Data is a list of dict [{name, label, type, description}] 
        @params additionnal params
        """
        # type: (Transporter, MonitoringConfig, str, str, str, str, list, dict, list, dict) -> Application
        
        return Application.create(self._transporter, self._config, application_name, application_label, description, prediction_type, data_input, data_output, metadata, params)
        

    def delete_application(self, application_name, request_options=None):
        """
        Delete an application.
        Return an object of the form: {'deleted_at': '2013-01-18T15:33:13.556Z'}
        @param application_name application name to delete
        """
        # type: (str, Optional[RequestOptions]) -> dict
        
        raw_response = self._transporter.write(
            Verb.DELETE,
            endpoint('/{}/delete', application_name),
            application_name,
            request_options
        )
        return raw_response

        
    def move_application(self, src_application_name, dst_application_name, request_options=None):
        """
        Move an existing application.
        @param src_application_name old name of application to move.
        @param dst_application_name new name of application name
            of src_application_name (destination will be overriten if it already exist).
        """
        # type: (str, str, Optional[RequestOptions]) -> dict
        
        raw_response = self._transporter.write(
            Verb.POST,
            endpoint('/{}/move', src_application_name),
            dst_application_name,
            request_options
        )
               
        return raw_response


    def monitoring_session(self, application_name, model_name):        
        """
        Create a new monitoring sesion.
        @param application_name name of application concerned.
        @param model_name name of model selected.
        """
        # type: (str, str) -> Session
        
        return Session(self._transporter, self._config, application_name, model_name)
        

    def get_application(self, application_name, request_options=None):
        """
        Get the application information
        @param application_name the name of application
        """
        # type: (str, Optional[RequestOptions]) -> dict
        
        raw_response = self._transporter.read(
            Verb.GET,
            endpoint('/{}/get', application_name),
            application_name,
            request_options
        )
        
        return raw_response

        
    def browse_applications(self, filters = None, request_options=None):
        """
        Get all applications of the user
        @param filters optional filters list
        """
        # type: (Optional[list[dict]], Optional[RequestOptions]) -> dict
        
        raw_response = self._transporter.read(
            Verb.GET,
            endpoint('/applications',),
            filters,
            request_options
        )
        
        return raw_response
       
 