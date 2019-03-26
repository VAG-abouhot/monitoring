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

from .helpers import safe

class Session(object):
    """
    Contains all the functions related to one monitoring session.
    >>> session = client.monitoring_session(self,'application_name', 'model_name')
    """
    
    def __init__(self, client, application_name, model_name):
        self.client = client
        self.application_name = application_name
        self.model_name = model_name
        self._request_path = '/%s/%s/prediction' % (self.application_name, self.model_name)

    def __repr__(self):
        return u'<Session: %r>' % self._request_path
        
    def start(self, request_options=None):
        """
        Start a new session to record logs from model.
        """
        path = ''
        self._req(False, path, 'PUT', request_options)
        return self
 
    def set_data_input(self, data):
        """
        Set explicative features
        """
        self.data_input = data

    def set_data_output(self, data):
        """
        Set target prediction
        """
        self.data_output = data

    def set_metadata(self, data):
        """
        Set illustrative features
        """
        self.metadata = data        

    def stop(self, request_options=None):
        """
        Stop session
        """
        path = ''
        return self._req(False, path, 'PUT', request_options, data = self)
        
    def _req(self, is_search, path, meth, request_options=None, params=None, data=None):
        """Perform an HTTPS request with retry logic."""
        path = '%s%s' % (self._request_path, path)
        return self.client._req(is_search, path, meth, request_options, params, data)
        
