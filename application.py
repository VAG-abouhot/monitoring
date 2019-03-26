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

import time
import random
import string

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from .helpers import MonitoringException
from .helpers import deprecated
from .helpers import urlify
from .helpers import safe


class IndexIterator:
    """Iterator on index."""

    def __init__(self, index, params=None, cursor=None, request_options=None):
        if params is None:
            params = {}

        self.index = index
        self.params = params
        self.cursor = cursor
        self.request_options = request_options

    def __iter__(self):
        self._load_next_page()
        return self

    def __next__(self):
        return self.next()

    def next(self):
        while True:
            if self.pos < len(self.answer['hits']):
                self.pos += 1
                return self.answer['hits'][self.pos - 1]
            elif self.cursor:
                self._load_next_page()
                continue
            else:
                raise StopIteration

    def _load_next_page(self):
        self.answer = self.index.browse_from(self.params, self.cursor, self.request_options)
        self.pos = 0
        self.cursor = self.answer.get('cursor', None)


class Application(object):
    """
    Contains all the functions related to one application.
    >>> application = client.init_application('myApplicationName')
    """

    def __init__(self, client, application_name):
        self.client = client
        self.application_name = application_name
        self._request_path = '/applications/%s' % safe(self.application_name)

    def __repr__(self):
        return u'<Application: %r>' % self.application_name

    def create(self, description, prediction_type, data_input, data_output, metadata, params, request_options=None):
        self.description = description
        self.prediction_type = prediction_type
        self.data_input = data_input
        self.data_output = data_output
        self.metadata = metadata
        self.params = params
        path = '' #TODO potentiellement mais je pense que c'est ok
        self._req(False, path, 'PUT', request_options, data=self)
        return self #TODO 

    def add_model(self, model_name, model_label, model_description, model_version, request_options=None):
        """
        Add an model in this application.
        @param model_name name of the model
        @param model_label label of the model
        @param model_description description of the model
        @param model_version version of the model
        """
        path = '/%s' % safe(model_name)
        self._req(False, path, 'PUT', request_options, data={
                'model_name': model_name, 
                'model_label': model_label,
                'model_description': model_description, 
                'model_version': model_version, 
            }) # TODO potentiellement créer un objet ? et renvoyé 
        return self



    def get_model(self, model_name, request_options=None):
        """
        Get an model from this application.
        @param model_name the unique identifier of the model to retrieve
        """
        path = '/%s' % safe(model_name)
        return self._req(True, path, 'GET', request_options)
       


    def delete_model(self, model_name, request_options=None):
        """
        Delete an model from the application.
        @param model_id the unique identifier of object to delete
        """
        if not model_name:
            raise MonitoringException('model_name cannot be empty')

        path = '/%s' % safe(model_name)
        return self._req(False, path, 'DELETE', request_options)

    def select_model(self, model_name, request_options=None):
        """
        Delete an model from the application.
        @param model_id the unique identifier of object to delete
        """
        if not model_name:
            raise MonitoringException('model_name cannot be empty')

        path = '/%s' % safe(model_name)
        return self._req(False, path, 'DELETE', request_options)
        
    def browse_models(self, params=None, request_options=None):
        """
         Browse all model's application.
         @param params contains the list of query parameter in a dictionary
         @return an iterator on the index content
        """
        return 'TODO'
        #return IndexIterator(self, params=params, request_options=request_options)


    def _req(self, is_search, path, meth, request_options=None, params=None, data=None):
        """Perform an HTTPS request with retry logic."""
        path = '%s%s' % (self._request_path, path)
        return self.client._req(is_search, path, meth, request_options, params, data)