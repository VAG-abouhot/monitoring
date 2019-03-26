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


MAX_API_KEY_LENGTH = 500



class Client(object):
    """
    Entry point in the Python Client API.
    You should instantiate a Client object with your ApplicationID, ApiKey to
    start using Monitoring Service.
    """

    def __init__(self, app_id, api_key, hosts=None, _transport=None):
        """
        Monitoring Client initialization
        @param app_id the application ID you have in your admin interface
        @param api_key a valid API key for the service
        @param hosts_array the list of hosts that you have received for the service
        """
        self._transport = Transport() if _transport is None else _transport

      ################" START TODO ########################"
        if not hosts: # TODO mettre la liste des serveurs (1 pour l'instant)
            fallbacks = [
                'monitoring.validandgo.com/%s' % app_id,
            ]
            random.shuffle(fallbacks)

            self._transport.read_hosts = ['monitoring.validandgo.com/%s' % app_id] 
            # TODO y a un serveur read.monitoring et write.monitoring
            self._transport.read_hosts.extend(fallbacks)
            self._transport.write_hosts = ['monitoring.validandgo.com/%s' % app_id]
            self._transport.write_hosts.extend(fallbacks)
        else:
            self._transport.read_hosts = hosts
            self._transport.write_hosts = hosts

        self._transport.headers = {
            'X-Monitoring-Application-Id': app_id,
            'Content-Type': 'gzip',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'Monitoring for Python (%s); Python (%s)' % (VERSION, python_version()),
        }
        ################" END TODO ########################"
        self._app_id = app_id
        self._api_key = api_key


    @property
    def app_id(self):
        return self._app_id

    @property
    def api_key(self):
        return self._api_key

    @property
    def headers(self):
        return self._transport.headers


    def delete_application(self, application_name, request_options=None):
        """
        Delete an application.
        Return an object of the form: {'deleted_at': '2013-01-18T15:33:13.556Z'}
        @param application_name the name of application to delete
        """
        path = '/application/%s' % safe(application_name)
        return self._req(False, path, 'DELETE', request_options)

    def move_application(self, src_application_name, dst_application_name, request_options=None):
        """
        Move an existing application.
        @param src_application_name the name of application to copy.
        @param dst_application_name the new application name that will contains a copy
            of src_application_name (destination will be overriten if it already exist).
        """
        path = '/application/%s' % safe(src_application_name)
        request = {'operation': 'move', 'destination': dst_application_name}
        return self._req(False, path, 'POST', request_options, data=request)


    def copy_application(self, src_application_name, dst_application_name, request_options=None, scope=None):
        """
        Copy an existing application.
        @param src_application_name the name of index to copy.
        @param dst_application_name the new application name that will contains a copy of
            src_application_name (destination will be overriten if it already exist).
        @param scope the scope of the copy, as a list. Possible items are:
            settings, rules, synonyms.
        """
        path = '/application/%s' % safe(src_application_name)
        request = {'operation': 'copy', 'destination': dst_application_name}

        if scope is not None:
            request['scope'] = scope

        return self._req(False, path, 'COPY', request_options, data=request)

    def monitoring_session(self, application_name, model_name):        
        """
        Create a new monitoring sesion.
        @param application_name name of application concerned.
        @param model_name name of model selected.
        """
        return Session(self, application_name, model_name)
        
        
        
        
        
        
        
        
        
        
        
        
    def get_logs(self, offset=0, length=10, type='all', request_options=None):
        """
        Return last logs entries.
        @param offset Specify the first entry to retrieve (0-based,
            0 is the most recent log entry).
        @param length Specify the maximum number of entries to retrieve
            starting at offset. Maximum allowed value: 1000.
        """
        params = {'offset': offset, 'length': length, 'type': type}
        return self._req(False, '/1/logs', 'GET', request_options, params)

    def init_application(self, application_name):
        """
        Get the application object initialized (no server call needed for
        initialization).
        @param application_name the name of application
        """
        return Application(self, application_name, description, prediction_type)
        
        
    def create_application(self, application_name, description, prediction_type, data_input, data_output, metadata, params):
        """
        Create the application object
        @param description the description of application (text)
        @prediction_type the type of prediction like regression, binary classification, multi-class
        @data_input explicative features
        @data_output target
        @metadata illustrative features
            Data is a list of dict [{name, label, type, description}] 
        @params additionnal params like the threshold
        """
        return Application(self, application_name).create(description, prediction_type, data_input, data_output, metadata, params)
 
    def list_api_keys(self, request_options=None):
        """List all existing api keys with their associated ACLs."""
        return self._req(True, '/1/keys', 'GET', request_options)

    def get_api_key(self, api_key, request_options=None):
        """'Get ACL of an api key."""
        path = '/1/keys/%s' % api_key
        return self._req(True, path, 'GET', request_options)

    def delete_api_key(self, api_key, request_options=None):
        """Delete an existing api key."""
        path = '/1/keys/%s' % api_key
        return self._req(False, path, 'DELETE', request_options)

    def restore_api_key(self, api_key, request_options=None):
        """Restore an api key."""
        path = '/1/keys/%s/restore' % api_key
        return self._req(False, path, 'POST', request_options)

    def add_api_key(self, obj,
                    validity=0,
                    max_queries_per_ip_per_hour=0,
                    max_hits_per_query=0,
                    indexes=None,
                    request_options=None):
        """
        Create a new api key.
        @param obj can be two different parameters:
            The list of parameters for this key. Defined by a NSDictionary that
            can contains the following values:
                - acl: array of string
                - indices: array of string
                - validity: int
                - referers: array of string
                - description: string
                - maxHitsPerQuery: integer
                - queryParameters: string
                - maxQueriesPerIPPerHour: integer
            Or the list of ACL for this key. Defined by an array of NSString that
            can contains the following values:
                - search: allow to search (https and http)
                - addObject: allows to add/update an object in the index (https only)
                - deleteObject : allows to delete an existing object (https only)
                - deleteIndex : allows to delete index content (https only)
                - settings : allows to get index settings (https only)
                - editSettings : allows to change index settings (https only)
        @param validity the number of seconds after which the key will be
            automatically removed (0 means no time limit for this key)
        @param max_queries_per_ip_per_hour Specify the maximum number of API
            calls allowed from an IP address per hour.  Defaults to 0 (no rate limit).
        @param max_hits_per_query Specify the maximum number of hits this API
            key can retrieve in one call. Defaults to 0 (unlimited)
        @param indexes the optional list of targeted indexes
        """
        if not isinstance(obj, dict):
            obj = {'acl': obj}

        # Check with `is not None`, because 0 is evaluated to False
        if validity is not None:
            obj['validity'] = validity
        if max_queries_per_ip_per_hour is not None:
            obj['maxQueriesPerIPPerHour'] = max_queries_per_ip_per_hour
        if max_hits_per_query is not None:
            obj['maxHitsPerQuery'] = max_hits_per_query

        if indexes:
            obj['indexes'] = indexes

        return self._req(False, '/1/keys', 'POST', request_options, data=obj)


    def update_api_key(self, api_key, obj,
                        validity=None,
                        max_queries_per_ip_per_hour=None,
                        max_hits_per_query=None,
                        indexes=None,
                        request_options=None):
        """
        Update a api key.
        @param obj can be two different parameters:
            The list of parameters for this key. Defined by a NSDictionary that
            can contains the following values:
                - acl: array of string
                - indices: array of string
                - validity: int
                - referers: array of string
                - description: string
                - maxHitsPerQuery: integer
                - queryParameters: string
                - maxQueriesPerIPPerHour: integer
            Or the list of ACL for this key. Defined by an array of NSString that
            can contains the following values:
                - search: allow to search (https and http)
                - addObject: allows to add/update an object in the index (https only)
                - deleteObject : allows to delete an existing object (https only)
                - deleteIndex : allows to delete index content (https only)
                - settings : allows to get index settings (https only)
                - editSettings : allows to change index settings (https only)
        @param validity the number of seconds after which the key will be
            automatically removed (0 means no time limit for this key)
        @param max_queries_per_ip_per_hour Specify the maximum number of API
            calls allowed from an IP address per hour.  Defaults to 0 (no rate limit).
        @param max_hits_per_query Specify the maximum number of hits this API
            key can retrieve in one call. Defaults to 0 (unlimited)
        @param indexes the optional list of targeted indexes
        """
        if not isinstance(obj, dict):
            obj = {'acl': obj}

        # Check with `is not None`, because 0 is evaluated to False
        if validity is not None:
            obj['validity'] = validity
        if max_queries_per_ip_per_hour is not None:
            obj['maxQueriesPerIPPerHour'] = max_queries_per_ip_per_hour
        if max_hits_per_query is not None:
            obj['maxHitsPerQuery'] = max_hits_per_query

        if indexes:
            obj['indexes'] = indexes

        path = '/1/keys/%s' % api_key
        return self._req(False, path, 'PUT', request_options, data=obj)


    def is_alive(self, request_options=None):
        """
        Test if the server is alive.
        This performs a simple application-level ping. If up and running, the server answers with a basic message.
        """
        return self._req(True, '/1/isalive', 'GET', request_options)

    def _req(self, is_search, path, meth, request_options=None, params=None, data=None):
        if len(self.api_key) > MAX_API_KEY_LENGTH:
            if data is None:
                data = {}
            data['apiKey'] = self.api_key
        return self._transport.req(is_search, path, meth, params, data, request_options)